import matplotlib.pyplot as plt
import threading, sys, signal
from .queueClass import DataQueue
from abc import ABC, abstractmethod


_color_map = ['blue', 'orange', 'green', 'red']  # 颜色映射列表
_color_map_max = len(_color_map)



class x_value(ABC):
    """
    为DataPlot方法提供绘图x坐标的基类，可以继承这个类以构造不同形式的x坐标
    """
    def __init__(self):
        self.x_vlue_list = []

    @abstractmethod
    def refresh_x_value(self, new_value = None):
        """"
        需要自己构造这个方法，实现对x坐标数据的刷新。记得判断new_value参数，因为有可能需要输入数据以更新参数。有如下重构要求

        :param new_value:   可选的参数，为x刷新提供数据。如果不需要用到这个参数请将其置为None并且加以判断。可以从get_x_new_value获取参数
        """
        pass
    
    @abstractmethod
    def get_x_new_value(self):
        """
        重构此方法，用于给x_value_list提供新的值，可以当作参数传给refresh_x_value
        """
        pass

    def return_x_list(self):
        return self.x_vlue_list
    
    def return_x_last_value(self):
        return self.x_vlue_list[-1] if len(self.x_vlue_list) != 0 else None
    
class isometry(x_value):
    """
    提供离散的等距点阵，给DataPlot画图
    """
    def __init__(self):
        super().__init__()
        self.count = 0

    def refresh_x_value(self, new_value = None):
        self.x_vlue_list.append(self.count)
        self.count += 1

    def get_x_new_value(self):
        return None



class DataPlot:
    def __init__(self, data_queue: DataQueue, x_value_class:x_value = isometry()):
        self.data_queue = data_queue
        self.queue_style = data_queue.queue_style
        self.x_class = x_value_class
        self.running = True

        signal.signal(signal.SIGINT, self.exit_handler)     # 注册退出信号

        # 绘图直接在主线程中进行： self.plot_data()

    def start(self):
        plt.ion()  # 开启交互模式
        self.fig, self.ax = plt.subplots()
        while self.running:
            try:
                if not self.data_queue.data_queue[self.queue_style[0]].empty():             # 这里还可以改进一下
                    self.data_queue.get_data()  # 从队列中拿走数据，防止阻塞信息队列
                    self.update_plot()  # 更新绘图
            except Exception as e:
                print(f"主线程发生错误: {e}")

    def update_plot(self):
        """
        刷新一次窗口，用于增加一组数据点
        """
        self.ax.clear()
        with self.data_queue._lock:
            self.x_class.refresh_x_value(self.x_class.get_x_new_value())        # 刷新x轴坐标值
            min_len = min(
                len(self.x_class.return_x_list()), 
                len(self.data_queue.data_dict[self.queue_style[0]]))
            for colorIndex, style in enumerate(self.queue_style):
                self.ax.plot(self.x_class.return_x_list()[:min_len], 
                            self.data_queue.data_dict[style][:min_len], 
                            color=_color_map[colorIndex if colorIndex < _color_map_max else _color_map_max - 1], 
                            label=style)

        self.ax.set_title('Real Time Data Plot')
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.legend()                    # 显示图例
        self.ax.grid(True)

        self.fig.canvas.draw()              # 绘制图形
        self.fig.canvas.flush_events()      # 刷新图形
        plt.pause(0.01)                     # 刷新窗口

    def stop(self):
        """
        停止绘图线程
        """
        self.running = False
        plt.close('all')  # 关闭所有 matplotlib 窗口，从而打破 plt.show() 的阻塞
        sys.exit(0)

    def exit_handler(self, fig, frame):
        """
        重构退出信号，防止线程阻塞
        """
        print("\n检测到 Ctrl+C，正在退出程序...")
        plt.close('all')  # 关闭所有 matplotlib 窗口，从而打破 plt.show() 的阻塞
        sys.exit(0)
