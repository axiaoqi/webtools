from pathlib import Path

file_path = Path(r'C:\Users\dell\SynologyDrive\01项目记录\02_AI学习机\01文案\好好学习_文案\09_售后.txt')


def _open_file_by_sep(file_path: Path, sep: str):
    """
    打开txt文件，根据特殊字符分割成列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    data = content.split(sep)  # 解析一下数据
    return data


if __name__ == '__main__':
    a = _open_file_by_sep(file_path, sep='\n\n')

    print(a)
    print(len(a))