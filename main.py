import components as cp, signal
import matplotlib.pyplot as plt, sys

COM = 'COM5'
baudrate = 115200

def exit_handler(fig, frame):
    """
    重构退出信号，防止线程阻塞
    """
    print("\n检测到 Ctrl+C，正在退出程序...")
    save_data()
    plt.close('all')  # 关闭所有 matplotlib 窗口，从而打破 plt.show() 的阻塞
    sys.exit(0)

def save_data():
    data = cp.DataPackage()
    data.addData('x_data', plot.x_class.return_x_list())
    data.addData('y_data', data_queue.data_dict)
    data.addData('timestamp', cp.returnTime())
    data.saveData()

queue_style = [
    ["pulse_R", "pulse_L"],
]

if __name__ == "__main__":
    # 示例代码
    signal.signal(signal.SIGINT, exit_handler)     # 注册退出信号
    data_queue = cp.DataQueue(queue_style=queue_style[0])
    bluetooth = cp.bluetoothDevice(COM, baudrate, data_queue)
    plot = cp.DataPlot(data_queue)
    plot.start()