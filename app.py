from flask import Flask, render_template, request
from programs.text import 闲鱼_学习机_文案1, 闲鱼_学习机_文案2_王, 闲鱼学习机文案_好好学习, 闲鱼学习机文案_苏苏, 闲鱼学习机文案_花花
from programs.text.违禁词检测.违禁词检测 import load_banned_words, check_for_banned_words
from programs import 淘宝分享链接转真实URL

app = Flask(__name__)


# 首页
@app.route('/')
def home():
    return render_template('index.html')


# 通用的程序运行路由
@app.route('/run_program/<program_name>', methods=['GET', 'POST'])
def run_program(program_name):
    result = None

    # 根据传入的 program_name 动态调用不同的程序
    if program_name == '闲鱼_学习机_文案1':
        result = 闲鱼_学习机_文案1.run()
    elif program_name == '闲鱼_学习机_文案2_王':
        result = 闲鱼_学习机_文案2_王.run()
    elif program_name == '闲鱼学习机文案_好好学习':
        result = 闲鱼学习机文案_好好学习.run()
    elif program_name == '闲鱼学习机文案_娜娜子':
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
