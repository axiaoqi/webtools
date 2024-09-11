from pathlib import Path

from programs.images.images import copy_random_images, copy_image_to_folders


def run():
    from programs.settings import SynologyDrive

    primary_images_dir = [SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\01主图\网上找的',
                          SynologyDrive / r'D:\SynologyDrive\01新项目记录\闲鱼项目\AI学习机\02图片\01主图\自己拍的_右边']
    destination = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\00_学习机原图'  # 目的地路径

    # 首图
    target_folders = copy_image_to_folders(primary_images_dir, destination)
    print(target_folders)

    # 循环掺入其他图片
    for target_folder in target_folders:
        # 二图
        second_images_dir = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\02整体展示'
        copy_random_images(1, second_images_dir, target_folder)

        # 三图。配件图
        third_images_dir = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\03配件图'
        copy_random_images(1, third_images_dir, target_folder)

        # 四图，小孩使用图
        forth_images_dir = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\04小孩使用图'
        copy_random_images(1, forth_images_dir, target_folder)

        # 其他五张细节图
        other_images_dir = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\其他细节图'
        copy_random_images(5, other_images_dir, target_folder)


if __name__ == '__main__':
    run()
