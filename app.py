import datetime
import time

from flask import Flask, render_template, request

from html import escape

from programs.music.music import add_music_url
from programs.music.query_url_from_csv import query_musics
from programs.quant.股票分红监控 import calculate_stock_dividends
from programs.text import 闲鱼学习机文案_通用, 闲鱼_学习机_文案2_王, 闲鱼学习机文案_好好学习, 闲鱼学习机文案_苏苏, 闲鱼学习机文案_花花
from programs.text.违禁词检测.违禁词检测 import load_banned_words, check_for_banned_words
from programs import 淘宝分享链接转真实URL
from programs.xunfei.xunfei import xunfei_lite

app = Flask(__name__)


# 添加自定义 Jinja2 宏
@app.context_processor
def inject_year():
    return {'current_year': datetime.datetime.now().year}

# 首页
@app.route('/')
def home():
    return render_template('index.html')


# 通用的程序运行路由
@app.route('/run_program/<program_name>', methods=['GET', 'POST'])
def run_program(program_name):
    result = None

    # 根据传入的 program_name 动态调用不同的程序
    if program_name == '闲鱼学习机文案_通用':
        result = 闲鱼学习机文案_通用.run()
    elif program_name == '闲鱼_学习机_文案2_王':
        result = 闲鱼_学习机_文案2_王.run()
    elif program_name == '闲鱼学习机文案_好好学习':
        result = 闲鱼学习机文案_好好学习.run()
    elif program_name == '闲鱼学习机文案_苏苏':
        result = 闲鱼学习机文案_苏苏.run()
    elif program_name == '闲鱼学习机文案_花花':
        result = 闲鱼学习机文案_花花.run()

    # 继续为其他程序添加分支
    return render_template('program.html', program_name=program_name, result=result)


@app.route('/淘宝分享链接转真实URL', methods=['GET', 'POST'])
def run_淘宝分享链接转真实URL_route():
    result = ""
    if request.method == 'POST':
        input_data = request.form['input_data']
        print(input_data)
        result = 淘宝分享链接转真实URL.run(input_data)

    return render_template('taobao_realurl.html', result=result)


@app.route('/违禁词检测', methods=['GET', 'POST'])
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


@app.route('/音乐下载', methods=['GET', 'POST'])
def run_音乐下载_route():
    music_names = ''
    if request.method == "POST":
        # 获取用户输入的数据
        music_names = request.form['music_names'].splitlines()  # 用户输入的音乐名称按行分割
        # 查询数据
        s = query_musics(music_names)
        result_html = s.replace('\n', '<br>')  # 转为html格式的
        return render_template("music_download.html", result_html=result_html, music_names='\n'.join(music_names))

    return render_template("music_download.html", music_names=music_names)


@app.route('/音乐添加', methods=['GET', 'POST'])
def run_音乐添加_route():
    s = ''
    if request.method == "POST":
        # 获取用户输入的数据
        music_name = request.form['music_name']  # 用户输入音乐的名称
        music_url_baidu = request.form['music_url_baidu']  # 用户输入音乐的名称
        music_url_kuake = request.form['music_url_kuake']  # 用户输入音乐的名称

        print(music_name)
        print('\n' + music_url_baidu + '\n')
        print(music_url_kuake)

        # 添加数据
        s = add_music_url(music_name, music_url_baidu, music_url_kuake)

        print(s)

        return render_template("music_add.html", result_html=s, music_name=music_name, music_url_baidu=music_url_baidu, music_url_kuake=music_url_kuake)

    return render_template("music_add.html", music_names=s)

@app.route('/xunfei', methods=['GET', 'POST'])
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
def run_字数统计_route():
    return render_template('字数统计工具.html')


@app.route('/文案生成助手')
def run_文案生成助手_route():
    return render_template('文案生成助手.html')


@app.route('/取消文案换行')
def run_取消文案换行_route():
    return render_template('取消文案换行.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
