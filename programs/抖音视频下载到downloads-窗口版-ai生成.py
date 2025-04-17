import pathlib
import re
import time

import requests
import tkinter as tk  # 新增tkinter导入
from tkinter import messagebox  # 新增messagebox导入

from tqdm import tqdm

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
    # 创建GUI窗口
    root = tk.Tk()
    root.title("抖音视频下载器")
    root.geometry("500x100")

    # URL输入框
    lbl = tk.Label(root, text="请输入抖音分享口令:")
    lbl.pack(pady=5)

    entry = tk.Entry(root, width=60)
    entry.pack(pady=5)

    def on_download():
        """ 下载按钮点击事件 """
        koulin = entry.get().strip()  # 获取输入内容
        if not koulin:
            messagebox.showerror("错误", "请输入抖音分享口令！")
            return
        try:
            dy_downloader(koulin)
            messagebox.showinfo("成功", "视频下载完成！")
        except Exception as e:
            messagebox.showerror("错误", f"下载失败：{str(e)}")

    # 下载按钮
    download_btn = tk.Button(root, text="下载", command=on_download)
    download_btn.pack(pady=5)

    root.mainloop()