import random
from pathlib import Path
from typing import List, Tuple

from programs.gemini_text.gemini_text import gemini_text
from programs.text.text import TextGenerator


class XianyuTextGenerator(TextGenerator):
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
        # return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items]) # 原来的
        items = [item.strip() for item in self.choice_items if item.strip()]

        # 处理边界情况
        if not items:
            return ""

        # 2. 拼接逻辑 (使用我们之前更简洁的“向前看”方案)
        # 第一个元素总是直接添加
        result = [items[0]]

        # 从第二个元素开始遍历
        for i in range(1, len(items)):
            prev_element = items[i - 1]  # 前一个元素
            current_element = items[i]  # 当前元素

            # 如果前一个元素是标题，并且当前元素不是标题，则直接用一个空格连接
            # 为什么是空格？因为标题【...】和正文之间通常需要一个空格来断开
            if '【' in prev_element and '【' not in current_element:
                result.append(' ' + current_element)
            # 其他所有情况，都用两个换行符（一个空行）隔开
            else:
                result.append('\n\n' + current_element)

        # 3. 用空字符串把所有部分连接起来
        all_text = "".join(result)
        try:
            # 用gemini改写文字
            first_parts = "我是一名闲鱼卖家，为了防止系统查重，改写下面的句子。直接给出一个结果，无需其他提示，无需多版本。文案格式保持不变，不需要加粗文字。同款这两个字不能少，因为不是正品。可以适当口语化。文案如下:"
            new_text = gemini_text(first_parts + '\n' + all_text, model='gemini-2.5-flash-preview-05-20')
            return new_text
        except Exception as e:
            return all_text


class XianyuImgTxt(TextGenerator):
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
