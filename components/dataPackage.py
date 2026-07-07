from .fileOperate import DataSaver
import time

def returnTime():
    utc = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", utc)

class DataPackage:
    def __init__(self, dataSaver:DataSaver = DataSaver()):
        self.dataSaver = dataSaver
        self.dict = {}
        print(returnTime())

    def saveData(self):
        self.dataSaver.save_data(self.dict)

    def addData(self, dataName:str, data):
        """
        用于添加字典中的数据
        """
        self.dict[dataName] = data 

    def dataRefresh(self):
        self.dict = {}

if __name__ == "__main__":
    data = DataPackage().saveData()