"""
用之前先配置google gemini api
setx GEMINI_API_KEY "你的api"
"""
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def gemini_text(contents, model="gemini-2.0-flash"):
    response = client.models.generate_content(
        model=model,
        contents=[contents]
    )
    return response.text


if __name__ == '__main__':
    first_parts = "我是一名闲鱼卖家，为了防止系统查重，改写下面的句子。直接给出一个结果，无需其他提示，无需多版本。文案格式保持不变，不需要加粗文字。同款这两个字不能少，因为不是正品。可以适当口语化。文案如下:"
    my_parts = """
【捡漏】 科大讯飞步步高同款学习机智能学习平板高清护眼学习机

自习室采购的一批学习机，还剩几台没用，都是全新未拆封的，只卖二手的价格，有需要的抓紧联系

【学习机参数】
学习机整机12寸，屏幕10.1寸，12+512G内存，学习机专用高清护眼类纸屏，分辨率2560*1600，12重高清护眼！！充电满可用5-7小时左右，家长可以远程管控学习机 ！！可以AI批改作业，自动归纳AI错题总结，自动多维度分析科目薄弱环节，避免偏科。

【学习机功能】完全免费，无二次收费！！！
① AI功能：AR智慧眼指读，AI批改作业，AI拍照搜题，AI精准学等；
② 同步课程：幼、小、初、高全国各年级、十科全套免费更新。科目包含（语文、数学、英语、物理、化学、生物、政治、历史、地理、科学），教材出版社包括（人教版、沪教版、闽教版、苏教版，青岛版，湘教版等全国各版本都有）；
③ 同步练习：全科同步，学练测一体化；
④ 其他功能：英语口语练习，英语阅读，英语写作，听力训练，背单词等等功能；
⑤ 使用学习机专用类纸护眼屏幕，结合AI护眼模式，距离过近会提示，防止近视；
⑥ 具有学习系统和安卓双系统，可以安装网课APP，用于孩子日常上网课。

【售后保障】
全新原装未拆包邮出！！！支持7天无理由，30天内质量问题可以免费换新，主板保修五年！！！
    """
    contents = first_parts + '\n' + my_parts

    print(contents)
    print("*******************分割线************************")
    print(gemini_text(contents, model="gemini-2.5-flash-preview-05-20"))

