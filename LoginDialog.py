from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from RegisterDialog import RegisterDialog
from DatabaseManager import DatabaseManager
from PyQt5.QtGui import QIcon  # 导入 QIcon 类


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon("v_preview.png"))  # 添加图标

        self.setFixedSize(600, 250)

        self.username_label = QLabel("用户名:")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("密码:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("登录")
        self.register_button = QPushButton("注册")  # 添加注册按钮
        self.cancel_button = QPushButton("取消")

        self.login_button.clicked.connect(self.handle_login)
        self.register_button.clicked.connect(self.open_register_dialog)  # 点击打开注册对话框
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)


    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # 调试信息，查看输入的用户名和密码
        print(f"输入的用户名: {username}")
        print(f"输入的密码: {password}")

        # 从数据库验证用户名和密码
        if self.verify_login(username, password):
            QMessageBox.information(self, "登录成功", "欢迎登录！", QMessageBox.Ok)
            self.accept()  # 登录成功
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误！", QMessageBox.Ok)
            self.reject()  # 登录失败


    def verify_login(self, username, password):
        conn = self.db_manager.connect()  # 连接数据库

        cursor = conn.cursor()
    
        # 查询数据库中的用户名和密码
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()  # 获取第一个匹配的用户
    
        print(f"查询到的用户: {user}")  # 输出调试信息

        conn.close()  # 关闭数据库连接
    
        if user is None:
            return False  # 用户不存在
        # 比较密码是否匹配
        return user[2] == password  # 假设密码在数据库的第三列

    def open_register_dialog(self):
        # 打开注册对话框
        register_dialog = RegisterDialog()
        if register_dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "注册成功", "用户注册成功，请使用新账号登录！")
