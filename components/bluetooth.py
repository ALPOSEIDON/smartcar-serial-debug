from .queueClass import DataQueue
import serial, threading, queue, re

class bluetoothDevice:
    def __init__(self, com_name:str, bit_per_second:int, dataQueue: DataQueue):
        """
        初始化串口名称以及波特率
        """
        self.ser = serial.Serial(com_name, bit_per_second)
        self.data_queue = dataQueue
        self.count = 0          # 记录数据点的数量，但也可以是一些其他你想要的东西
        self.running = True     # 控制线程运行的标志

        self._thread = threading.Thread(target=self.bluetooth_receive_thread, daemon = True)
        self._thread.start()    # 启动线程

    def bluetooth_receive_thread(self):
        """
        蓝牙接收线程，读取串口数据并放入队列中
        """
        # bluetooth = bluetoothDevice('COM5', 115200)
        print("蓝牙接收线程已启动...")
        try:
            while self.running:
                recv = self.ser.readline()
                if recv:
                    string = recv.decode().strip()
                    nums = data_receive(string)        # 找到所有的数字

                    print(f"接收到数据: {nums}")        # 可以注释掉这行，避免打印过多信息

                    # 使用封装好的消息队列存储信息，同时发送信息给别的线程S
                    self.data_queue.put_data(self.count, nums)  # 将数据点的索引和数据放入队列
                    self.count += 1  
        except Exception as e:
            print(f"蓝牙线程发生错误: {e}")
        finally:
            print("蓝牙线程已关闭，请使用ctrl+c终止进程，并排查问题。")

    def stop(self):
        """
        停止蓝牙接收线程
        """
        self.running = False

def data_receive(data:str):
    """
    :param (str) data: 输入的字符串
    :return out (list): 返回正常的数组
    """
    data = re.findall(r'-?\d+', data)
    return [int(num) for num in data]

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