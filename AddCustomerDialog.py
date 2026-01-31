from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox



class AddCustomerDialog(QDialog):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager

        self.setWindowTitle("添加客户")

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        self.email_input = QLineEdit()
        self.remark_input = QLineEdit()

        layout.addRow("姓名", self.name_input)
        layout.addRow("电话", self.phone_input)
        layout.addRow("地址", self.address_input)
        layout.addRow("邮箱", self.email_input)
        layout.addRow("备注", self.remark_input)

        self.save_button = QPushButton("保存")
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_customer)

        self.setLayout(layout)


        # 调整窗口大小
        self.resize(600, 200)  # 或者使用 self.adjustSize()


    def save_customer(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        email = self.email_input.text()
        remark = self.remark_input.text()

        if not name or not phone:  # 必填字段检查
            QMessageBox.warning(self, "警告", "姓名和电话不能为空！")
            return

        # 将客户信息保存到数据库
        self.db_manager.add_customer(name, phone, address, email, remark)
        self.accept()
        # 提示用户
        QMessageBox.information(self, "保存成功", "客户记录已保存！")

