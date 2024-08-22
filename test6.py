import numpy as np
import time

def generate_floats(num_floats, filename):
    """
    生成指定數量的隨機浮點數並將其寫入指定的文件。
    
    :param num_floats: 生成的浮點數數量
    :param filename:   要寫入的文件名
    """
    data = np.random.rand(num_floats)
    with open(filename, 'w') as f:
        for value in data:
            f.write(f"{value}\n")

def read_floats(filename):
    """
    從文件中讀取浮點數並返回一個列表。
    
    :param filename: 讀取的文件名
    :return:         浮點數列表
    """
    with open(filename, 'r') as f:
        return [float(line.strip()) for line in f]

def sort_floats(data):
    """
    對浮點數列表進行排序並返回排序後的列表。
    
    :param data: 需要排序的浮點數列表
    :return:     排序後的浮點數列表
    """
    return sorted(data)

def measure_sorting_time(data):
    """
    測量排序操作的耗時。
    
    :param data: 需要排序的浮點數列表
    :return:     排序後的列表和排序耗時
    """
    start_time = time.time()
    sorted_data = sort_floats(data)
    end_time = time.time()
    return sorted_data, end_time - start_time

if __name__ == "__main__":
    # 生成浮點數並寫入文件
    num_floats = 20000000
    filename = 'random_floats.txt'
    generate_floats(num_floats, filename)
    
    # 讀取浮點數
    data = read_floats(filename)
    
    # 排序並測量時間
    sorted_data, elapsed_time = measure_sorting_time(data)
    
    # 輸出結果
    print(f"排序完成，耗時 {elapsed_time:.2f} 秒")
