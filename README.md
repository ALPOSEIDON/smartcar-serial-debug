# 智能车串口调试脚本

### 使用教程：

- 使用venv创建虚拟运行环境：

```python
>>>cd your_workspace
>>>python -m venv .venv
>>>your_workspace\.venv\Scripts\activate
>>>pip install -r requirements.txt
```

- 激活环境后运行

```python
>>>python main.py
```

- 各个参数解释：
  
  1. queue_style 就是你可以在图像上绘制的曲线名称，例如["pulse_R", "pulse_L"]
  
  2. 修改bluetoothDevice中的串口名和波特率 

```python
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
```
