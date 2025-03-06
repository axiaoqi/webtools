from pathlib import Path
import hashlib
from collections import defaultdict
from programs.settings import SynologyDrive


def calculate_hash(file_path, hash_algo=hashlib.md5):
    """计算文件的哈希值"""
    hash_func = hash_algo()
    with file_path.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def find_duplicate_images(folder_paths):
    """查找重复的图片"""
    hash_dict = defaultdict(list)

    for folder_path in folder_paths:
        folder = Path(folder_path)
        for file_path in folder.rglob('*'):
            if file_path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}:
                file_hash = calculate_hash(file_path)
                hash_dict[file_hash].append(file_path)

    # 筛选出有重复文件的哈希值
    duplicates = {hash_value: paths for hash_value, paths in hash_dict.items() if len(paths) > 1}
    return duplicates


def delete_selected_duplicates(duplicates):
    """删除用户选择的重复图片"""
    for hash_value, paths in duplicates.items():
        print(f"\n以下图片文件是重复的 (哈希值: {hash_value}):")
        for index, path in enumerate(paths, start=1):  # 编号从 1 开始
            print(f"[{index}] {path}")

        # 选择要删除的文件
        to_delete = input("输入要删除的文件编号（用逗号分隔多个编号）或按 Enter 跳过删除: ")
        if to_delete:
            indices = map(int, to_delete.split(','))
            for index in indices:
                paths[index - 1].unlink()  # 使用 index-1 访问列表
                print(f"已删除: {paths[index - 1]}")


if __name__ == "__main__":

    folders = [
        # SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\01主图'
        # r'C:\Users\e5\Desktop\新建文件夹',
        # r'C:\Users\e5\SynologyDrive\01新项目记录\闲鱼项目\AI学习机\00_学习机原图\源文件\闲鱼主图-花花'
        # r'D:\SynologyDrive\01新项目记录\02_AI学习机\02图片\09素材',
        # r'D:\SynologyDrive\01新项目记录\02_AI学习机\02图片\09素材\01主图_无水印'
        '/Volumes/disk3/SynologyDrive/01新项目记录/02_AI学习机/02图片/09素材/01主图_无水印'

    ]

    # 查找重复的图片
    duplicates = find_duplicate_images(folders)

    if duplicates:
        # 显示重复图片并选择删除
        delete_selected_duplicates(duplicates)
    else:
        print("未找到重复的图片。")
