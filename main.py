import components as cp

if __name__ == "__main__":
    # 测试代码
    data_queue = cp.DataQueue(queue_style=["pulse_R", "pulse_L"])
    bluetooth = cp.bluetoothDevice('COM5', 115200, data_queue)
    plot = cp.DataPlot(data_queue)