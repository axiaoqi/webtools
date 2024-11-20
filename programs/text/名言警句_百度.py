import random

import pandas as pd
import requests
import json


def xue_xi_ming_yan():
    query_word = '学习每日名言警句'
    zhuti = '学习'
    page = random.randint(1, 5)

    url = 'https://hanyu.baidu.com/hanyu/api/sentencelistv2'
    params = {
        'query': query_word,
        'src_id': 51328,
        'query_type': '',
        'type': '',
        'pn': page,
        'ps': 20,
        'smpid': 61135,
        'tab_type': zhuti,
        'gssda_res': '{"quote_tag":"学习","sentence_type":"名言",}'
    }

    resp = requests.get(url, params=params)
    _data = json.loads(resp.text)

    data = _data['data']['ret_array'][0]['list']

    sentence_list = [item['body'][0] for item in data]

    return random.choice(sentence_list)


if __name__ == '__main__':
    s = xue_xi_ming_yan()
    print(s)