import requests
import re


def run(kouling=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    }
    if kouling:
        url = kouling.split(' ')[0].split('】')[1]
        resp = requests.get(url, headers=headers)
        pattern = r"var url = '(.+?)';"
        real_url = re.findall(pattern, resp.text)[0]

        return real_url


if __name__ == '__main__':
    k = '【淘宝】http://e.tb.cn/h.gsklYA3eEQefZ4p?tk=Igjb38swtWy MF6563 「pycharm2023正式专业版永久激活python/anaconda环境搭建远程安装」点击链接直接打开 或者 淘宝搜索直接打开'

    run(kouling=k)
