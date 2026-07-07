import components as cp

queue_style = [
    ["pulse_R", "pulse_L"],
]

if __name__ == "__main__":
    # 示例代码
    data_queue = cp.DataQueue(queue_style=queue_style[0])
    bluetooth = cp.bluetoothDevice('COM5', 115200, data_queue)
    plot = cp.DataPlot(data_queue)
    plot.start()