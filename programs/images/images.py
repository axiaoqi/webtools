"""
功能1：从多个文件夹选取n张图片到目标文件夹
功能2：从多个文件夹读取所有的图片，复制到目标文件夹当主图
"""
import random
from pathlib import Path
import shutil


def copy_random_images(n, folder_paths, target_folder):
    """
    功能1：从多个文件夹选取n张图片到目标文件夹
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

    if n == 1:
        shutil.copy2(selected_images[0], target_path)
        print(f"已复制 {selected_images[0]} 到 {target_folder}")
    else:
        # 复制每张图片到目标文件夹
        for image in selected_images:
            shutil.copy2(image, target_path)
            print(f"已复制 {image} 到 {target_folder}")


def copy_image_to_folders(folder_paths, target_folder):
    """
    功能2：从多个文件夹读取所有的图片，复制到目标文件夹当主图
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
                dst_file_path = dst_folder / image_file.name
                shutil.copy2(image_file, dst_file_path)
                print(f"图片 {image_file.name} 已复制到文件夹 {dst_folder}")

                # 增加计数器
                folder_counter += 1
    return dst_folders


if __name__ == '__main__':
    from programs.settings import SynologyDrive

    white_primary = SynologyDrive / r'01新项目记录\咸鱼项目\AI学习机\白色主图收集'
    black_primary = SynologyDrive / r'01新项目记录\咸鱼项目\AI学习机\黑色主图收集'
    destination = Path.home() / 'Desktop'  # 目的地路径

    dst_folders = copy_image_to_folders(
        folder_paths=[white_primary, black_primary],
        target_folder=destination
    )
    print(dst_folders)