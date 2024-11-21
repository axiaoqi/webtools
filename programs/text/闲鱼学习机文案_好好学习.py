import random
from programs.text.xianyu_text import XianyuTextGenerator
from programs.settings import xuexiji_dir
from programs.text.名言警句_百度 import xue_xi_ming_yan
from programs.text.学习机标题生成 import xuexiji_name


class HaoHaoXueXi(XianyuTextGenerator):
    def run(self, start=None, end=None):

        # 第1句，卖点--通用文案
        first_list = self._open_file(self.data_dir / r'01通用文案\01_卖点.txt')
        choice_item = random.choice(first_list)
        self.choice_items.append(choice_item)

        # 第2句，标题
        # second_list = self._open_file(self.data_dir / r'好好学习_文案\02_标题.txt')
        # choice_item = random.choice(second_list)
        # self.choice_items.append(choice_item)
        name_file = xuexiji_dir / r'01文案\好好学习_文案\02_多字段标题生成.txt'
        self.choice_items.append(xuexiji_name(name_file))

        # 第3句，故事，售卖原因--通用文案
        third_list = self._open_file(self.data_dir / r'01通用文案\03_故事.txt')
        choice_item = random.choice(third_list)
        self.choice_items.append('\n' + choice_item)

        # 第4句，卖点提炼，分割符分割
        # fourth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\04_卖点提炼.txt', sep='|||')
        # choice_item = random.choice(fourth_list)
        # self.choice_items.append('\n' + choice_item)

        # 添加一个名言警句
        self.choice_items.append('\n每日名言：' + xue_xi_ming_yan())

        # 第5句，硬件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\05_参数_硬件.txt', sep='|||')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第6句，硬件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\06_参数_软件.txt', sep='|||')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第7句，售后，分割符分割
        fifth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\09_售后.txt', sep='|||')
        choice_item = random.choice(fifth_list)
        self.choice_items.append(choice_item)

        return self.choice_items

    def __str__(self):
        return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items])


def run():
    x = HaoHaoXueXi(xuexiji_dir / '01文案')

    """
    咸鱼AI学习机
    """
    x.run()
    return x


if __name__ == '__main__':
    # run()
    print(run())

