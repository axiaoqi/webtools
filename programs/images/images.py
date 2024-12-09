"""
功能1：从多个文件夹选取n张图片到目标文件夹
功能2：从多个文件夹读取所有的图片，复制到目标文件夹当主图
"""
import random
from pathlib import Path
import shutil
from typing import List


def copy_random_images(n, folder_paths, target_folder, image_name=None):
    """
    功能1：从多个文件夹随机选取n张图片到目标文件夹
    批量填充2图，尾图
    """
    all_images = []

    if not isinstance(folder_paths, list):
        folder_paths = [folder_paths]

    # 遍历每个文件夹
    for folder in folder_paths:
        # 获取文件夹中的所有图片文件
        images = list(folder.glob('*.*'))  # 获取所有文件
        images = [img for img in images if img.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']]
        all_images.extend(images)

    # 检查是否有足够的图片可供选择
    if n > len(all_images):
        raise ValueError(f"可用图片数量不足。共有 {len(all_images)} 张图片，但要求选择 {n} 张。")

    # 随机选择 n 个图片
    selected_images = random.sample(all_images, n)

    # 创建目标文件夹（如果不存在）
    target_path = Path(target_folder)
    target_path.mkdir(parents=True, exist_ok=True)

    # 复制一张图时候，可以自己命名
    if n == 1:
        if image_name is None:  # 不自己命名，就保持默认
            shutil.copy2(selected_images[0], target_path)
        else:  # 自己命名就保留原来的扩展名
            shutil.copy2(selected_images[0], target_path / (image_name + selected_images[0].suffix))
        print(f"已复制 {selected_images[0]} 到 {target_folder}")
    else:
        # 复制每张图片到目标文件夹
        for image in selected_images:
            shutil.copy2(image, target_path)
            print(f"已复制 {image} 到 {target_folder}")


def copy_image_to_folders(folder_paths, target_folder, image_name=None):
    """
    功能2：从多个文件夹读取所有的图片，复制到目标文件夹当主图，一张图片
    用来批量生成主图的
    """
    dst_folders = []

    if not isinstance(folder_paths, list):
        folder_paths = [folder_paths]

    # 初始化计数器
    folder_counter = 1

    # 遍历源文件夹列表
    for folder in folder_paths:
        # 遍历当前源文件夹及其子文件夹中的所有文件
        for image_file in folder.rglob('*'):
            if image_file.is_file() and image_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
                # 生成按编号命名的目标文件夹
                dst_folder = target_folder / f'{folder_counter:02d}'
                dst_folder.mkdir(parents=True, exist_ok=True)
                dst_folders.append(dst_folder)  # 目标文件夹列表

                # 复制图片到目标文件夹
                if image_name is None:
                    dst_file_path = dst_folder / image_file.name  # 不自定义名字
                else:
                    dst_file_path = dst_folder / (image_name + image_file.suffix)  # 自定义名字

                shutil.copy2(image_file, dst_file_path)
                print(f"图片 {image_file.name} 已复制到文件夹 {dst_folder}")

                # 增加计数器
                folder_counter += 1
    return dst_folders


def copy_images_must_and_other(must_select_folders: List[Path], other_folders: List[Path], target_folder: Path, total_images=8):
    # 存储选择的图片路径
    selected_images = []

    # 定义支持的图片扩展名
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    # 从必选文件夹中随机选择一个图片
    for folder in must_select_folders:
        folder_path = Path(folder)
        image_files = [f for f in folder_path.glob('*') if f.suffix.lower() in valid_extensions]  # 过滤图片扩展名
        if image_files:
            selected_images.append(random.choice(image_files))

    # 计算还需要从其他文件夹选择的图片数量
    remaining_images_count = total_images - len(selected_images)

    # 从其他文件夹中随机选择图片，直到补充到总共 8 张图片
    other_selected_images = []

    if remaining_images_count > 0:
        # 如果其他文件夹数量不足，随机选取一些文件夹
        random_other_folders = random.sample(other_folders, min(remaining_images_count, len(other_folders)))
        for folder in random_other_folders:
            folder_path = Path(folder)
            image_files = [f for f in folder_path.glob('*') if f.suffix.lower() in valid_extensions]  # 过滤图片扩展名
            if image_files:
                other_selected_images.append(random.choice(image_files))

    # 合并所有选择的图片
    all_selected_images = selected_images + other_selected_images

    # 如果图片总数不足 8 张，继续从已选的文件夹中补充
    while len(all_selected_images) < total_images:
        all_selected_images.append(random.choice(all_selected_images))  # 随机重复已有的图片

    # 复制图片到目标文件夹
    for img in all_selected_images:
        shutil.copy(img, target_folder)

    print(f"成功复制了 {len(all_selected_images)} 张图片到 {target_folder}")
