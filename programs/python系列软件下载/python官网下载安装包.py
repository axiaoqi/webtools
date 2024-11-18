import os
import re
from pathlib import Path

import requests
from lxml import etree

from programs.utils.download_file import download_file


# 定义一个函数用来比较版本号
def compare_versions(v1, v2):
    # 使用正则表达式提取版本号中的数字部分
    v1_parts = [int(x) for x in re.findall(r'\d+', v1)]
    v2_parts = [int(x) for x in re.findall(r'\d+', v2)]

    # 对比版本号
    return v1_parts >= v2_parts


def update_python(computer_system, file_dir):
    # url = 'https://www.python.org/ftp/python/'
    url = 'https://repo.huaweicloud.com/python/'  # 华为镜像

    # 取出所有的链接
    resp = requests.get(url)
    # 解析 HTML 内容
    tree = etree.HTML(resp.text)
    # 使用 XPath 提取所有 <a> 标签中的文本内容
    links = tree.xpath('//a/text()')
    # 取出版本号
    links = [link.rstrip('/') for link in links if re.match(r'^\d', link)]

    # 过滤出版本号大于或等于 '3.5'
    result = [link for link in links if link.startswith('3.') and compare_versions(link, '3.6.')]

    if computer_system == 'windows':
        # windows
        download_urls = [url + link + '/' + 'python-' + link + '-amd64.exe' for link in result]
        file_dir = file_dir / 'Python安装包【windows版】'
    elif computer_system == 'mac':
        # macOS11
        download_urls = [url + link + '/' + 'python-' + link + '-macos11.pkg' for link in result]
        file_dir = file_dir / 'Python安装包【mac版】'

    else:
        print('电脑系统填错了！')
        # macOS10.9
        # download_urls = [url + link + '/' + 'python-' + link + '-macosx10.9.pkg' for link in result]
        # macOS10.6
        # download_urls = [url + link + '/' + 'python-' + link + '-macosx10.6.pkg' for link in result]

    # 设置下载保存的文件夹路径
    download_folder = file_dir / 'Python安装包【windows版】'
    # 设置记录404错误链接的文件路径
    error_log_file = file_dir / "404_links.txt"

    # 如果目标文件夹不存在，创建它
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if len(download_urls) > 0:
        # 打开文件记录404错误链接
        with open(error_log_file, "a") as error_file:
            for url in download_urls:
                print(url)
                try:
                    # 发起GET请求
                    response = requests.get(url, stream=True)

                    # 检查状态码
                    if response.status_code == 200:
                        # 下载文件
                        file_name = url.split("/")[-1]
                        file_path = file_dir / file_name

                        if not file_path.exists():
                            download_file(url=url, file_path=file_path)
                        else:
                            print(f'{file_path}文件已经存在！')


                    elif response.status_code == 404:
                        # 记录404错误链接
                        error_file.write(url + "\n")
                        print(f"链接 {url} 返回404，已记录")

                    else:
                        print(f"链接 {url} 返回状态码 {response.status_code}，跳过下载")

                except requests.exceptions.RequestException as e:
                    print(f"下载文件时出错 {url}: {e}")


if __name__ == '__main__':
    pass