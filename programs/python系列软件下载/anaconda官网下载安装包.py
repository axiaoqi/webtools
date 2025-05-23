import re
import requests

from pathlib import Path
from programs.utils.download_file import download_file


def update_anaconda(computer_system, file_dir):

    url = 'https://repo.anaconda.com/archive/'
    # url = 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/'  # 清华源

    resp = requests.get(url)

    if computer_system == 'windows':
        # 正则表达式匹配 Windows-x86_64.exe 后缀的文件
        pattern = r'href="([^"]*Windows-x86_64\.exe)"'
        file_dir = file_dir / 'anaconda安装包【windows版】'
    elif computer_system == 'mac_intel':
        # MacOS，intel芯片的，MacOSX-x86_64.pkg
        pattern = r'href="([^"]*MacOSX-x86_64.pkg)"'
        file_dir = file_dir / 'anaconda安装包【mac版intel芯片】'
    elif computer_system == 'mac_m':
        # MacOS，M系列芯片的，MacOSX-x86_64.pkg
        pattern = r'href="([^"]*MacOSX-arm64.pkg)"'
        file_dir = file_dir / 'anaconda安装包【mac版m芯片】'
    else:
        print('电脑系统填错了！')

    if not file_dir.exists():
        file_dir.mkdir()

    # 查找所有匹配的文件名
    file_names = re.findall(pattern, resp.text)

    download_file_urls = [url + file_name for file_name in file_names]

    print(download_file_urls)
    print(len(download_file_urls))

    # 下载文件
    for download_file_url in download_file_urls:
        print(download_file_url)
        file_name = download_file_url.split('/')[-1]
        file_path = file_dir / file_name

        if not file_path.exists():
            download_file(url=download_file_url, file_path=file_path)
        else:
            print(f'{file_path}文件已经存在！')


