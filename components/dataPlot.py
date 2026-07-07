import matplotlib.pyplot as plt, numpy as np
import threading, sys
from .queueClass import DataQueue

_color_map_max = 4
_color_map = ['blue', 'orange', 'green', 'red']  # 颜色映射列表


class DataPlot:
    def __init__(self, data_queue: DataQueue):
        self.data_queue = data_queue
        self.queue_style = data_queue.queue_style
        self.running = True

        # 绘图直接在主线程中进行： self.plot_data()

    def start(self):
        plt.ion()  # 开启交互模式
        self.fig, self.ax = plt.subplots()

        while self.running:
            try:
                if not self.data_queue.datax_queue.empty():
                    self.data_queue.get_data()  # 从队列中拿走数据，防止阻塞信息队列
                    self.update_plot()  # 更新绘图
            except Exception as e:
                print(f"主线程发生错误: {e}")


    def update_plot(self):
        """
        刷新一次窗口，通常用于增加一组数据点
        """
        self.ax.clear()
        for colorIndex, style in enumerate(self.queue_style):
            self.ax.plot(self.data_queue.datax_list, 
                         self.data_queue.datay_list[style], 
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