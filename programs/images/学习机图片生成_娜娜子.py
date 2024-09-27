from programs.images.images import copy_random_images, copy_image_to_folders


def run_web_images():
    from programs.settings import SynologyDrive

    """
    自定义部分
    """
    # 主图文件夹
    primary_images_dir = [SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\00_学习机原图\源文件\闲鱼主图-娜娜子']
    # 目标文件夹
    destination = SynologyDrive / fr'01新项目记录\闲鱼项目\AI学习机\00_学习机原图\娜娜子图片'  # 目的地路径

    # 首图
    target_folders = copy_image_to_folders(primary_images_dir, destination, image_name='主图')
    print(target_folders)

    # 循环掺入其他图片
    for target_folder in target_folders:
        # 二图，三图，用没有处理过的原图
        second_images_dir = [SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\学习机图片-网上找的\01学习机主图']
        copy_random_images(2, second_images_dir, target_folder)

        # 四图。配件图
        third_images_dir = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\03配件图'
        copy_random_images(1, third_images_dir, target_folder, image_name='三图_配件图')

        # 五图，小孩使用图
        forth_images_dir = SynologyDrive / r'01新项目记录\闲鱼项目\AI学习机\02图片\04小孩使用图'
        copy_random_images(1, forth_images_dir, target_folder, image_name='四图_小孩使用图')


if __name__ == '__main__':
    run_web_images()
