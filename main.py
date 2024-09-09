import os
import sys

# 切换到项目根目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from app.login_app import LoginApp

if __name__ == '__main__':
    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 创建并显示登录应用
    login_app = LoginApp()
    login_app.show()

    # 运行应用的事件循环
    sys.exit(app.exec())