import random
from programs.text.xianyu_text import XianyuTextGenerator
from programs.settings import xuexiji_dir
from programs.text.学习机标题生成 import xuexiji_name


class HaoHaoXueXi(XianyuTextGenerator):
    def run(self, start=None, end=None):

        # 第1句，卖点--通用文案
        first_list = self._open_file_by_sep(self.data_dir / r'01通用文案\01_卖点.txt')
        choice_item = random.choice(first_list)
        self.choice_items.append(choice_item)

        # 第2句，标题
        name_file = xuexiji_dir / r'01文案\好好学习_文案\02_多字段标题生成.txt'
        self.choice_items.append(xuexiji_name(name_file))

        # 第3句，故事，售卖原因--通用文案
        third_list = self._open_file_by_sep(self.data_dir / r'01通用文案\03_故事.txt', sep='\n\n')
        choice_item = random.choice(third_list)
        self.choice_items.append('\n' + choice_item)

        # 第4句，硬件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\05_参数_硬件.txt', sep='\n\n')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第6句，硬件参数，分割符分割
        fourth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\06_参数_软件.txt', sep='\n\n')
        choice_item = random.choice(fourth_list)
        self.choice_items.append(choice_item)

        # 第7句，售后，分割符分割
        fifth_list = self._open_file_by_sep(self.data_dir / r'好好学习_文案\09_售后.txt', sep='\n\n')
        choice_item = random.choice(fifth_list)
        self.choice_items.append(choice_item)

        return self.choice_items

    # def __str__(self):
    #     # return '\n'.join(['\n' + element if '【' in element else element for element in self.choice_items])
    #     # return '\n\n'.join(self.choice_items)
    #     # 1. 清洗数据：创建一个新的列表，移除每个元素首尾的空白字符（包括换行符）
    #     #    这是一个非常重要的预处理步骤，能避免很多意外情况。
    #     items = [item.strip() for item in self.choice_items if item.strip()]
    #
    #     # 处理边界情况
    #     if not items:
    #         return ""
    #
    #     # 2. 拼接逻辑 (使用我们之前更简洁的“向前看”方案)
    #     # 第一个元素总是直接添加
    #     result = [items[0]]
    #
    #     # 从第二个元素开始遍历
    #     for i in range(1, len(items)):
    #         prev_element = items[i - 1]  # 前一个元素
    #         current_element = items[i]  # 当前元素
    #
    #         # 如果前一个元素是标题，并且当前元素不是标题，则直接用一个空格连接
    #         # 为什么是空格？因为标题【...】和正文之间通常需要一个空格来断开
    #         if '【' in prev_element and '【' not in current_element:
    #             result.append(' ' + current_element)
    #         # 其他所有情况，都用两个换行符（一个空行）隔开
    #         else:
    #             result.append('\n\n' + current_element)
    #
    #     # 3. 用空字符串把所有部分连接起来
    #     return "".join(result)


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

