import random
from programs.text.xianyu_text import XianyuTextGenerator, XianyuImgTxt, generate_price
from programs.settings import xuexiji_dir


class SuSu(XianyuTextGenerator):
    def run(self, start=None, end=None):

        # 第1句，卖点--通用文案
        first_list = self._open_file_by_sep(self.data_dir / r'01通用文案\01_卖点.txt')
        choice_item = random.choice(first_list)
        self.choice_items.append(choice_item)

        # # 第2句，标题
        second_list = self._open_file_by_sep(self.data_dir / r'智慧学习_文案\02_标题.txt', sep='\n\n')
        choice_item = random.choice(second_list)
        self.choice_items.append(choice_item)

        # 第3句，故事，售卖原因--通用文案
        third_list = self._open_file_by_sep(self.data_dir / r'01通用文案\03_故事.txt', sep='\n\n')
        choice_item = random.choice(third_list)
        self.choice_items.append(choice_item)

        # 第5句，硬件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'智慧学习_文案\05_参数_硬件.txt', sep='\n\n')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第6句，软件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'智慧学习_文案\06_参数_软件.txt', sep='\n\n')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第7句，售后，分割符分割
        fifth_list = self._open_file_by_sep(self.data_dir / r'智慧学习_文案\09_售后.txt', sep='\n\n')
        choice_item = random.choice(fifth_list)
        self.choice_items.append(choice_item)

        return self.choice_items


def run():
    x = SuSu(xuexiji_dir / '01文案')

    """
    咸鱼AI学习机
    """
    x.run()
    return x


if __name__ == '__main__':
    # run()
    print(run())

