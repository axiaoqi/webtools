from pathlib import Path
try:
    from wenan import XianyuCopywritingGenerator, XianyuImgTxt, generate_price
except ModuleNotFoundError:
    import os
    import sys
    curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(curPath)
    from wenan import XianyuCopywritingGenerator, XianyuImgTxt, generate_price

from programs.wenan.examples.settings import SynologyDrive


def run():
    """
    价格
    """
    print(f'价格：{generate_price(intervals=[(310, 370)])}元\n')

    """
    图片文案
    """

    img_txt_path = SynologyDrive / r'01新项目记录\咸鱼项目\AI学习机\图片内容'
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
    data_dir = SynologyDrive / r'01新项目记录\咸鱼项目\AI学习机\文案素材'
    xianyu = XianyuCopywritingGenerator(data_dir)

    xianyu.run()  # start=4, end=7
    return xianyu


if __name__ == '__main__':
    while True:
        run()
        print('\n')
        input("按 Enter 键运行一次，或 Ctrl+C 退出: ")
        print('\n')


