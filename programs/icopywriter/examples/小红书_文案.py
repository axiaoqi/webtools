try:
    from icopywriter.xiaohongshu import XiaohongshuCopywritingGenerator
except ModuleNotFoundError:
    import os
    import sys
    curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(curPath)
    from icopywriter.xiaohongshu import XiaohongshuCopywritingGenerator


from settings import SynologyDrive

data_dir = SynologyDrive / r'01新项目记录\禅修项目\01_文案收集\苏州禅修\文案样式1'


def run():
    xhs = XiaohongshuCopywritingGenerator(data_dir)
    xhs.run()
    return xhs


if __name__ == '__main__':
    print(run())

