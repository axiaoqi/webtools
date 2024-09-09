import random
from pathlib import Path
from typing import List

from icopywriter.icopywriter import CopywritingGenerator


class XiaohongshuCopywritingGenerator(CopywritingGenerator):
    """
    小红书文案生成器
    """

    def __init__(self, data_dir: Path):
        super().__init__(data_dir)
        self.chanxiu_files = []
        self.lvyou_files = []
        self.start_files = []
        self.end_files = []

        self.chanxiu_first_index = None
        self.lvyou_last_index = None

        self.choice_items = []  # 选择出来的文案输出的结果

        self._classification_data()

    @staticmethod
    def _find_last_special_char_position(lst, special_char):
        last_position = -1  # 初始化为 -1，表示未找到

        for i, item in enumerate(lst):
            if special_char in item:
                last_position = i  # 更新最后一次出现特殊字符的位置

        return last_position

    def _classification_data(self):
        """
        初始化txt数据
        """

        # 分割数据：开头，禅修，旅游，结尾
        self.chanxiu_first_index = next((i for i, x in enumerate([file.stem for file in self.data_files_path]) if '随机禅修' in x), -1)
        self.lvyou_last_index = self._find_last_special_char_position([file.stem for file in self.data_files_path], '随机旅游')

        self.start_files = self.data_files_path[:self.chanxiu_first_index]
        self.chanxiu_files = [path for path in self.data_files_path if '随机禅修' in path.stem]
        self.lvyou_files = [path for path in self.data_files_path if '随机旅游' in path.stem]
        self.end_files = self.data_files_path[self.lvyou_last_index+1:]

    def _select_item(self, file_path_list: List[Path], shuffle=False):
        """
        :param file_path_list: 文件列表
        :param shuffle: 是否要打乱顺序
        :return:
        """
        choice_items = []

        # 打开我们的文件列表，获取数据
        data_list = self._open_files(file_path_list)

        for item in data_list:
            if len(item) > 0:
                choice_item = random.choice(item)  # 随机选一条数据
                choice_items.append(choice_item)   # 数据添加到数据列表里面

        if shuffle:  # 如果要随机排序
            random.shuffle(choice_items)
        return choice_items

    # def

    def run(self):
        """
        :return: 被选中的文案
        """
        # 开始的
        start_choice_datas = self._select_item(self.start_files)

        # 禅修随机排序的
        chanxiu_choice_datas = self._select_item(self.chanxiu_files, shuffle=True)

        # 旅游随机排序的
        lvyou_choice_datas = self._select_item(self.lvyou_files, shuffle=True)

        # 结尾的
        end_choice_datas = self._select_item(self.end_files)

        # 合并数据
        self.choice_items = start_choice_datas + chanxiu_choice_datas + lvyou_choice_datas + end_choice_datas
        return self.choice_items

    def __str__(self):
        return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items])
