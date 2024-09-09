import os
import sqlite3

# 切换到项目根目录
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Database:
    def __init__(self):
        # 连接到SQLite数据库
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # 创建用户表（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (username TEXT PRIMARY KEY, password TEXT, security_question TEXT, security_answer TEXT)
        ''')
        self.conn.commit()

    def verify_user(self, username, password):
        # 验证用户名和密码
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def add_user(self, username, password, security_question, security_answer):
        # 添加新用户
        try:
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                                (username, password, security_question, security_answer))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 如果用户名已存在，返回False
            return False

    def check_user_exists(self, username):
        # 检查用户名是否已存在
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone() is not None

    def verify_security_answer(self, username, security_answer):
        # 验证安全问题答案
        self.cursor.execute("SELECT * FROM users WHERE username=? AND security_answer=?",
                            (username, security_answer))
        return self.cursor.fetchone() is not None

    def update_password(self, username, new_password):
        # 更新用户密码
        self.cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        self.conn.commit()

    def get_security_question(self, username):
        # 获取用户的密保问题
        self.cursor.execute("SELECT security_question FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def __del__(self):
        # 关闭数据库连接
        self.conn.close()