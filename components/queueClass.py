import queue
from typing import Union
import threading

_default_data_receive = ["pulse_R", "pulse_L"]  # 使用数组传递字符串创建消息队列，可以任意组合自己的情况，建议使用英文，否则matplotlib可能会报错

class DataQueue:
    """
    数据队列类，用于管理数据的接收和存储。这是一个通用的模块，适用于其他需要数据队列的场景。它使用线程安全的队列来存储数据点，并提供了方法来添加和获取数据。
    """
    def __init__(self, queue_style:list = _default_data_receive):
        """
        :param (list) queue_style: 数据队列样式列表，使用数组传递字符串创建消息队列，可以任意组合自己的情况，建议使用英文，否则matplotlib可能会报错
        """
        # 备份所需要的数据队列样式
        self.queue_style:list = queue_style
        self._lock = threading.Lock()  # 创建一个锁对象，用于线程安全
        # 注册消息队列   注册空的列表以供保存历史数据
        self.data_dict: dict = {style: [] for style in queue_style}
        # 使用字典存储消息队列以及对应的历史数据列表
        self.data_queue = {style: queue.Queue() for style in queue_style}


    def put_data(self, data: list):
        """
        一次性将一组数据放入队列中，确保数据的顺序与注册的队列样式一致

        :param (list) data: 数据列表，请按照注册的顺序写入，确保数据的个数足够
        """
        assert len(data) == len(self.queue_style), "数据长度与队列样式长度不匹配，请检查输入数据。"
        with self._lock:  # 使用互斥锁确保线程安全
            for numIndex, style in enumerate(self.queue_style):
                self.data_queue[style].put(data[numIndex])
                self.data_dict[style].append(data[numIndex])

    def get_data(self):
        """
        从数据队列中一次获取全部数据

        :return data (list): 数据列表
        """
        with self._lock:  # 使用互斥锁确保线程安全
            data = [
                self.data_queue[style].get() for style in self.queue_style
            ]
        return data
    
if __name__ == "__main__":
    # 测试代码
    data_queue = DataQueue(queue_style=["pulse_R", "pulse_L"])
    data_queue.put_data([100, 200])
    data_queue.put_data([110, 210])
    data_queue.put_data([120, 220])

    while not data_queue.data_queue["pulse_R"].empty():
        data = data_queue.get_data()
        print(f"Data: {data}")