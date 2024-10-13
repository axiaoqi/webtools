import random
import time

import requests
from lxml import etree
from tqdm.auto import tqdm
from 下载pan_tpym_cn文件3_升级版 import get_file_and_dir_url

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


def get_url_list():
    url = 'https://pan.tpym.cn/'
    resp = get_response(url=url)

    tree = etree.HTML(resp.content)
    _hrefs = tree.xpath('/html/body/div[1]/div/main/div/div[6]/div/div/div[2]/a/@href')
    hrefs = ['https://pan.tpym.cn'+href for href in _hrefs]
    return hrefs


def run(url_file, retries=10):

    # 读取url文件列表
    txt_url_list = []
    with open(url_file, 'r') as file:
        for line in file:
            txt_url_list.append(line.strip())

    # 获取url列表
    add_url_list = []
    for i in tqdm(range(1, retries+1)):
        url_list = get_url_list()
        add_url_list.extend(url_list)
        time.sleep(5*random.random())

    # 新链接去重，
    new_add_url_list = list(dict.fromkeys(add_url_list))

    # 跟txt里面的对比去重，
    results = [url for url in new_add_url_list if url not in txt_url_list]

    # 然后追加写入到txt内
    with open(url_file, 'a') as file:
        # file.write('\n')
        for element in results:
            file.write(element + '\n')


# def check_url_available(url):
#     dir_url_list, file_data_list, app_value, dir_id_value = get_file_and_dir_url(url)
#     if len(file_data_list) > 0:
#         dir_url_list_1, _file_data_list_1, app_value_1, dir_id_value_1 = get_file_and_dir_url(dir_url_list[0])


if __name__ == '__main__':
    url_file = r'C:\Users\e5\Desktop\url.md'
    # url_file = input('输入url列表文件路径：') or r'C:\Users\e5\Desktop\url.md'
    run(url_file=url_file)

    txt_url_list = []
    with open(url_file, 'r') as file:
        for line in file:
            txt_url_list.append(line.strip())

    for i in txt_url_list:
        print(i)

    print(len(txt_url_list))

    a = list(dict.fromkeys(txt_url_list))
    print(a)
    print(len(list(dict.fromkeys(txt_url_list))))

    # check_url_available('https://pan.tpym.cn/s/519791006')
