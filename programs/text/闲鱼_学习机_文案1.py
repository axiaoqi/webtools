from programs.text.xianyu_text import XianyuTextGenerator, XianyuImgTxt, generate_price
from programs.settings import xuexiji_dir


def run():
    img_txt_path = xuexiji_dir / r'01文案\图片内容'
    data_dir = xuexiji_dir / r'01文案\文案素材1'

    all_str = []

    """
    价格
    """
    price_str = f'价格：{generate_price(intervals=[(310, 370)])}元\n'
    all_str.append(price_str)

    """
    图片文案
    """
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

    all_str.append(str(xianyuimg))

    """
    咸鱼AI学习机
    """
    xianyu = XianyuTextGenerator(data_dir)
    xianyu.run()  # start=4, end=7
    all_str.append(str(xianyu))
    return '\n'.join(all_str)


if __name__ == '__main__':
    while True:
        print(run())
        print('\n')
        input("按 Enter 键运行一次，或 Ctrl+C 退出: ")
        print('\n')


