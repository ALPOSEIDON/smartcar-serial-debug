import json
import os
from pathlib import Path

def file_loader(filepath, ENCODING = 'utf-8'):
    """
    file_loader 的 Docstring。用于将json文件加载成python可读文件
    
    :param filepath: 文件路径
    :param ENCODING: 编码格式
    """
    with open(filepath, encoding=ENCODING) as fp:
        return json.load(fp)

def file_store(filepath, files,ENCODING = 'utf-8'):
    """
    name_store 的 Docstring。用于将python格式数据存储为json文件
    
    :param filepath: 文件路径
    :param files: 需要保存的文件
    :param ENCODING: 编码格式
    """
    with open(filepath, mode = 'w', encoding=ENCODING) as fp:
        json.dump(files, fp)


class DataSaver:
    def __init__(self, save_dir="data_backup"):
        self.save_dir = Path(save_dir)
        # 自动创建保存数据的文件夹，如果不存在的话
        self.save_dir.mkdir(exist_ok=True)
        # 寻找当前文件夹下最大的编号，防止覆盖之前的记录
        self.file_counter = self._get_next_counter()

    def _get_next_counter(self):
        """检查目录，找出接下来应该从几开始编号"""
        existing_files = [f.stem for f in self.save_dir.glob("*.json")]
        
        # 过滤出纯数字的文件名
        existing_numbers = []
        for name in existing_files:
            if name.isdigit():
                existing_numbers.append(int(name))
                
        # 如果文件夹是空的，从 1 开始；否则从最大值 + 1 开始
        return max(existing_numbers) + 1 if existing_numbers else 1

    def save_data(self, data_dict):
        """将传入的数据保存为新的 json 文件"""
        file_name = f"{self.file_counter}.json"
        file_path = self.save_dir / file_name
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # indent=4 让 json 看起来有缩进，方便人类阅读
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            print(f"[成功] 数据已保存至: {file_path}")
            
            # 计数器加 1，下一次就是新文件
            self.file_counter += 1
        except Exception as e:
            print(f"[错误] 保存文件失败: {e}")

# ================= 怎么在你的接收循环里调用？ =================
if __name__ == "__main__":
    saver = DataSaver()  # 初始化保存器，默认创建 received_data 文件夹
    
    # 模拟蓝牙每收到一次数据的动作
    try:
        while True:
            # 假设这是你蓝牙收到的单次数据（打包成字典）
            mock_bluetooth_data = {
                "timestamp": "2026-07-06 14:00:00",
                "sensor_value": 42.5,
                "status": "OK"
            }
            
            # 保存数据
            saver.save_data(mock_bluetooth_data)
            
            # 模拟等待下一次接收
            import time
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，停止保存，安全退出。")
