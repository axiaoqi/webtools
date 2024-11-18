from pathlib import Path

from programs.python系列软件下载.anaconda官网下载安装包 import update_anaconda
from programs.python系列软件下载.pycharm官网下载安装包 import update_pycharm
from programs.python系列软件下载.python官网下载安装包 import update_python


file_dir = Path(r'Z:\software\python系列')


# 更新Python安装包
update_python(computer_system='windows', file_dir=file_dir)
update_python(computer_system='mac', file_dir=file_dir)

# 更新anaconda安装包
update_anaconda(computer_system='windows', file_dir=file_dir)
update_anaconda(computer_system='mac_intel', file_dir=file_dir)
update_anaconda(computer_system='mac_m', file_dir=file_dir)

# 更新pycharm社区版安装包
update_pycharm(computer_system='windows', file_dir=file_dir)
update_pycharm(computer_system='mac_intel', file_dir=file_dir)
update_pycharm(computer_system='mac_m', file_dir=file_dir)

