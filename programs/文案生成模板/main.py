from pathlib import Path


def generate_html(content: str):
    format_content = ''
    template_content = Path('模板.html').read_text(encoding='utf-8')
    i = 1
    content_list = content.split('\n\n')
    # 分割段落，以空行分割
    for s in content_list:
        format_s = template_content.format(f"{i:02d}", s)
        format_content = format_content + format_s + '\n'
        i += 1
    return format_content


if __name__ == '__main__':
    wenan_file = Path.home() / 'Desktop' / '文案.txt'
    f_wenan_file = Path.home() / 'Desktop' / '格式化--文案.txt'
    content = wenan_file.read_text(encoding='utf-8')
    f_c = generate_html(content)
    with open(f_wenan_file, encoding='utf-8', mode='w') as f:
        f.write(f_c)


