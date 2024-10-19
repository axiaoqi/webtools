from pathlib import Path

log_file = Path.home() / 'Desktop' / '已删除的文件.txt'


def find_small_files(start_path, min_size):
    for file_path in start_path.rglob('*'):
        if file_path.is_file() and file_path.stat().st_size < min_size:
            print(file_path, file_path.stat().st_size)

            # 删除文件
            file_path.unlink()

            # 写入文件
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(str(file_path) + '\n')


# 使用示例：
start_dir = Path(r'C:\Users\e5\Desktop\小初资料')  # 替换为你要搜索的目录
min_size = 1024  # 1KB = 1024 bytes
find_small_files(start_dir, min_size)

