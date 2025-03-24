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
    print(format_content)


if __name__ == '__main__':
    content = """
𝗦𝗽𝗿𝗶𝗻𝗴𝘀𝘂𝗻𝗻𝘆⁺⁹⁹⁹
时间煮雨，岁月缝花
烟火谋生，诗意谋爱
得失随缘，枯荣有数
行则将至，静待春来

🎀 𝐵𝑒 𝓅𝓇ℴ𝓊𝒹 🎀 
玫瑰带刺，依然被爱
苔花如米，也学牡丹
接纳缺口，自成圆满
余生很长，不必慌张

˗ ̗̀ 💎 𝐖𝐢𝐥𝐥 𝐛𝐞 𝐛𝐞𝐭𝐭𝐞𝐫
暗处生长，静候花期
逆风执炬，自有光迹
山有顶峰，海有彼岸
素履以往，终成璀璨

𝗦𝗲𝗹𝗳-𝗵𝗲𝗮𝗹𝗶𝗻𝗴 🌿
空杯见月，静水听雷
不困荆棘，自成蔷薇
心有猛虎，细嗅蔷薇
万般皆苦，自渡可追

🦋·₊˚ 𝒮𝒽𝒾𝓃𝒾𝓃𝑔 𝓉𝒾𝓂ℯ 
破茧成蝶，自缚作茧
飞蛾扑火，亦是涅槃
不惧深渊，自成彼岸
心若皎月，何惧夜寒

𓆩♡𓆪 𝙎𝙚𝙡𝙛-𝙧𝙚𝙙𝙚𝙢𝙥𝙩𝙞𝙤𝙣 
与光同尘，与时舒卷
和其同光，不掩锋芒
花自向阳，水自流淌
心若菩提，何惧沧桑

☄️‧₊˚ 𝘾𝙤𝙪𝙧𝙖𝙜𝙚 𝙩𝙤 𝙗𝙚 
枯枝生芽，废墟开花
暗室燃灯，深渊架桥
虽败犹荣，虽迟但到
心若有光，何惧路遥

🌌‧₊˚ 𝒮𝓉𝒶𝓇𝓁𝒾𝑔𝒽𝓉 
萤火微光，可亮旷野
星子碎芒，终成银河
暗潮涌动，自成漩涡
心向璀璨，终有星河

🪐‧₊˚ 𝙃𝙤𝙥𝙚 𝙛𝙪𝙚𝙡𝙨 𝙡𝙞𝙛𝙚 
山不让尘，川不辞盈
树摇风响，浪推潮生
暗夜泅渡，终见黎明
心火不灭，永怀热诚

𓂃𓂃𓈒𓏸 𝙒𝙖𝙧𝙙 𝙤𝙛𝙛 𝙙𝙖𝙧𝙠𝙣𝙚𝙨𝙨 
暗室逢灯，绝渡逢舟
雪中送炭，困时援手
深渊回响，终有应答
心灯长明，无惧孤途
"""
    generate_html(content)


