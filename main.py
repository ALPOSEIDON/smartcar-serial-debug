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
_default_queue_style = 0

if __name__ == "__main__":
    # 示例代码
    import argparse
    parser = argparse.ArgumentParser(description="蓝牙串口接受程序")
    parser.add_argument("-c", "--com", default=COM, type=str, help="请传入需要打开的串口号，默认为 COM")
    parser.add_argument("-b", "--baudrate", default=baudrate, type=int, help="串口的波特率，默认为115200")
    parser.add_argument("-ch", "--channels", default=queue_style[_default_queue_style], nargs='+', type=str, help="最终需要接受的通道列表")
    
    args = parser.parse_parser_args() if 'parse_parser_args' in dir(parser) else parser.parse_args()

    signal.signal(signal.SIGINT, exit_handler)     # 注册退出信号
    data_queue = cp.DataQueue(queue_style=args.channels)
    bluetooth = cp.bluetoothDevice(args.com, args.baudrate, data_queue)
    plot = cp.DataPlot(data_queue)
    plot.start()