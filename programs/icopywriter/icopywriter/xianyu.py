import random
from pathlib import Path
from typing import List, Tuple

from icopywriter.icopywriter import CopywritingGenerator


class XianyuCopywritingGenerator(CopywritingGenerator):
    """
    咸鱼文案生成器
    """

    def __init__(self, data_dir: Path):
        super().__init__(data_dir)
        self.choice_items = []  # 选择出来的文案输出的结果

    def run(self, start=None, end=None):
        """
        :param start: 这个是随机打乱顺序的参数。start到end行乱序排列
        :param end:
        :return: 被选中的文案
        """
        # 每一行选一个出来
        data_list = self._open_all_file()

        for item in data_list:
            choice_item = random.choice(item)
            self.choice_items.append(choice_item)

        # 如果需要随机排序,排序一下
        if start:
            self.choice_items = self._random_shuffle(self.choice_items, start, end)

        return self.choice_items

    def __str__(self):
        return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items])


class XianyuImgTxt(CopywritingGenerator):
    def __init__(self):
        super().__init__()
        self.data = []

    def get_items(self, file_path: Path, count: int = 1):
        data_list = self._open_file(file_path)
        choice_items = random.sample(data_list, count)  # 随机选取count个数据
        self.data.append(choice_items)  # 把数据存放到data列表内

    def __str__(self):
        return '\n'.join(['，'.join(i) for i in self.data])


def generate_price(intervals: List[Tuple] = None):
    """
    intervals = [(310, 370), (460, 480)]
    """
    # 随机选择一个区间
    start, end = random.choice(intervals)

    # 在区间内随机选择一个数，结尾是8或者9
    number = random.randint(start, end)
    while number % 10 not in [8, 9]:
        number = random.randint(start, end)

    return number
