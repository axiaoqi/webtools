from programs.images.images import copy_image_to_folders, copy_images_must_and_other, run_web_images

if __name__ == '__main__':
    from programs.settings import SynologyDrive
    # 主图文件夹
    primary_images_dir = [SynologyDrive / r'01新项目记录\02_AI学习机\02图片\素材_花花家主图']
    # 目标文件夹
    destination = SynologyDrive / r'01新项目记录\02_AI学习机\02图片\02花花家图片'

    run_web_images(primary_images_dir, destination)
