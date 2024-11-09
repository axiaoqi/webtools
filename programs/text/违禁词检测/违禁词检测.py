import re
import os
import sys
from pathlib import Path


# 获取指定文件夹中的所有违禁词文件
def load_banned_words(file_name):
    # 获取违禁词文件夹的路径
    # 先获取群晖文件夹的路径，这里根据自己的文件位置去改
    SynologyDrive = Path.home() / 'SynologyDrive'
    if not SynologyDrive.exists():
        SynologyDrive = Path('D:\SynologyDrive')
    # 文件位置
    folder_path = SynologyDrive / "01新项目记录/Z违禁词"  # 获取违禁词 文件夹的路径
    file_path = os.path.join(folder_path, file_name)  # 拼接文件路径

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            banned_words = [line.strip() for line in f.readlines()]
        return banned_words
    except FileNotFoundError:
        return []


# 检查文本中的违禁词，并将违禁词标红
def check_for_banned_words(text, banned_words):
    for word in banned_words:
        # 用正则替换违禁词为带有红色标记的词
        text = re.sub(r'(' + re.escape(word) + r')', r'<span style="color:red">\1</span>', text)
    return text
