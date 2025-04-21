import pathlib
import time

import requests
from lxml import etree
from tqdm import tqdm


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


file_fir = pathlib.Path.home() / 'Downloads'


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'cookie': '_ga=GA1.1.793506616.1744649776; __gads=ID=add244bfd7cb2e3b:T=1744649775:RT=1745252526:S=ALNI_Ma8PqbvnU3IEv81uFhQwCjyZKeiTw; __gpi=UID=0000109e1d5da5c7:T=1744649775:RT=1745252526:S=ALNI_MbVyD5APSEcZBLxwc7nXgFjGlXOiQ; __eoi=ID=4df8f435029d3fcd:T=1744649775:RT=1745252526:S=AA-AfjavYgiVMdyKSyJ4MtiOW3M-; XSRF-TOKEN=eyJpdiI6IjhIMTNpcWJEY1pPNTMxT3B1aXlCSnc9PSIsInZhbHVlIjoiTEMxQXZtK2lmb0lNeTQ5amtjaitQQ0EzOTF5YlpPY1A0RzJkM2N6TzQweVE1aTF2T3hZUVdDVVczOEFBQ2pZY2Y5bi8vMmU2dVovNlE1UnlLc2dkTS9MSXhpV1Qvd0V5b0xsWjk2Y2d0a3lHUUo5aWNqMldNY2NGTnhrT0hvU3MiLCJtYWMiOiI1YmFhMTY3NGQxNTNmNGViZjgyOWEzZTAyMWZjNWU0MmQ3YTE4NjlmZWExYzMzNDEzZDIwZmE3NDlkYTIxODc0IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6Im1SbWdxWXJEajNnZHhiZjZyV0FNUXc9PSIsInZhbHVlIjoiV2hYbkVrMmhYbFNBOW5ENXgyMXBEMUdXL1ZwaG51ZDAydldYZWV4UTErYXRSZ0xlOXhtSnp0UkhtRmhuKzJubDdJTHhRYmp1OVEzRlBTUVNlYkg5bFdaMlVUbXlPY20yeHVxY0xiWGgwdzEyd29KcVZhWFpsbnJBSVhGekMrcFMiLCJtYWMiOiI0MjhjMjdhNjk2NTc5ZTViOTM5ZmU5MDI5M2ZlN2NmYTZkNGE1NmQ1ZjU3YzU3YzEzODcyMzQwMmE2OTEyMGQ3IiwidGFnIjoiIn0%3D; FCOEC=%5B%5B%5B28%2C%22%5Bnull%2C%5Bnull%2C1%2C%5B1745252537%2C288674000%5D%5D%5D%22%5D%5D%5D; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B13%2C%22%5B%5C%22DBABL~BVQqAAAAAg%5C%22%2C%5B%5B7%2C%5B1745252533%2C186682000%5D%5D%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol-Gggi4oJPXb4cGvst_nTw1lx18Pb1WNgDeqCBkEebFe_QTBJbstgxnWRequoFrDVExB3GQCGeYFizO5D-1jq3dy5h-Fs4hhloWwXWI_9TRQR_bIyYrN3USmJvAFgP5-Myswb58HcblRdxorud7dGtKQm1SHQ%3D%3D%22%5D%2Cnull%2C%5B%5B2%2C%22%5Bnull%2C%5Bnull%2C1%2C%5B1745252537%2C288674000%5D%5D%5D%22%5D%5D%5D; _ga_MEHFNQTGNY=GS1.1.1745252525.3.1.1745252599.0.0.0'
}

base_url = 'https://douyinxz.com/kuaishou/'


if __name__ == '__main__':
    url = input('输入快手视频链接：')
    # url = 'https://www.kuaishou.com/short-video/3x3sf46sh54qtrc?authorId=3xyxdkksqu36yr6&streamSource=search&searchKey=%E8%BE%A3%E6%A4%92&area=searchxxnull'
    data = {
        '_token': '9hL3iIB1lDy4l8mHo77AlZXlchnhQLEKdpb1s2Px',
        'url': url
    }
    resp = requests.post(url=base_url, headers=headers, json=data)

    print(resp.text)

    # 获取名称\获取下载地址

    tree = etree.HTML(resp.text)
    download_url = tree.xpath('//video/@src')[0]
    file_name = tree.xpath('//h2/text()')[0]
    print(download_url)
    print(file_name)

    file_path = file_fir / (file_name + '.mp4')


    # 下载文件
    download_file(url=download_url, file_path=file_path)
