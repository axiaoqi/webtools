from pathlib import Path

SynologyDrive = Path.home() / 'SynologyDrive'
if not SynologyDrive.exists():
    SynologyDrive = Path(r'D:\SynologyDrive')
# mac电脑
if not SynologyDrive.exists():
    SynologyDrive = Path('/Volumes/disk3/SynologyDrive')


# 学习机文件夹根目录
xuexiji_dir = SynologyDrive / r'01项目记录\02_AI学习机'

# 讯飞api文件位置
xunfei_config_file_path = SynologyDrive / r'config_file\xunfei_config_file.json'
