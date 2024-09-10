from flask import Flask, render_template
from programs import program1, program2, program4, program3
from programs.wenan import 闲鱼_学习机_文案

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# 数据处理
@app.route('/xianyu_wenan', methods=['GET', 'POST'])
def run_program1():
    result = 闲鱼_学习机_文案.run()  # 假设 program1.py 里面有一个 run() 方法
    return render_template('xianyu_wenan.html', result=result)


@app.route('/run_program2', methods=['GET', 'POST'])
def run_program2():
    result = program2.run()
    return render_template('program2.html', result=result)


# 图像处理
@app.route('/program3', methods=['GET', 'POST'])
def run_program3():
    result = program3.run()
    return render_template('program3.html', result=result)


# 文本处理
@app.route('/program4', methods=['GET', 'POST'])
def run_program4():
    result = program4.run()
    return render_template('result.html', result=result)


# 添加更多功能路由

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
