from flask import Flask, render_template, request
from programs.text import 闲鱼_学习机_文案1, 闲鱼_学习机_文案2_王

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

    # 继续为其他程序添加分支
    return render_template('program.html', program_name=program_name, result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
