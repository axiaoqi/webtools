import time
import requests
from tqdm.auto import tqdm


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}


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