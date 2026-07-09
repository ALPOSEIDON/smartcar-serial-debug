import components as cp, signal
import matplotlib.pyplot as plt, sys

def exit_handler(fig, frame):
    """
    重构退出信号，防止线程阻塞
    """
    print("\n检测到 Ctrl+C，正在退出程序...")
    plt.close('all')  # 关闭所有 matplotlib 窗口，从而打破 plt.show() 的阻塞
    sys.exit(0)

if __name__ == "__main__":
    # 示例代码
    import argparse
    parser = argparse.ArgumentParser(description="根据保存的历史数据查看图像")
    parser.add_argument("-choose", "--choose_one_path", action="store_true",
                         help="请传入是否需要指定打开的文件路径，若不需要则默认打开文件名最大的那个。默认不需要")
    
    args = parser.parse_parser_args() if 'parse_parser_args' in dir(parser) else parser.parse_args()

    signal.signal(signal.SIGINT, exit_handler)     # 注册退出信号

    data = cp.DataLoader(need_specific_path=args.choose_one_path)
    data.load_data()
    plot= cp.DataLoadPlot()
    plot.draw(data.dict["x_data"], data.dict["y_data"])