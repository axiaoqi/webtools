import random
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List


class BaseTextGenerator:
    """
    定义一个文案生成器的接口
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        raise NotImplementedError(
            "Should implement run()"
        )


class TextGenerator(BaseTextGenerator):
    """
    文案生成器基本功能的实现
    """
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir
        self.data_files_path = []  # 所有的txt文件的路径

        if self.data_dir:
            self._add_data()  # 初始化文件名称列表

    def _add_data(self):
        """
        初始化txt数据
        """
        # 文件按文件名排序一下
        txt_files = sorted([item for item in self.data_dir.iterdir() if item.name.endswith('.txt')],
                           key=lambda x: int(x.stem.split('_')[0]))
        # 数据添加进去
        self.data_files_path.extend(txt_files)

    def _open_all_file(self):
        data_list = []
        for item in self.data_files_path:
            _data = self._open_file(item)
            data_list.append(_data)
        return data_list

    @staticmethod
    def _open_file(file_path: Path) -> list:
        """
        打开txt文件，每行，转为列表
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            file_list = f.readlines()
        data = [item.strip() for item in file_list]  # 解析一下数据
        return data

    def _open_files(self, file_paths: List[Path]):
        """
        打开txt文件，转为列表
        """
        data_list = []
        for item in file_paths:
            _data = self._open_file(item)
            data_list.append(_data)
        return data_list

    @staticmethod
    def _random_shuffle(data: list, start, end):
        """
        从start行到end行随机排序
        """
        sublist = data[start:(end + 1)]  # 提取子列表
        random.shuffle(sublist)  # 随机排序子列表
        # 将排序后的子列表放回原列表
        data[start:end + 1] = sublist

        return data

    @staticmethod
    def _open_file_by_sep(file_path: Path, sep: str):
        """
        打开txt文件，根据特殊字符分割成列表
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        data = content.split(sep)  # 解析一下数据
        return data

    def run(self):
        pass
