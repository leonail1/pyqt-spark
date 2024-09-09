from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox)

from utils.password_utils import is_strong_password, get_password_strength_message, PasswordLineEdit


class RegisterWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('注册')
        self.setGeometry(350, 350, 300, 350)

        # 创建主布局
        layout = QVBoxLayout()

        # 创建用户名输入框
        self.username = QLineEdit()

        # 创建密码输入框，使用自定义的PasswordLineEdit类
        self.password = PasswordLineEdit()
        # 当密码输入框的文本改变时，检查密码强度
        self.password.textChanged.connect(self.check_password_strength)

        # 创建密码强度提示标签
        self.password_strength_label = QLabel()
        self.password_strength_label.setWordWrap(True)

        # 创建密保问题下拉列表
        self.security_question = QComboBox()
        self.security_question.addItems([
            "您的出生地是？",
            "您母亲的姓名是？",
            "您父亲的姓名是？",
            "您就读的小学名称是？",
            "您最喜欢的颜色是？",
            "您最喜欢的食物是？"
        ])

        # 创建密保答案输入框
        self.security_answer = QLineEdit()

        # 添加标签和输入框到布局
        layout.addWidget(QLabel('用户名:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('密码:'))
        layout.addWidget(self.password)
        layout.addWidget(self.password_strength_label)
        layout.addWidget(QLabel('密保问题:'))
        layout.addWidget(self.security_question)
        layout.addWidget(QLabel('密保答案:'))
        layout.addWidget(self.security_answer)

        # 创建注册按钮
        register_button = QPushButton('注册')
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        # 设置窗口的主布局
        self.setLayout(layout)

    def check_password_strength(self):
        # 获取当前密码输入框中的文本
        password = self.password.text()
        # 获取密码强度消息
        strength_message = get_password_strength_message(password)
        # 更新密码强度提示标签
        self.password_strength_label.setText(strength_message)

    def register(self):
        # 获取用户输入的注册信息
        username = self.username.text()
        password = self.password.text()
        security_question = self.security_question.currentText()
        security_answer = self.security_answer.text()

        # 输入验证
        if not username or not password or not security_answer:
            QMessageBox.warning(self, "注册失败", "所有字段都必须填写。")
            return

        if not is_strong_password(password):
            QMessageBox.warning(self, "注册失败", "密码不符合安全要求。请检查密码强度提示。")
            return

        # 尝试添加新用户
        if self.db.add_user(username, password, security_question, security_answer):
            QMessageBox.information(self, "注册成功", "您已成功注册。")
            self.close()
        else:
            QMessageBox.warning(self, "注册失败", "用户名已存在。")