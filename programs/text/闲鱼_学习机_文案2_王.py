import random
from programs.text.xianyu_text import XianyuTextGenerator, XianyuImgTxt, generate_price
from programs.settings import SynologyDrive


class XianyuTextGenerator2(XianyuTextGenerator):
    # def __init__(self, data_dir: Path):
    #     super().__init__(data_dir)
    #     self.choice_items = []  # 选择出来的文案输出的结果

    def run(self, start=None, end=None):

        # 第一句，卖点
        first_list = self._open_file(self.data_files_path[0])
        choice_item = random.choice(first_list)
        self.choice_items.append(choice_item)

        # 第二句，标题
        second_list = self._open_file(self.data_files_path[1])
        choice_item = random.choice(second_list)
        self.choice_items.append(choice_item)

        # 第三句，故事，售卖原因
        third_list = self._open_file(self.data_files_path[2])
        choice_item = random.choice(third_list)
        self.choice_items.append(choice_item)

        # 第4句，配置，分割符分割
        fourth_list = self._open_file_by_sep(self.data_files_path[3], sep='|||')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第5句，售后，分割符分割
        fifth_list = self._open_file_by_sep(self.data_files_path[4], sep='|||')
        choice_item = random.choice(fifth_list)
        self.choice_items.append(choice_item)

        return self.choice_items

    def __str__(self):
        return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items])


def run():
    """
    价格
    """
    print(f'价格：{generate_price(intervals=[(310, 370)])}元\n')

    """
    图片文案
    """

    img_txt_path = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\01文案\图片内容'
    xianyuimg = XianyuImgTxt()

    # 打印所有的文件
    files = img_txt_path.rglob('*.txt')
    for file in files:
        if '主图卖点' in file.stem:
            count = 6
            xianyuimg.get_items(file, count)
        elif '主图标签' in file.stem:
            count = 6
            xianyuimg.get_items(file, count)
        else:
            xianyuimg.get_items(file)

    print(xianyuimg)

    """
    咸鱼AI学习机
    """
    x = XianyuTextGenerator2(SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\01文案\文案素材2_抄王')
    x.run()
    print(x)


if __name__ == '__main__':
    while True:
        run()
        print('\n')
        input("按 Enter 键运行一次，或 Ctrl+C 退出: ")
        print('\n')


