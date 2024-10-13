import datetime
import os
import random
import re
import time
from pathlib import Path
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}


def get_response(url, timeout=60, retries=5):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            return response
        except requests.exceptions.RequestException as e:
            print(f"尝试 {i + 1} 失败: {e}")
            if i == retries - 1:
                return None  # 重试结束，返回 None


def get_file_respnse(url, timeout=60, retries=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            return response
        except requests.exceptions.RequestException as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt == retries - 1:
                return None  # 重试结束，返回 None


def download_file(url, file_path, max_duration=1200, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            start_time = time.time()

            response = get_file_respnse(url)
            total_size = int(response.headers.get('content-length', 0))

            with open(file_path, "wb") as file:
                with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                    for data in response.iter_content(chunk_size=1024):
                        if time.time() - start_time > max_duration:
                            print("下载超时！")
                            break
                        file.write(data)
                        pbar.update(len(data))
            break
        except Exception as e:
            print(f'下载中断，正在第{retries+1}次重试: {e}')
        retries += 1
        time.sleep(5)  # Wait for 5 seconds before retrying
    if retries == max_retries:
        print('重试次数过多，下载失败')


def download_a_url(file_dir: Path, data_list: List[Dict], app_value, dir_id_value):
    """
    下载文件
    :param file_dir: 文件保存路径
    :param data_list: 爬虫获取的文件名和id的列表
    :param app_value:
    :param dir_id_value:
    :return:
    """
    base_file_url = 'https://pan.tpym.cn/s/baidu_filedown?app={}&dir_id={}&id={}&down_psw='

    # 输出结果
    for item in data_list:
        print( '\n' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        file_path = file_dir / item.get('data-clipboard-text')[1:]
        file_path.parent.mkdir(parents=True, exist_ok=True)

        download_url = base_file_url.format(app_value, dir_id_value, item.get('js_downfile'))

        print(str(file_path) + '：' + download_url)

        if not file_path.exists():  # 文件不存在，则去下载
            download_file(url=download_url, file_path=file_path)
        elif file_path.exists and file_path.stat().st_size < 436:  #
            download_file(url=download_url, file_path=file_path)
            print(f'被覆盖：已存在：{file_path}')
        else:
            print(f'已存在：{file_path}')
    print(f'完成{len(data_list)}条下载')


def get_file_and_dir_url(url):  # 'https://pan.tpym.cn/s?app=1533906244&dir_id=4674'

    # 使用正则表达式提取app和dir_id的值
    app_match = re.search(r'app=(\d+)', url)
    dir_id_match = re.search(r'dir_id=(\d+)', url)

    app_value = app_match.group(1) if app_match else None
    dir_id_value = dir_id_match.group(1) if dir_id_match else None

    resp = get_response(url=url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 提取所有ul标签
    ul_tags = soup.find_all(attrs={'class': 'am-list am-list-static'})[0]
    # 提取所有li标签
    li_tags = ul_tags.find_all('li')

    # 创建一个字典存储当前项的信息
    dir_url_list = []
    file_data_list = []

    for li in li_tags:

        dir_app_div = li.find(class_="base-icon dir-app-small")
        if not dir_app_div:  # 获取文件
            item = {}  # 创建一个字典存储当前项的信息

            # 提取onclick的值，使用正则表达式提取ID
            onclick_div = li.find('div', onclick=True)
            if onclick_div:
                onclick_value = onclick_div['onclick']
                match = re.search(r"js_downfile\('(\d+)'\)", onclick_value)
                if match:
                    item['js_downfile'] = match.group(1)  # 提取文件ID

            # 提取data-clipboard-text的值
            copy_btn = li.find('div', id='copyBtn')
            if copy_btn:
                item['data-clipboard-text'] = copy_btn['data-clipboard-text']

            # 仅在item有数据时加入列表
            if item:
                file_data_list.append(item)
        else:
            dir_url = li.find('a').get('href')  # 获取文件夹
            dir_url_list.append('https://pan.tpym.cn/' + dir_url)

    return dir_url_list, file_data_list, app_value, dir_id_value


def continue_download(file_dir, dir_url_list):
    # dir_url 列表
    __dir_url_list = []

    for _url in dir_url_list:
        _dir_url_list, _file_data_list, _app_value, _dir_id_value = get_file_and_dir_url(_url)
        __dir_url_list.extend(_dir_url_list)

        # 下载文件
        if len(_file_data_list) > 0:
            download_a_url(file_dir=file_dir, data_list=_file_data_list, app_value=_app_value, dir_id_value=_dir_id_value)

    # 循环获取文件夹链接
    return __dir_url_list


def run(url, file_dir):
    if not isinstance(file_dir, Path):
        file_dir = Path(file_dir)

    # 第一层
    dir_url_list, file_data_list, app_value, dir_id_value = get_file_and_dir_url(url)

    # 下载文件
    if len(file_data_list) > 0:
        download_a_url(file_dir=file_dir, data_list=file_data_list, app_value=app_value, dir_id_value=dir_id_value)
    else:
        print(f'此链接没有需要下载的文件：{url}')

    if len(dir_url_list) > 0:
        # 循环文件夹(第二层)
        dir_url_list_2 = continue_download(file_dir, dir_url_list)

        if len(dir_url_list_2) > 0:
            dir_url_list_3 = continue_download(file_dir, dir_url_list=dir_url_list_2)

            if len(dir_url_list_3) > 0:
                dir_url_list_4 = continue_download(file_dir, dir_url_list=dir_url_list_3)

                if len(dir_url_list_4) > 0:
                    dir_url_list_5 = continue_download(file_dir, dir_url_list=dir_url_list_4)

                    if len(dir_url_list_5) > 0:
                        dir_url_list_6 = continue_download(file_dir, dir_url_list=dir_url_list_5)

                        if len(dir_url_list_6) > 0:
                            dir_url_list_7 = continue_download(file_dir, dir_url_list=dir_url_list_6)

                            if len(dir_url_list_7) > 0:
                                dir_url_list_8 = continue_download(file_dir, dir_url_list=dir_url_list_7)

                                if len(dir_url_list_8) > 0:
                                    dir_url_list_9 = continue_download(file_dir, dir_url_list=dir_url_list_8)

                                    if len(dir_url_list_9) > 0:
                                        dir_url_list_10 = continue_download(file_dir, dir_url_list=dir_url_list_9)

                                        if len(dir_url_list_10) > 0:
                                            dir_url_list_11 = continue_download(file_dir, dir_url_list=dir_url_list_10)

                                            if len(dir_url_list_11) > 0:
                                                print('还没下载完成')

    else:
        print('下载完成了')


if __name__ == '__main__':
    # file_dir = Path.home() / 'Desktop' / '直播间资料'
    # url = 'https://pan.tpym.cn/s?app=1533906244&dir_id=4676&path=%2F15%E5%8F%B7%E8%B5%84%E6%96%99'
    #
    # run(url=url, file_dir=file_dir)


    # file_path = Path(r'C:\Users\e5\Desktop\【小学数学】四年级下册预习卡（西师版）.pdf')
    # url = 'https://pan.tpym.cn/s/baidu_filedown?app=1533906244&dir_id=4692&id=301002051005717&down_psw='
    # download_file(url=url, file_path=file_path)
    while True:
        url = input('请输入需要下载的链接：')
        file_dir = input('请输入文件保存路径：') or r'C:\Users\e5\Desktop\小初资料\小学资料'
        run(url=url, file_dir=file_dir)