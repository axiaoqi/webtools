import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QProcess, QUrl


class FlaskDesktopApp(QMainWindow):
    def __init__(self, flask_process):
        super().__init__()
        self.flask_process = flask_process
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("XQ桌面程序")
        self.setGeometry(100, 100, 1024, 768)

        # 创建 WebEngineView
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("http://127.0.0.1:7000"))

        # 布局
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.web_view)
        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        """关闭窗口时终止 Flask 进程"""
        self.flask_process.terminate()

        # 最多等待 3 秒关闭 Flask，否则强制杀死
        if not self.flask_process.waitForFinished(150):
            self.flask_process.kill()

        super().closeEvent(event)


def run_flask():
    """启动 Flask 服务器"""
    process = QProcess()
    process.setProgram("python")
    process.setArguments(["app.py"])
    process.setProcessChannelMode(QProcess.MergedChannels)  # 处理日志
    process.start()
    return process


if __name__ == "__main__":
    flask_process = run_flask()

    app = QApplication(sys.argv)
    main_window = FlaskDesktopApp(flask_process)
    main_window.show()
    sys.exit(app.exec())
