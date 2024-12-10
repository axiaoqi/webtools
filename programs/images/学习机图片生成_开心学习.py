from programs.images.images import run_web_images

if __name__ == '__main__':
    from programs.settings import SynologyDrive
    image_dir = SynologyDrive / r'01新项目记录\02_AI学习机\02图片'

    # 主图文件夹
    primary_images_dir = [SynologyDrive / '素材_开心学习主图']
    # 目标文件夹
    destination = SynologyDrive / '01开心学习图片'

    run_web_images(primary_images_dir, destination)
