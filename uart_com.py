import serial, matplotlib.pyplot as plt, numpy as np
import threading
import time
import queue
import re


data_queue = queue.Queue()
running = True  # 全局控制标志

class bluetoothDevice:
    def __init__(self, com_name:str, bit_per_second:int):
        self.ser = serial.Serial(com_name, bit_per_second)

    def debug_func(self):
        i=0
        while True:
            print(self.ser.readline())
            if i%50 ==0 :
                self.ser.write(b'\x0ahello, world!\x0d\x0a')
                # ser.write(b'\x0d')
                self.ser.flush()
            i += 1


def bluetooth_receive_thread():
    """
    Brief:
        蓝牙接收线程，读取串口数据并放入队列中
    """
    global running
    bluetooth = bluetoothDevice('COM5', 115200)
    print("蓝牙接收线程已启动...")
    try:
        while running:
            recv = bluetooth.ser.readline()
            if recv:
                string = recv.decode().strip()
                data_queue.put(data_receive(string))
    except Exception as e:
        print(f"蓝牙线程发生错误: {e}")
    finally:
        print("蓝牙线程已关闭。")



class runningData:
    def __init__(self, data_style:int = 0):
        self.x_data = []
        self.y1_data = []
        self.count = 0

    def append_data(self, data):
        self.x_data.append(self.count)
        self.y1_data.append(data)
        self.count += 1

    def print_data(self):
        print(self.y1_data[-1])



class plotData:
    def __init__(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.data = runningData()

    def append_data(self, data):
        self.data.append_data(data)
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.data.x_data, self.data.y1_data, color='blue', label='曲线一')
        self.ax.set_title('实时速度曲线')
        self.ax.set_xlabel('X轴')
        self.ax.set_ylabel('Y轴')
        self.ax.legend()                    # 显示图例
        self.ax.grid(True)

        self.fig.canvas.draw()              # 绘制图形
        self.fig.canvas.flush_events()        # 刷新图形
        plt.pause(0.01)                 # 刷新窗口



def data_receive(data:str):
    """
    Returns:
        返回正常的数组
    """
    data = re.findall(r'-?\d+', data)
    return int(data[0])


if __name__ == '__main__':
    data = plotData()
    bluetooth = bluetoothDevice('COM5', 115200)



    while True:
        try:
            recv = bluetooth.ser.readline()
            if recv:
                string = recv.decode().strip()
                data.append_data(data_receive(string))
                data.data.print_data()
        except Exception as e:
            print(f"Error occurred: {e}")


#bluetoothDevice('COM8', 9600).debug_func()