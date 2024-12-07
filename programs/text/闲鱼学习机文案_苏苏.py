import random
from programs.text.xianyu_text import XianyuTextGenerator, XianyuImgTxt, generate_price
from programs.settings import xuexiji_dir


class SuSu(XianyuTextGenerator):
    def run(self, start=None, end=None):

        # 第1句，卖点--通用文案
        first_list = self._open_file(self.data_dir / r'01通用文案\01_卖点.txt')
        choice_item = random.choice(first_list)
        self.choice_items.append(choice_item)

        # # 第2句，标题
        second_list = self._open_file(self.data_dir / r'苏苏家_文案\02_标题.txt')
        choice_item = random.choice(second_list)
        self.choice_items.append(choice_item)

        # 第3句，故事，售卖原因--通用文案
        third_list = self._open_file(self.data_dir / r'01通用文案\03_故事.txt')
        choice_item = random.choice(third_list)
        self.choice_items.append(choice_item)

        # 第8句，英语名言
        eighth_list = self._open_file(self.data_dir / r'01通用文案\152个名言警句-英文.txt')
        choice_item = '一天一句【英语写作素材】：' + random.choice(eighth_list) + '\n咨询客服，可免费赠送150多句英语名言警句txt文档，后期还可免费更新，小学初中高中英语作文神器！！'
        self.choice_items.append(choice_item)

        # 第5句，硬件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'苏苏家_文案\05_参数_硬件.txt', sep='|||')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第6句，软件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'苏苏家_文案\06_参数_软件.txt', sep='|||')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第7句，售后，分割符分割
        fifth_list = self._open_file_by_sep(self.data_dir / r'苏苏家_文案\09_售后.txt', sep='|||')
        choice_item = random.choice(fifth_list)
        self.choice_items.append(choice_item)

        return self.choice_items

    def __str__(self):
        # return '\n'.join(self.choice_items)
        return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items])


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

