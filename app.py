import datetime
from functools import wraps

from flask import Flask, render_template, request, url_for

from programs.music.music import add_music_url
from programs.music.query_url_from_csv import query_musics
from programs.quant.股票分红监控 import calculate_stock_dividends
from programs.text import 闲鱼学习机文案_通用, 闲鱼学习机文案_好好学习, 闲鱼学习机文案_苏苏
from programs.text.违禁词检测.违禁词检测 import load_banned_words, check_for_banned_words
from programs import 淘宝分享链接转真实URL
from programs.xunfei.xunfei import xunfei_lite

from config import EXTERNAL_LINKS, COMMON_PROGRAMS

app = Flask(__name__)

# --- 自动化导航的核心代码 ---
NAV_LINKS = []


# 给装饰器增加 order 参数，默认值为 999
def add_to_nav(name, category=None, show_in_nav=True, order=999):
    def decorator(f):
        NAV_LINKS.append({
            'endpoint': f.__name__,
            'name': name,
            'category': category,
            'show_in_nav': show_in_nav,
            'order': order  # <-- 记录排序号
        })
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.context_processor
def inject_links():
    all_internal_links = []
    # --- 阶段一：收集所有内部链接 ---
    for link in NAV_LINKS:
        try:
            all_internal_links.append(
                {'url': url_for(link['endpoint']), 'name': link.get('name'), 'category': link.get('category'),
                 'show_in_nav': link.get('show_in_nav', True), 'order': link.get('order', 999), 'type': 'internal'})
        except Exception as e:
            print(f"Warning: URL for endpoint '{link['endpoint']}' failed: {e}")
    if 'COMMON_PROGRAMS' in globals():
        for prog in COMMON_PROGRAMS:
            try:
                all_internal_links.append({'url': url_for(prog['endpoint'], **prog['params']), 'name': prog.get('name'),
                                           'category': prog.get('category'),
                                           'show_in_nav': prog.get('show_in_nav', True),
                                           'order': prog.get('order', 999), 'type': 'internal'})
            except Exception as e:
                print(f"Warning: URL for common program '{prog['name']}' failed: {e}")

    # --- 阶段二：构建导航栏列表 (nav_links) ---
    nav_links_raw = [link for link in all_internal_links if link.get('show_in_nav', True)]
    for link in EXTERNAL_LINKS:
        if link.get('category') and link.get('show_in_nav', True): nav_links_raw.append(link)

    nav_links = []
    for item in nav_links_raw:
        nav_links.append({'url': item.get('url'), 'name': item.get('name'), 'category': item.get('category') or ''})

    nav_links.sort(key=lambda x: (x.get('order', 999), x.get('category', ''), x.get('name') or ''))

    # --- 阶段三：构建统一的首页列表 (all_home_links) ---
    all_home_links = all_internal_links + EXTERNAL_LINKS

    # 使用最健壮的排序逻辑对合并后的列表进行统一排序
    all_home_links.sort(key=lambda x: (x.get('order', 999), x.get('category') or '', x.get('name') or ''))

    return dict(
        nav_links=nav_links,
        all_home_links=all_home_links  # <-- 注入这个新列表
    )
@app.context_processor
def inject_external_links():
    return dict(external_links=EXTERNAL_LINKS)

# --- 自动化导航代码结束 ---


# 添加自定义 Jinja2 宏
@app.context_processor
def inject_year():
    return {'current_year': datetime.datetime.now().year}


# 首页
@app.route('/')
@add_to_nav('首页', order=1)  # 加到导航栏
def home():
    return render_template('index.html')


# 通用的程序运行路由
@app.route('/run_program/<program_name>', methods=['GET', 'POST'])
def run_program(program_name):
    result = None

    # 根据传入的 program_name 动态调用不同的程序
    if program_name == '闲鱼学习机文案_通用':
        result = 闲鱼学习机文案_通用.run()
    elif program_name == '闲鱼学习机文案_好好学习':
        result = 闲鱼学习机文案_好好学习.run()
    elif program_name == '闲鱼学习机文案_苏苏':
        result = 闲鱼学习机文案_苏苏.run()

    # 继续为其他程序添加分支
    return render_template('program.html', program_name=program_name, result=result)


