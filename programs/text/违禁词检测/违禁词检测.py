import re
import os


# 获取指定文件夹中的所有违禁词文件
def load_banned_words(file_name):
    folder_path = os.path.join(os.getcwd(), "programs/text/违禁词检测/banned_txt")  # 获取 banned_txt 文件夹的路径
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
