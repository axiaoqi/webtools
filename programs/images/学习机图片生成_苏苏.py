from programs.images.images import run_web_images_susu

if __name__ == '__main__':
    from programs.settings import SynologyDrive
    image_dir = SynologyDrive / r'01新项目记录\02_AI学习机\02图片'

    # 主图文件夹
    primary_images_dir = [image_dir / '素材_苏苏家主图']
    # 目标文件夹
    destination = image_dir / '03苏苏家图片'

    run_web_images_susu(primary_images_dir, destination)