@app.route('/淘宝分享链接转真实URL', methods=['GET', 'POST'])
@add_to_nav('淘宝分享链接转真实URL', show_in_nav=False)  # 这个在导航栏
def run_淘宝分享链接转真实URL_route():
    result = ""
    if request.method == 'POST':
        input_data = request.form['input_data']
        print(input_data)
        result = 淘宝分享链接转真实URL.run(input_data)

    return render_template('taobao_realurl.html', result=result)


@app.route('/违禁词检测', methods=['GET', 'POST'])
@add_to_nav('违禁词检测', category='小工具', show_in_nav=True)  # 这个在导航栏
def run_违禁词检测_route():
    result_text = ""
    selected_file = "闲鱼_违禁词.txt"  # 默认选择抖音
    if request.method == "POST":
        input_text = request.form['input_text']
        selected_file = request.form['platform']
        banned_words = load_banned_words(selected_file)
        result_text = check_for_banned_words(input_text, banned_words)

    return render_template("weijinci_jiance.html", result_text=result_text, selected_file=selected_file)


@app.route('/股票分红监测', methods=['GET', 'POST'])
@add_to_nav('股票分红监测', category='股票', show_in_nav=True, order=100)  # 这个在导航栏
def run_股票分红监测_route():
    stock_names = ''
    dividend_year = 2023
    initial_cash = 200000
    if request.method == "POST":
        # 获取用户输入的数据
        stock_names = request.form['stock_names'].splitlines()  # 用户输入的股票名称按行分割
        dividend_year = int(request.form['dividend_year'])
        initial_cash = float(request.form['initial_cash'])

        # 调用分红计算函数
        result_df = calculate_stock_dividends(stock_names, dividend_year, initial_cash)

        # 将结果转换为 HTML 表格进行展示
        result_html = result_df.to_html(classes='table table-bordered', index=False)

        return render_template("fenhong_jiance.html", result_html=result_html, stock_names='\n'.join(stock_names),
                               dividend_year=dividend_year, initial_cash=initial_cash)

    return render_template("fenhong_jiance.html", stock_names=stock_names, dividend_year=dividend_year,
                           initial_cash=initial_cash)


@app.route('/xunfei', methods=['GET', 'POST'])
@add_to_nav('讯飞文案改写', category='小工具', show_in_nav=True)  # 这个在导航栏
def run_xunfei_route():
    s = ''
    master = '你是一个闲鱼卖家专家，帮我修改成原创文案。我是卖小品牌学习机的卖家，想蹭大品牌的流量，开发的同款学习机。文案修改后的格式跟原来差不多'
    if request.method == "POST":
        # 获取用户输入的数据
        content = request.form['content']
        master = request.form['master']
        new_content = master + '文案如下：' + content  # 用户输入音乐的名称

        s = xunfei_lite(new_content)

        return render_template("xunfei.html", result_html=s, content=content, master=master)

    return render_template("xunfei.html", content=s, master=master)


@app.route('/字数统计')
@add_to_nav('字数统计', category='小工具', show_in_nav=True, order=200)  # 这个在导航栏
def run_字数统计_route():
    return render_template('字数统计工具.html')


@app.route('/文案生成助手')
@add_to_nav('文案生成助手', category='小工具', show_in_nav=False, order=400)  # 这个在导航栏
def run_文案生成助手_route():
    return render_template('文案生成助手.html')


@app.route('/取消文案换行')
@add_to_nav('取消文案换行', category='小工具', show_in_nav=True, order=300)  # 这个在导航栏
def run_取消文案换行_route():
    return render_template('取消文案换行.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
