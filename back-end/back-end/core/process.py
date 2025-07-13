import os


def pre_process(data_path):
    # 从完整路径中提取文件名（不含扩展名)
    file_name = os.path.split(data_path)[1].split('.')[0]
    # 返回原始路径和文件名的元组
    return data_path, file_name
