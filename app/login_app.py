# app/login_app.py

import os

# 切换到项目根目录
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from utils.database import Database
from app.register_window import RegisterWindow
from utils.password_utils import PasswordLineEdit
from app.forgot_password_window import ForgotPasswordWindow

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化数据库连接
        self.db = Database()
        # 初始化用户界面
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('登录系统')
        self.setGeometry(300, 300, 300, 200)

        # 创建主布局
        layout = QVBoxLayout()

        # 创建用户名和密码输入框
        self.username_input = QLineEdit()
        self.password_input = PasswordLineEdit()  # 使用自定义的 PasswordLineEdit

        # 添加标签和输入框到布局
        layout.addWidget(QLabel('用户名:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('密码:'))
        layout.addWidget(self.password_input)

        # 创建按钮布局
        button_layout = QHBoxLayout()

        # 创建登录、注册和忘记密码按钮
        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.login)
        register_button = QPushButton('注册')
        register_button.clicked.connect(self.show_register)
        forgot_password_button = QPushButton('忘记密码')
        forgot_password_button.clicked.connect(self.show_forgot_password)

        # 将按钮添加到按钮布局
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(register_button)
        button_layout.addWidget(forgot_password_button)

        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)

        # 设置窗口的主布局
        self.setLayout(layout)

        # 设置登录按钮为默认按钮
        self.login_button.setDefault(True)
        self.login_button.setAutoDefault(True)

    def login(self):
        # 获取用户输入的用户名和密码
        username = self.username_input.text()
        password = self.password_input.get_password()  # 使用 get_password() 方法获取实际密码

        # 验证用户
        if self.db.verify_user(username, password):
            QMessageBox.information(self, "登录成功", "欢迎回来！")
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误。")

    def show_register(self):
        # 显示注册窗口
        self.register_window = RegisterWindow(self.db)
        self.register_window.show()

    def show_forgot_password(self):
        # 显示忘记密码窗口
        self.forgot_password_window = ForgotPasswordWindow(self.db)
        self.forgot_password_window.show()

    def keyPressEvent(self, event):
        # 如果按下回车键，触发登录
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            event.accept()  # 防止事件传播
            self.login()
        else:
            super().keyPressEvent(event)