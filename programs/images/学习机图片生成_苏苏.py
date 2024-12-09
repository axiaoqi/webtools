from programs.images.images import copy_image_to_folders, copy_images_must_and_other


def run_web_images():
    from programs.settings import SynologyDrive

    """
    自定义部分
    """
    # 主图文件夹
    primary_images_dir = [SynologyDrive / r'01新项目记录\02_AI学习机\02图片\素材_花花家主图']
    # 目标文件夹
    destination = SynologyDrive / r'01新项目记录\02_AI学习机\02图片\02花花家图片'  # 目的地路径

    # 首图
    target_folders = copy_image_to_folders(primary_images_dir, destination, image_name='主图')
    print(target_folders)

    # 其他8张图
    must_choose_folders = [
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\02整体展示',
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\03配件图',
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\04小孩使用图',
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\05同步课程图',
    ]

    other_folders = [
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\07AR智慧眼图',
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\08选课图',
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\09练习图',
        SynologyDrive / r'01新项目记录\02_AI学习机\02图片\09素材\11护眼模式图',
        SynologyDrive / r'02_AI学习机\02图片\09素材\19其他细节图',
        # ...更多文件夹
    ]

    # 循环掺入其他图片
    for target_folder in target_folders:
        copy_images_must_and_other(must_choose_folders, other_folders, target_folder)


if __name__ == '__main__':
    run_web_images()
