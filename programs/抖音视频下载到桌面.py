import pathlib
import re

import requests

file_fir = pathlib.Path.home() / 'Desktop'


def dy_downloader(koulin):
    # 第一步，组合网站的url和抖音的url
    # 正则表达式匹配抖音标准分享链接
    pattern = r'https://v\.douyin\.com/[\w\/-]+/?'
    url = re.findall(pattern, koulin)[0]
    base_url = f'https://dlpanda.com/zh-CN?url={url}&token=G7eRpMaa'
    # 正则表达式（包含话题标签）
    pattern = r'\d{2}/\d{2}\s+((?:.(?!\s+https?://))+)'
    match = re.search(pattern, koulin, re.DOTALL)
    video_name = match.group(1).strip() if match else None

    # 获取下载地址
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
    resp = requests.get(base_url, headers=headers).text
    pattern = r'window\.location\.href\s*=\s*["\'](.*?)["\']'
    match = re.search(pattern, resp)
    if match:
        video_download_url = "http:" + match.group(1)
        print(video_download_url)  # 输出提取的URL
    else:
        print("未找到匹配的URL")


    # 下载文件



if __name__ == '__main__':
    kl = '5.61 z@g.Bt reo:/ 02/28 延时摄影25分钟，带你欣赏流动的云彩# 蓝蓝的天空白云飘# 蓝天白云绿草地  https://v.douyin.com/zyp2peR0Ju0/ 复制此链接，打开Dou音搜索，直接观看视频！'
    dy_downloader(kl)