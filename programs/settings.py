from pathlib import Path

SynologyDrive = Path.home() / 'SynologyDrive'
if not SynologyDrive.exists():
    SynologyDrive = Path(r'D:\SynologyDrive')


# 学习机文件夹根目录
xuexiji_dir = SynologyDrive / r'01新项目记录\02_AI学习机'
