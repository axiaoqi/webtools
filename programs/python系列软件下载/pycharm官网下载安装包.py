import json
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup

from programs.utils.download_file import download_file

# 所有版本
# url = 'https://data.services.jetbrains.com/products?code=PCP%2CPCC&release.type=release&_=1731772'
# 社区版所有的
url = 'https://data.services.jetbrains.com/products?code=PCC&release.type=release'
# 专业版所有的
# url = 'https://data.services.jetbrains.com/products?code=PCP&release.type=release'

resp = requests.get(url)

data = json.loads(resp.text)[0]

# 提取所有 .exe 文件的链接
download_file_urls = []

# # 遍历 releases 数据，提取 downloads 字段中的 .exe 文件链接
# for release in data['releases']:
#     downloads = release['downloads']
#     for key, value in downloads.items():
#         if 'exe' in value['link'] and '-aarch64' not in value['link']:  # 排除包含 '-aarch64' 的链接
#             file_links.append(value['link'])

# # 遍历 releases 数据，提取 downloads 字段中的 macM1 链接
# for release in data['releases']:
#     downloads = release['downloads']
#     # 只提取 macM1 相关的下载链接
#     if 'macM1' in downloads:
#         file_links.append(downloads['macM1']['link'])

# 遍历 releases 数据，提取 downloads 字段中的 mac 下载链接
for release in data['releases']:
    downloads = release['downloads']
    # 只提取 mac 相关的下载链接
    if 'mac' in downloads:
        download_file_urls.append(downloads['mac']['link'])

print(download_file_urls)
print(len(download_file_urls))

# 下载文件
file_dir = Path.home() / r'Downloads\pycharm安装包【mac版intel芯片】'
if not file_dir.exists():
    file_dir.mkdir()

# 下载文件
for download_file_url in download_file_urls:
    print(download_file_url)
    file_name = download_file_url.split('/')[-1]
    file_path = file_dir / file_name

    if not file_path.exists():
        download_file(url=download_file_url, file_path=file_path)
    else:
        print(f'{file_path}文件已经存在！')



