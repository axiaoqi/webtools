import random
from pathlib import Path

from programs.settings import xuexiji_dir


def _open_file(file_path: Path, sep: str):
    """
    打开txt文件，所有的行是一个列表。然后根据每行根据特殊字符分割成子列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        file_list = f.readlines()
        data = [item.strip().split(sep) for item in file_list]  # 解析一下数据
    return data


def xuexiji_name():
    name_file = xuexiji_dir / r'01文案\好好学习_文案\02_多字段标题生成.txt'
    data = _open_file(name_file, sep='——')

    # 构建学习机名称
    name = ''
    for item in data:
        name = name + random.choice(item)

    return name
