import sys
import os
import webview
import threading
import time
import socket
from flask import Flask

from app import app as original_app


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 创建一个新的、路径配置正确的 Flask 实例
app = Flask(
    __name__,
    template_folder=resource_path('templates'),
    static_folder=resource_path('static')
)

# ================== "偷天换日"的核心代码 (最终修正版 v2) ==================

# 1. 复制配置
app.config.update(original_app.config)

# 2. 遍历原始 app 的所有 URL 规则
for rule in original_app.url_map.iter_rules():
    # 跳过默认的 'static' 规则
    if rule.endpoint == 'static':
        continue

    # 获取原始的视图函数
    view_func = original_app.view_functions[rule.endpoint]

    # ================== 关键修复在这里 ==================
    # 使用更通用、更安全的参数来注册路由
    app.add_url_rule(
        rule.rule,  # 路由路径 (e.g., '/')
        endpoint=rule.endpoint,  # 端点名称 (e.g., 'home')
        view_func=view_func,  # 对应的处理函数
        methods=rule.methods,  # 支持的 HTTP 方法 (e.g., {'GET', 'POST'})
        defaults=rule.defaults  # 默认参数 (如果有的话)
    )
    # ==================================================

# 3. 复制上下文处理器
if hasattr(original_app, 'template_context_processors'):
    for func_list in original_app.template_context_processors.values():
        for func in func_list:
            app.context_processor(func)

# 4. 复制错误处理器
for code, funcs in original_app.error_handler_spec.items():
    for func in funcs.values():
        app.register_error_handler(code, func)


# ==========================================================

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def run_flask_app(port):
    try:
        from waitress import serve
        serve(app, host='127.0.0.1', port=port)
    except ImportError:
        app.run(host='127.0.0.1', port=port)


def main():
    flask_port = find_free_port()
    flask_thread = threading.Thread(target=run_flask_app, args=(flask_port,), daemon=True)
    flask_thread.start()
    time.sleep(1)

    window = webview.create_window(
        '我的个人工具箱',
        f'http://127.0.0.1:{flask_port}/',
        width=1280,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )

    icon_path = resource_path('static/favicon.ico')

    webview.start(icon=icon_path)


if __name__ == '__main__':
    main()