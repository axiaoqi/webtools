import pathlib
import re
import requests

from programs.utils.download_file import download_file


file_fir = pathlib.Path.home() / 'Downloads'


def extract_name(koulin):
    """
    取出视频名称
    """
    # 分割出https之前的部分
    first_part = koulin.split('https')[0].strip()

    pattern = r"[#\u4e00-\u9fa5].*"  # 匹配第一个 `#` 或中文字符及其后的所有内容
    match = re.search(pattern, first_part)
    name = match.group()

    # 名字特殊字符用空格替换
    name = name.replace('|', ' ') if name else None
    return name


def dy_downloader(koulin):
    # 第一步，组合网站的url和抖音的url
    # 正则表达式匹配抖音标准分享链接
    pattern = r'https://v\.douyin\.com/[\w\/-]+/?'
    url = re.findall(pattern, koulin)[0]
    base_url = f'https://dlpanda.com/zh-CN?url={url}&token=G7eRpMaa'

    # 正则表达式（包含话题标签）
    video_name = extract_name(koulin)

    # 获取下载地址
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
    resp = requests.get(base_url, headers=headers).text
    pattern = r'window\.location\.href\s*=\s*["\'](.*?)["\']'
    match = re.search(pattern, resp)
    if match:
        video_download_url = "http:" + match.group(1)
        print(video_download_url)  # 输出提取的URL

        # 下载文件
        file_path = file_fir / (video_name+'.mp4')
        print(file_path)
        download_file(url=video_download_url, file_path=file_path)
    else:
        print("未找到匹配的URL")


if __name__ == '__main__':
    kl = input("输入抖音分享口令：")
    # name = extract_name(kl)
    # print(name)
    dy_downloader(kl)
