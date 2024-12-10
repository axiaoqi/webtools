from pathlib import Path
from typing import Union


def count_images_in_folder(folder_path: Union[str, Path]):
    # 定义支持的图片扩展名
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    # 将路径转为Path对象
    if not isinstance(folder_path, Path):
        folder_path = Path(folder_path)

    # 用来存储每个文件夹及子文件夹的图片数量
    folder_image_count = {}

    # 遍历文件夹及其所有子文件夹
    for folder in folder_path.rglob('*'):
        # 只处理文件夹
        if folder.is_dir():
            # 统计该文件夹中符合扩展名的图片文件数量
            image_count = sum(1 for file in folder.glob('*') if file.suffix.lower() in valid_extensions)
            if image_count > 0:
                folder_image_count[folder] = image_count

    # 输出结果
    for folder, count in folder_image_count.items():
        print(f"文件夹: {folder} -> 图片数量: {count}")

    return folder_image_count


if __name__ == '__main__':
    count_images_in_folder(r'D:\SynologyDrive\01新项目记录\02_AI学习机\02图片\02花花家图片')
