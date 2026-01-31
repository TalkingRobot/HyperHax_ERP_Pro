import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt



class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("注册")
        self.setFixedSize(400, 250)

        # 输入框和标签
        self.username_label = QLabel("用户名:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("密码:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_label = QLabel("确认密码:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # 注册按钮和取消按钮
        self.register_button = QPushButton("注册")
        self.cancel_button = QPushButton("取消")

        self.register_button.clicked.connect(self.register)
        self.cancel_button.clicked.connect(self.reject)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def connect_db(self):
        """数据库连接"""
        return sqlite3.connect("company.db")

    def register(self):
        """注册逻辑"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        # 输入验证
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "输入错误", "用户名和密码不能为空！", QMessageBox.Ok)
            return

        if len(password) < 6:
            QMessageBox.warning(self, "密码过短", "密码长度不能少于6个字符！", QMessageBox.Ok)
            return

        if password != confirm_password:
            QMessageBox.warning(self, "密码不匹配", "两次输入的密码不一致，请重新输入！", QMessageBox.Ok)
            return

        if self.check_if_user_exists(username):
            QMessageBox.warning(self, "用户名已存在", f"用户名 '{username}' 已存在，请更换！", QMessageBox.Ok)
            return

        # 保存用户数据到数据库
        if self.save_user_to_db(username, password):
            QMessageBox.information(self, "注册成功", "注册成功，欢迎使用！", QMessageBox.Ok)
            self.accept()
        else:
            QMessageBox.critical(self, "注册失败", "注册过程中出现错误，请重试！", QMessageBox.Ok)

    def check_if_user_exists(self, username):
        """检查用户名是否已存在"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def save_user_to_db(self, username, password):
        """保存新用户到数据库"""
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
