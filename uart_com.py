import serial, matplotlib.pyplot as plt, numpy as np
import threading
import time
import queue
import re
from typing import Union

data_receive_mode = 2  # n: 只接收n个数据 , 当前n<=4， 但是可以扩展
datax_queue = queue.Queue()
data1_queue = queue.Queue()
data2_queue = queue.Queue()
data3_queue = queue.Queue()
data4_queue = queue.Queue()
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
    global running, data_receive_mode
    bluetooth = bluetoothDevice('COM5', 115200)
    print("蓝牙接收线程已启动...")
    count = 0       # 记录数据点的数量
    try:
        while running:
            recv = bluetooth.ser.readline()
            if recv:
                string = recv.decode().strip()
                nums = data_receive(string)         # 找到所有的数字
                print(f"接收到数据: {nums}")
                # 使用for循环遍历数组
                for i in range(data_receive_mode):  # 确保不会超过4个数据点
                    if i == 0:
                        data1_queue.put(nums[i])
                    elif i == 1:
                        data2_queue.put(nums[i])
                    elif i == 2:
                        data3_queue.put(nums[i])
                    elif i == 3:
                        data4_queue.put(nums[i])
                # 认为接收到一次数据点
                datax_queue.put(count)  # 将数据点的索引放入队列
                count += 1  
    except Exception as e:
        print(f"蓝牙线程发生错误: {e}")
    finally:
        print("蓝牙线程已关闭。")

def data_receive(data:str):
    """
    Returns:
        返回正常的数组
    """
    data = re.findall(r'-?\d+', data)
    return [int(num) for num in data]





class runningData:
    def __init__(self, data_style:int = 0):
        self.x_data = []
        self.y1_data = []
        self.y2_data = []
        self.y3_data = []
        self.y4_data = []

    def append_data(self, datax:Union[int, float], datay:list):     # 注意确保 datay 是一个列表，长度不低于 data_receive_mode
        self.x_data.append(datax)
        for i in range(data_receive_mode):
            if i == 0:
                self.y1_data.append(datay[i])
            elif i == 1:
                self.y2_data.append(datay[i])
            elif i == 2:
                self.y3_data.append(datay[i])
            elif i == 3:
                self.y4_data.append(datay[i])

    def print_data(self):
        print(self.y1_data[-1])



class plotData:
    def __init__(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.data = runningData()

    def append_data(self, datax:Union[int, float], datay:list):
        self.data.append_data(datax, datay)
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        for i in range(data_receive_mode):
            if i == 0:
                self.ax.plot(self.data.x_data, self.data.y1_data, color='blue', label='curve1')
            elif i == 1:
                self.ax.plot(self.data.x_data, self.data.y2_data, color='orange', label='curve2')
            elif i == 2:
                self.ax.plot(self.data.x_data, self.data.y3_data, color='green', label='curve3')
            elif i == 3:
                self.ax.plot(self.data.x_data, self.data.y4_data, color='red', label='curve4')
        self.ax.set_title('Real Time Data Plot')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.legend()                    # 显示图例
        self.ax.grid(True)

        self.fig.canvas.draw()              # 绘制图形
        self.fig.canvas.flush_events()        # 刷新图形
        plt.pause(0.01)                 # 刷新窗口




if __name__ == '__main__':
    data = plotData()

    # 启动蓝牙接收后台线程
    bt_thread = threading.Thread(target=bluetooth_receive_thread, daemon=True)
    bt_thread.start()


    while True:
        try:
            if not datax_queue.empty():
                datax = datax_queue.get()
                datay = []
                for i in range(data_receive_mode):
                    if i == 0:
                        datay.append(data1_queue.get())
                    elif i == 1:
                        datay.append(data2_queue.get())
                    elif i == 2:
                        datay.append(data3_queue.get())
                    elif i == 3:
                        datay.append(data4_queue.get())
                data.append_data(datax, datay)
                # data.print_data()
        except Exception as e:
            print(f"主线程发生错误: {e}")

    # print(data_receive("123, 456, -789"))  # 测试数据接收函数