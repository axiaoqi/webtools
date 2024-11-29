"""
功能：
1、添加曲库，没有则添加进去，【后期可以自动添加】
2、从csv文件根据文件名提取：歌曲名、百度网盘下载链接、夸克网盘下载链接
"""
import os
import datetime
import re
import sys
from pathlib import Path

import pandas as pd

from programs.settings import SynologyDrive

music_data_dir = Path(r'Z:\music\A曲库')

# 各种格式的文件所在的文件，后期还可以添加
mp3_music_data_dir = music_data_dir / 'mp3'
flac_music_data_dir = music_data_dir / 'flac'

# 存储文件的链接数据（csv文件）
music_url_csv_file = SynologyDrive / 'music_url.csv'

columns = ['music_name', 'music_url_baidu', 'music_url_kuake',
           'update_timestamp']  # 音乐名，百度网盘分享链接，夸克网盘分享链接。后期可以写一个检测链接是否有效的函数


def get_music_file_path(music_name):
    music_name = '童话镇 - 陈一发儿.flac'
    music_format = os.path.splitext(music_name)[1][1:]  # 获取歌曲扩展名
    music_author = os.path.splitext(music_name)[0].split(' - ')[-1]  # 获取歌手名
    music_path = music_data_dir / music_format / music_author / music_name  # 获取歌曲的路径，可以用来发邮件

    return music_path


def init_music_url_csv_file():
    """
    初始化一个存储歌曲的分享链接的csv数据
    """
    df = pd.DataFrame(columns=columns)
    if not music_url_csv_file.exists():
        df.to_csv(music_url_csv_file, index=False)
        print('**********音乐数据库文件初始化成功**********')


def add_music_url(music_name, music_url_baidu, music_url_kuake):
    """
    把音乐添加到数据库中
    """
    # 初始化数据文件
    init_music_url_csv_file()

    # 打开文件
    df = pd.read_csv(music_url_csv_file)

    # 对比数据，添加不存在的数据,就是根据music_name判断
    if not df['music_name'].isin([music_name]).any():
        # 构建添加的数据
        add_data_list = [music_name, format_baidu_url(music_url_baidu), format_kuake_url(music_url_kuake), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        add_data_df = pd.DataFrame(data=[add_data_list], columns=columns)
        # 添加数据到文件内
        df = pd.concat([df, add_data_df], ignore_index=True)
        df.to_csv(music_url_csv_file, index=False, encoding='utf-8-sig')

        s = f'数据添加成功：{add_data_list}'
        return s
    else:
        exist_music_url_df = df[df['music_name'] == music_name]
        s = f'数据已经存在：\n{exist_music_url_df}'
        return s


def query_musics_url(music_names):
    """
    获取多首音乐的数据
    """
    if isinstance(music_names, str):
        music_names = [music_names]

    # 打开文件
    df = pd.read_csv(music_url_csv_file)

    # 查询数据，不存在的生成一个新的列表，返回
    existing_names_query_df = df[df['music_name'].isin(music_names)]
    # 提取不存在的名字
    non_existing_names = [name for name in music_names if name not in df['music_name'].values]

    existing_names_query_df = existing_names_query_df[['music_name', 'music_url_baidu', 'music_url_kuake']]
    return existing_names_query_df, non_existing_names


def format_baidu_url(baidu_url):
    """
    添加文件时候，格式化百度网盘连接数据
    百度网盘链接：
    """
    # 使用正则表达式提取链接和提取码
    pattern = r'链接：(https://pan.baidu.com/s/\S+)\s+提取码：(\S+)'
    match = re.search(pattern, baidu_url)

    # 提取链接和提取码
    link = match.group(1)
    code = match.group(2)

    # 构造新的文本格式
    result = f'百度网盘：链接：{link} 提取码：{code}'

    return result


def format_kuake_url(kuake_url):
    """
    添加文件时候，格式化夸克网盘连接数据
    夸克网盘链接：
    """
    # 使用正则表达式提取链接部分
    link_pattern = r"链接：(\S+)"
    match = re.search(link_pattern, kuake_url)
    # 提取到链接并格式化输出
    link = match.group(1)
    result = f"夸克网盘：链接：{link}"
    return result


if __name__ == '__main__':
    # _music_name = '童话镇 - 陈一发儿.flac'
    # # _music_url_baidu = '11'
    # # _music_url_kuake = '22'
    # # add_music_url(_music_name, _music_url_baidu, _music_url_kuake)
    # # print(query_musics_url(_music_name))
    #
    # baidu_url = input('输入百度网盘连接：')
    #
    # print('\n\n' + baidu_url)

    music_name = '童话镇 - 陈一发儿.flac'

    baidu_url = '''通过百度网盘分享的文件：爱情心法422.pdf
链接：https://pan.baidu.com/s/1E_KzQv5RStHxG3JSgsqT-w?pwd=8888 
提取码：8888 
--来自百度网盘超级会员V2的分享'''

    kuake_url = '''我用夸克网盘分享了「【抢鲜版】四语（上册）电子课本（新版）.pdf」，点击链接即可保存。打开「夸克APP」在线查看，支持多种文档格式转换。
链接：https://pan.quark.cn/s/18a0a852189d'''

    # print(format_baidu_url(baidu_url))
    # print(format_kuake_url(kuake_url))

    s = add_music_url(music_name, baidu_url, kuake_url)
    print(s)
