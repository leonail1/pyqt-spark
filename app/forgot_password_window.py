import os
os.chdir(os.path.dirname(os.path.dirname(__file__)))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from utils.password_utils import is_strong_password, get_password_strength_message

from utils.password_utils import PasswordLineEdit


class ForgotPasswordWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('忘记密码')
        self.setGeometry(350, 350, 300, 300)

        # 创建主布局
        layout = QVBoxLayout()

        # 创建用户名输入框
        self.username = QLineEdit()
        self.username.textChanged.connect(self.update_security_question)

        # 创建密保问题标签
        self.security_question_label = QLabel('密保问题:')

        # 创建密保答案输入框
        self.security_answer = QLineEdit()

        # 创建新密码输入框，使用自定义的PasswordLineEdit类
        self.new_password = PasswordLineEdit()
        self.new_password.textChanged.connect(self.check_password_strength)

        # 创建密码强度提示标签
        self.password_strength_label = QLabel()
        self.password_strength_label.setWordWrap(True)

        # 添加标签和输入框到布局
        layout.addWidget(QLabel('用户名:'))
        layout.addWidget(self.username)
        layout.addWidget(self.security_question_label)
        layout.addWidget(QLabel('密保答案:'))
        layout.addWidget(self.security_answer)
        layout.addWidget(QLabel('新密码:'))
        layout.addWidget(self.new_password)
        layout.addWidget(self.password_strength_label)

        # 创建重置密码按钮
        reset_button = QPushButton('重置密码')
        reset_button.clicked.connect(self.reset_password)
        layout.addWidget(reset_button)

        # 设置窗口的主布局
        self.setLayout(layout)

    def update_security_question(self):
        # 获取用户名
        username = self.username.text()
        # 获取对应的密保问题
        question = self.db.get_security_question(username)
        if question:
            self.security_question_label.setText(f'密保问题: {question}')
        else:
            self.security_question_label.setText('密保问题: 用户不存在')

    def check_password_strength(self):
        # 获取当前新密码输入框中的文本
        password = self.new_password.text()
        # 获取密码强度消息
        strength_message = get_password_strength_message(password)
        # 更新密码强度提示标签
        self.password_strength_label.setText(strength_message)

    def reset_password(self):
        # 获取用户输入的信息
        username = self.username.text()
        security_answer = self.security_answer.text()
        new_password = self.new_password.text()

        # 验证新密码强度
        if not is_strong_password(new_password):
            QMessageBox.warning(self, "密码重置失败", "新密码不符合安全要求。请检查密码强度提示。")
            return

        # 验证安全问题答案并重置密码
        if self.db.verify_security_answer(username, security_answer):
            self.db.update_password(username, new_password)
            QMessageBox.information(self, "密码重置", "密码已成功重置。")
            self.close()
        else:
            QMessageBox.warning(self, "密码重置失败", "用户名或密保答案错误。")