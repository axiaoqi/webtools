from pathlib import Path
import shutil
import math


def distribute_images_1(src_path: Path, base_dest_folder):
    # 收集所有图片文件
    image_files = []
    for subfolder in src_path.iterdir():
        if subfolder.is_dir():
            for file in subfolder.iterdir():
                if file.is_file() and file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}:
                    image_files.append(file)

    # 如果没有图片，退出
    if not image_files:
        print("源文件夹没有图片文件")
        return

    # 计算需要的目标文件夹数量
    num_folders = len(image_files)

    # 创建目标文件夹
    dest_folders = []
    for i in range(num_folders):
        dest_folder = Path(base_dest_folder) / f'folder_{i + 1}'
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_folders.append(dest_folder)

    # 将图片分配到目标文件夹
    for i, image_file in enumerate(image_files):
        dest_folder = dest_folders[i % num_folders]
        dest_file = dest_folder / image_file.name
        shutil.copy(image_file, dest_file)
        print(f'复制 {image_file} 到 {dest_file}')


# 示例使用
src_folder = Path('path/to/source_folder')
base_dest_folder = 'path/to/destination_base_folder'
distribute_images_1(src_folder, base_dest_folder)
