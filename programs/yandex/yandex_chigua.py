import requests
from lxml import etree


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
           'cookie': '_ym_uid=1730943633591778485; spravka=dD0xNzMwOTQzNjM1O2k9NDYuMjMyLjEyMy42O0Q9RkMzM0I0QTk4QkEzOTQzRjRFRjNFNTVBNzJEMjVFOUJBQzdGMkI4RTU5RDkzQ0IzMkVCNzZEQTUxQkYyODI0MzkzQkM1OTcxOTMwNjA4MzhFNjY0QzRGNzg1NkMzMzY3NDg0OEU1QkZGNENDRDczOEM1QzY1RUFBRkJDRTNENzI5QzQzRTlBQTY2MjRFRTA4RjkwOUEwQ0E1QTRFO3U9MTczMDk0MzYzNTI1NTE3NzY0NjtoPWIwZGI1NTgzOTdlMWQ2OTVjZmE1YWJjYTkzOTZlNzY4; is_gdpr=0; is_gdpr_b=CNCkdRCEnQIoAg==; yashr=9953894971730943636; receive-cookie-deprecation=1; gdpr=0; yandexuid=2249851931730943632; yuidss=2249851931730943632; i=+ZaS7X74C09uFlxU1WxPRsaL68yBiAC9IN6vTlKXN6QXeMCtI8z5ogDjnQPaaLgQQz63v6lnb4HOkbzkC7ly0pJqYzY=; ymex=1734531197.oyu.5074232731730943636#2046303640.yrts.1730943640; _ym_isad=2; font_loaded=YSv1; cycada=eJy7f2sp1WyE8K2on8tsPmEtlGhUGKKwuD2Wx3HzUGY=; yandex_gid=10636; my=YysBqYwA; gpb=yandex_gid.10636#ygo.134%3A10636#ygu.0; _ym_d=1731941825; _yasc=EOnTBCbhPp/k1OX9udKBlYaCD8Bo4Ly021xqlsjPM80GX5ttvVOhBOOf706/9hAabRGKpeTAN364BvPBHQ==; bh=EkEiQ2hyb21pdW0iO3Y9IjEzMCIsICJHb29nbGUgQ2hyb21lIjt2PSIxMzAiLCAiTm90P0FfQnJhbmQiO3Y9Ijk5IhoFIng4NiIiECIxMzAuMC42NzIzLjExOSIqAj8wMgIiIjoJIldpbmRvd3MiQggiMTUuMC4wIkoEIjY0IlJdIkNocm9taXVtIjt2PSIxMzAuMC42NzIzLjExOSIsICJHb29nbGUgQ2hyb21lIjt2PSIxMzAuMC42NzIzLjExOSIsICJOb3Q/QV9CcmFuZCI7dj0iOTkuMC4wLjAiWgI/MGCbr+25Bmoe3Mrh/wiS2KGxA5/P4eoD+/rw5w3r//32D6fIzIcI; yp=1747709804.szm.2_5%3A1280x720%3A1263x585#1763477812.ygu.0#1763477812.ygo.134%3A10636#2047302297.pcs.1#1737126299.atds.1#1732025597.yu.5074232731730943636#1732803201.dlp.2#1734620216.csc.1; ys=wprid.1731942296732190-13016623595090316538-balancer-l7leveler-kubr-yp-klg-117-BAL'}

keyword = '吃瓜网'
pages = 2

can_open_urls = []
for page in range(pages):
    url = f'https://yandex.com/search/?text={keyword}&lr=10590&p={page}'

    resp = requests.get(url, headers=headers)

    tree = etree.HTML(resp.content)
    items = tree.xpath('//*[@id="search-result"]/li/div/div[2]/div/a')

    for item in items:
        url = item.xpath('@href')[0]
        try:
            _reps = requests.get(url, headers=headers, timeout=3)
            if _reps.status_code == 200:
                print(f'正常的链接：{url}')
                can_open_urls.append(url)
        except Exception as e:
            print(f'连不上网：{url}')

print('********************************')
for i in can_open_urls:
    print(i)

