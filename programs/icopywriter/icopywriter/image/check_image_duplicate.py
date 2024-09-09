"""
判断这个图片，是不是已经存在这个文件夹里面

计算md5值，然后逐个对比
"""
import hashlib
from pathlib import Path


def get_image_hash(image_path):
    # 读取图片内容
    with open(image_path, 'rb') as f:
        data = f.read()

    # 计算SHA256哈希值
    return hashlib.sha256(data).hexdigest()


def get_all_files(file_dir: Path):
    """
    获取文件夹及子文件夹内所有的文件
    """
    return [p for p in file_dir.rglob('*') if p.is_file()]


