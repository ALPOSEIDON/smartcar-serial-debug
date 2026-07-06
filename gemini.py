import threading
import time
import queue
import sys
import signal
import random  # 模拟数据用
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 创建一个线程安全的队列，用于在蓝牙线程和绘图线程之间传递数据
data_queue = queue.Queue()
running = True  # 全局控制标志

# 2. 模拟蓝牙接收线程 (如果是真实蓝牙，替换为你的蓝牙读取逻辑)
def bluetooth_receive_thread():
    global running
    print("蓝牙接收线程已启动...")
    try:
        while running:
            # ==========================================
            # 真实蓝牙代码替换处:
            # data = bluetooth_socket.recv(1024)
            # val = parse_data(data)
            # ==========================================
            
            # 模拟每秒产生一个 0-100 的随机数据
            val = random.randint(0, 100) 
            data_queue.put(val)
            
            time.sleep(0.1)  # 采样率 10Hz
    except Exception as e:
        print(f"蓝牙线程发生错误: {e}")
    finally:
        print("蓝牙线程已关闭。")

# 3. 优雅处理 Ctrl+C
def signal_handler(sig, frame):
    global running
    print("\n检测到 Ctrl+C，正在退出程序...")
    running = False
    plt.close('all')  # 关闭所有 matplotlib 窗口，从而打破 plt.show() 的阻塞
    sys.exit(0)

# 注册信号捕获
signal.signal(signal.SIGINT, signal_handler)

# 4. Matplotlib 动画更新函数
def update_plot(frame, x_data, y_data, line):
    # 从队列中清空所有新数据，防止绘图延迟
    while not data_queue.empty():
        val = data_queue.get()
        y_data.append(val)
        if len(x_data) == 0:
            x_data.append(0)
        else:
            x_data.append(x_data[-1] + 1)
        
        # 限制数据显示长度（比如只显示最近 100 个点）
        if len(x_data) > 100:
            x_data.pop(0)
            y_data.pop(0)
    
    # 更新折线数据
    line.set_data(x_data, y_data)
    
    # 动态调整坐标轴视角
    if x_data:
        ax.set_xlim(x_data[0], x_data[-1] + 5)
        ax.set_ylim(min(y_data) - 10, max(y_data) + 10)
    
    return line,

# 5. 主程序准备
if __name__ == "__main__":
    # 初始化数据存储
    x_data, y_data = [], []

    # 初始化图表
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'r-', lw=2)
    ax.set_title("Real-time Bluetooth Data")
    ax.set_xlabel("Time / Count")
    ax.set_ylabel("Value")

    # 启动蓝牙接收后台线程
    bt_thread = threading.Thread(target=bluetooth_receive_thread, daemon=True)
    bt_thread.start()

    # 启动 Matplotlib 动画 (interval 单位为毫秒，表示每 50ms 刷新一次画面)
    # blit=True 可以大幅提高渲染效率
    ani = FuncAnimation(fig, update_plot, fargs=(x_data, y_data, line), interval=50, blit=False)

    try:
        plt.show()
    except KeyboardInterrupt:
        # 兜底捕获防止部分平台不触发 signal
        signal_handler(None, None)