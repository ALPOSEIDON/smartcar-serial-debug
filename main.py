import components as cp
import signal, json
import matplotlib.pyplot as plt, numpy as np
import sys

def my_exit_handler(sig, frame):
    print("\n检测到 Ctrl+C，正在退出程序...")
    plt.close('all')  # 关闭所有 matplotlib 窗口，从而打破 plt.show() 的阻塞
    sys.exit(0)

if __name__ == "__main__":
    # 示例代码
    signal.signal(signal.SIGINT, my_exit_handler)

    data_queue = cp.DataQueue(queue_style=["pulse_R", "pulse_L"])
    bluetooth = cp.bluetoothDevice('COM5', 115200, data_queue)
    plot = cp.DataPlot(data_queue)
    plot.start()