import queue
from typing import Union
import threading

_default_data_receive = ["pulse_R", "pulse_L"]  # 使用数组传递字符串创建消息队列，可以任意组合自己的情况，建议使用英文，否则matplotlib可能会报错

class DataQueue:
    """
    数据队列类，用于管理数据的接收和存储
    """
    def __init__(self, queue_style:list = _default_data_receive):
        """
        :param (list) queue_style: 数据队列样式列表，使用数组传递字符串创建消息队列，可以任意组合自己的情况，建议使用英文，否则matplotlib可能会报错
        """
        # 备份所需要的数据队列样式
        self.queue_style:list = queue_style
        self._lock = threading.Lock()  # 创建一个锁对象，用于线程安全
        # 注册消息队列
        self.datax_queue = queue.Queue()
        # 使用字典存储消息队列以及对应的历史数据列表
        self.datay_queue = {style: queue.Queue() for style in queue_style}
        # 注册空的列表以供保存历史数据
        self.datax_list = []
        self.datay_list: dict[str, list] = {style: [] for style in queue_style}


    def put_data(self, datax: Union[int, float], datay: list):
        """
        :param datax: 数据x
        :param datay: 数据y列表，请按照注册的顺序写入，确保数据的个数足够
        """
        with self._lock:  # 使用互斥锁确保线程安全
            for style in self.queue_style:
                self.datay_queue[style].put(datay[self.queue_style.index(style)])
                self.datay_list[style].append(datay[self.queue_style.index(style)])
            # 最后调用 put 方法将数据点x写入，防止有时候误操作。虽然实际上调用互斥锁已经避免了此类问题
            self.datax_list.append(datax)
            self.datax_queue.put(datax)

    def get_data(self):
        """
        从数据队列中获取数据

        :return datax: 数据x
        :return datay: 数据y列表
        """
        datax = self.datax_queue.get()
        datay = [
            self.datay_queue[style].get() for style in self.queue_style
        ]
        return datax, datay
    
if __name__ == "__main__":
    # 测试代码
    data_queue = DataQueue(queue_style=["pulse_R", "pulse_L"])
    data_queue.put_data(1, [100, 200])
    data_queue.put_data(2, [110, 210])
    data_queue.put_data(3, [120, 220])

    while not data_queue.datax_queue.empty():
        datax, datay = data_queue.get_data()
        print(f"DataX: {datax}, DataY: {datay}")