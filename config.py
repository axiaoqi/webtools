# config.py

SHOW_IN_NAV = False
# 外部链接
EXTERNAL_LINKS = [
    {
        'name': '电子资料',
        'url': 'http://iuhui.com:4000/02项目/2024幼小虚拟资料项目/幼小资料链接.html',
        # 'category': '小工具',  # <-- 关键改动：给它分配一个分类
        'order': 4
    },
    {
        'name': 'Python链接',
        'url': 'http://iuhui.com:4000/02项目/2024Python项目/python系列链接.html',
        'order': 3
        # 这个没有 category，所以它不会出现在导航栏里，只会出现在首页内容区
    },
    {
        'name': '学习机售后',
        'url': 'http://iuhui.com:4000/02项目/2024学习机项目/售后文案.html',
        'order': 2
    }
]


# ==================== 新增代码 ====================
# 定义一个列表，存放所有通过通用路由调用的程序
# endpoint: 对应 Flask 的函数名
# params: 传给 url_for 的参数
# name: 在界面上显示的名称
# category: 分类

COMMON_PROGRAMS = [
    {
        'endpoint': 'run_program',
        'params': {'program_name': '闲鱼学习机文案_通用'},
        'name': '学习机文案(通用)',
        'category': '文案',
        'show_in_nav': SHOW_IN_NAV,  # 这个出现在导航栏
        'order': 30
    },
    {
        'endpoint': 'run_program',
        'params': {'program_name': '闲鱼学习机文案_好好学习'},
        'name': '学习机文案(好好学习)',
        'category': '文案',
        'show_in_nav': SHOW_IN_NAV,  # <-- 这个只出现在首页
        'order': 10
    },
    {
        'endpoint': 'run_program',
        'params': {'program_name': '闲鱼学习机文案_智慧学习'},
        'name': '学习机文案(智慧学习)',
        'category': '文案',
        'show_in_nav': SHOW_IN_NAV,  # <-- 这个也只出现在首页
        'order': 20
    },
]
# ===============================================
