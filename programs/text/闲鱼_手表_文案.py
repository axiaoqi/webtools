import random
from pathlib import Path


try:
    from wenan.icopywriter import CopywritingGenerator
except ModuleNotFoundError:
    import os
    import sys
    curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(curPath)
    from wenan.icopywriter import CopywritingGenerator


class XianYuWatch(CopywritingGenerator):
    def __init__(self,
                 biaoti: Path,
                 huazhongdian: Path,
                 zhenshipeizhi: Path,
                 shiyongrenqun: Path,
                 youdian: Path,
                 quedian: Path,
                 shouhou: Path,
                 ):
        super().__init__()

        self.biaoti = biaoti
        self.huazhongdian = huazhongdian
        self.zhenshipeizhi = zhenshipeizhi
        self.shiyongrenqun = shiyongrenqun
        self.youdian = youdian
        self.quedian = quedian
        self.shouhou = shouhou

        self.data = []  # 选择出来的文案输出的结果

    def _biaoti(self):
        data = self._open_file(self.biaoti)
        self.data.append(random.choice(data))

    def _huazhongdian(self):
        data = self._open_file_by_sep(self.huazhongdian, '/////')
        self.data.append(random.choice(data))

    def _zhenshipeizhi(self):
        data = self._open_file_by_sep(self.zhenshipeizhi, '/////')
        self.data.append(random.choice(data))

    def _shiyongrenqun(self):
        data = self._open_file_by_sep(self.shiyongrenqun, '/////')
        self.data.append(random.choice(data))

    def _youdian(self):
        data = self._open_file_by_sep(self.youdian, '/////')
        self.data.append(random.choice(data))

    def _quedian(self):
        data = self._open_file_by_sep(self.quedian, '/////')
        self.data.append(random.choice(data))

    def _shouhou(self):
        data = self._open_file_by_sep(self.shouhou, '/////')
        self.data.append(random.choice(data))

    def run(self):

        # 标题
        self._biaoti()

        # 划重点
        self._huazhongdian()

        # 真实配置
        self._zhenshipeizhi()

        # 适用人群
        self._shiyongrenqun()

        # 优点
        self._youdian()

        # 缺点
        self._quedian()

        # 售后
        self._shouhou()

    def __str__(self):
        return '\n\n'.join(item.strip('\n') for item in self.data)


def run_cd100():

    from settings import SynologyDrive

    file_path_str = r'01新项目记录\咸鱼项目\华强北手表\01文案'
    abs_file_path = SynologyDrive / file_path_str

    watch = XianYuWatch(
        biaoti=abs_file_path / 'CD100_标题.txt',
        huazhongdian=abs_file_path / 'CD100_划重点.txt',
        zhenshipeizhi=abs_file_path / 'CD100_真实配置.txt',
        shiyongrenqun=abs_file_path / '适用人群.txt',
        youdian=abs_file_path / 'CD100_优点.txt',
        quedian=abs_file_path / 'CD100_缺点.txt',
        shouhou=abs_file_path / '售后.txt',
    )
    watch.run()
    print(watch)


if __name__ == '__main__':
    while True:
        run_cd100()
        print('\n')
        input("按 Enter 键运行一次，或 Ctrl+C 退出: ")
        print('\n')
