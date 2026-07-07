from .queueClass import DataQueue
import serial, threading, queue, re

class bluetoothDevice:
    def __init__(self, com_name:str, bit_per_second:int, dataQueue: DataQueue, receive_mode:str = "int"):
        """
        初始化串口名称，波特率以及接受数据类型。
        这是一个蓝牙接收类，使用线程来接收蓝牙数据，并将数据放入消息队列中。确保所有数据放在一句话中传输，最后以\n结尾，避免数据丢失。

        :param (str) receive_mode:  将数据转化的目标类型
            默认有 int float str三种类型
        """
        self.ser = serial.Serial(com_name, bit_per_second)
        self.data_queue = dataQueue
        self.receive_mode = receive_mode
        self.running = True     # 控制线程运行的标志
        self.start()

    def bluetooth_receive_thread(self):
        """
        蓝牙接收线程，读取串口数据并放入队列中。
        """
        # bluetooth = bluetoothDevice('COM5', 115200)
        print("蓝牙接收线程已启动...")
        try:
            while self.running:
                recv = self.ser.readline()              # 程序会在这里阻塞，直到接收到一行以\n结尾的数据
                if recv:
                    string = recv.decode().strip()
                    nums = self.data_receive(string, receive_mode = self.receive_mode)         # 找到所有的数字

                    print(f"接收到数据: {nums}")         # 可以注释掉这行，避免打印过多信息

                    # 使用封装好的消息队列存储信息，同时发送信息给别的线程S
                    self.data_queue.put_data(nums)      # 将数据放入队列
        except Exception as e:
            print(f"蓝牙线程发生错误: {e}")
        finally:
            print("蓝牙线程已关闭，请使用ctrl+c终止进程，并排查问题。")

    def start(self):
        """
        开始蓝牙接收线程
        """
        self.running = True
        self._thread = threading.Thread(target=self.bluetooth_receive_thread, daemon = True)
        self._thread.start()    # 启动线程

    def stop(self):
        """
        停止蓝牙接收线程
        """
        self.running = False

    def data_receive(self, data:str, receive_mode:str = "int"):
        """
        :param (str) data: 输入的字符串
        :param (str) receive_mode:  将数据转化的目标类型
            默认有 int float str三种类型
        :return out (list): 返回整数数组
        """
        data = re.findall(r'-?\d+', data)
        if receive_mode == "int":
            return [int(num) for num in data]
        elif receive_mode == "float":
            return [float(num) for num in data]
        elif receive_mode == "str":
            return [num for num in data]

if __name__ == "__main__":
    # 测试代码
    data_queue = DataQueue(queue_style=["pulse_R", "pulse_L"])
    bluetooth = bluetoothDevice('COM5', 115200, data_queue)

    try:
        while True:
            if not data_queue.datax_queue.empty():
                datax, datay = data_queue.get_data()
                print(f"DataX: {datax}, DataY: {datay}")
    except KeyboardInterrupt:
        bluetooth.stop()
        print("程序已终止。")