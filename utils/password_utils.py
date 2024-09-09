import re

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLineEdit


class PasswordLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_last_char)
        self.last_length = 0
        self.textEdited.connect(self.on_text_edited)
        self._actual_password = ""  # 存储实际密码

    def on_text_edited(self, text):
        if len(text) > self.last_length:
            self.timer.stop()
            self._actual_password += text[-1]  # 更新实际密码
            self.show_last_char()
            self.timer.start(1000)
        elif len(text) < self.last_length:
            # 处理删除字符的情况
            self._actual_password = self._actual_password[:len(text)]
        self.last_length = len(text)

    def show_last_char(self):
        text = self.text()
        if text:
            masked_text = '•' * (len(text) - 1) + text[-1]
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.setText(masked_text)
            self.setCursorPosition(len(text))

    def hide_last_char(self):
        text = self.text()
        if text:
            masked_text = '•' * (len(text))
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.setText(masked_text)
            self.setCursorPosition(len(text))

    def text(self):
        # 重写 text() 方法，返回实际密码而不是显示的文本
        return self._actual_password

    def get_password(self):
        # 提供一个明确的方法来获取实际密码
        return self._actual_password

def is_strong_password(password):
    """
    检查密码强度
    要求：
    1. 至少8个字符
    2. 包含至少一个小写字母
    3. 包含至少一个数字
    4. 包含至少一个大写字母或一个特殊字符
    """
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not (re.search(r"[A-Z]", password) or re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

def get_password_strength_message(password):
    """
    返回密码强度的详细信息
    """
    print(f"Checking password: {password}")  # 调试输出

    messages = []
    if len(password) < 8:
        messages.append("密码长度至少为8个字符")
    if not any(c.islower() for c in password):
        messages.append("密码需包含至少一个小写字母")
    if not any(c.isdigit() for c in password):
        messages.append("密码需包含至少一个数字")
    if not (any(c.isupper() for c in password) or any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)):
        messages.append("密码需包含至少一个大写字母或一个特殊字符")

    print(f"Messages: {messages}")  # 调试输出

    if not messages:
        return "密码强度符合要求"
    else:
        return "\n".join(messages)