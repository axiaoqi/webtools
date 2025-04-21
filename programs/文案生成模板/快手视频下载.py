import requests
from lxml import etree


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'cookie': '_ga=GA1.1.793506616.1744649776; __gads=ID=add244bfd7cb2e3b:T=1744649775:RT=1745252526:S=ALNI_Ma8PqbvnU3IEv81uFhQwCjyZKeiTw; __gpi=UID=0000109e1d5da5c7:T=1744649775:RT=1745252526:S=ALNI_MbVyD5APSEcZBLxwc7nXgFjGlXOiQ; __eoi=ID=4df8f435029d3fcd:T=1744649775:RT=1745252526:S=AA-AfjavYgiVMdyKSyJ4MtiOW3M-; XSRF-TOKEN=eyJpdiI6IjhIMTNpcWJEY1pPNTMxT3B1aXlCSnc9PSIsInZhbHVlIjoiTEMxQXZtK2lmb0lNeTQ5amtjaitQQ0EzOTF5YlpPY1A0RzJkM2N6TzQweVE1aTF2T3hZUVdDVVczOEFBQ2pZY2Y5bi8vMmU2dVovNlE1UnlLc2dkTS9MSXhpV1Qvd0V5b0xsWjk2Y2d0a3lHUUo5aWNqMldNY2NGTnhrT0hvU3MiLCJtYWMiOiI1YmFhMTY3NGQxNTNmNGViZjgyOWEzZTAyMWZjNWU0MmQ3YTE4NjlmZWExYzMzNDEzZDIwZmE3NDlkYTIxODc0IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6Im1SbWdxWXJEajNnZHhiZjZyV0FNUXc9PSIsInZhbHVlIjoiV2hYbkVrMmhYbFNBOW5ENXgyMXBEMUdXL1ZwaG51ZDAydldYZWV4UTErYXRSZ0xlOXhtSnp0UkhtRmhuKzJubDdJTHhRYmp1OVEzRlBTUVNlYkg5bFdaMlVUbXlPY20yeHVxY0xiWGgwdzEyd29KcVZhWFpsbnJBSVhGekMrcFMiLCJtYWMiOiI0MjhjMjdhNjk2NTc5ZTViOTM5ZmU5MDI5M2ZlN2NmYTZkNGE1NmQ1ZjU3YzU3YzEzODcyMzQwMmE2OTEyMGQ3IiwidGFnIjoiIn0%3D; FCOEC=%5B%5B%5B28%2C%22%5Bnull%2C%5Bnull%2C1%2C%5B1745252537%2C288674000%5D%5D%5D%22%5D%5D%5D; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B13%2C%22%5B%5C%22DBABL~BVQqAAAAAg%5C%22%2C%5B%5B7%2C%5B1745252533%2C186682000%5D%5D%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol-Gggi4oJPXb4cGvst_nTw1lx18Pb1WNgDeqCBkEebFe_QTBJbstgxnWRequoFrDVExB3GQCGeYFizO5D-1jq3dy5h-Fs4hhloWwXWI_9TRQR_bIyYrN3USmJvAFgP5-Myswb58HcblRdxorud7dGtKQm1SHQ%3D%3D%22%5D%2Cnull%2C%5B%5B2%2C%22%5Bnull%2C%5Bnull%2C1%2C%5B1745252537%2C288674000%5D%5D%5D%22%5D%5D%5D; _ga_MEHFNQTGNY=GS1.1.1745252525.3.1.1745252599.0.0.0'
}

base_url = 'https://douyinxz.com/kuaishou/'


if __name__ == '__main__':
    url = 'https://www.kuaishou.com/short-video/3x3sf46sh54qtrc?authorId=3xyxdkksqu36yr6&streamSource=search&searchKey=%E8%BE%A3%E6%A4%92&area=searchxxnull'
    # url = 'https://www.kuaishou.com/short-video/3x8g8u68jbhj89m?authorId=3xciavcy82p2bru&streamSource=search&area=searchxxnull&searchKey=%E8%BE%A3%E6%A4%92'
    data = {
        '_token': '9hL3iIB1lDy4l8mHo77AlZXlchnhQLEKdpb1s2Px',
        'url': url
    }
    resp = requests.post(url=base_url, headers=headers, json=data)

    print(resp.text)

    tree = etree.HTML(resp.text)
    download_url = tree.xpath('//video/@src')[0]
    file_name = tree.xpath('//h2/text()')[0]
    print(download_url)
    print(file_name)
    # 获取名称

    # 获取下载地址

    # 下载文件