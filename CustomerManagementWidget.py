from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QDialog

from AddCustomerDialog import AddCustomerDialog



class CustomerManagementWidget(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__(parent)  # 传递 parent 给 QWidget

        self.main_window = parent  # 将 parent 赋值给 main_window

        self.db_manager = db_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 添加搜索框
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入客户ID或姓名进行搜索")
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        # 客户数据表格
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.load_customer_data()  # 初始加载所有客户数据

        # 搜索框输入时触发查询
        self.search_input.textChanged.connect(self.search_customers)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加客户")
        self.delete_btn = QPushButton("删除客户")
        self.back_btn = QPushButton("返回")
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)
        self.layout.addLayout(button_layout)

        self.add_btn.clicked.connect(self.add_customer)
        self.delete_btn.clicked.connect(self.delete_customer)
        self.back_btn.clicked.connect(self.back_to_main)

    def load_customer_data(self, customers=None):
        """
        加载客户数据到表格。如果没有提供客户数据，则加载所有客户。
        """
        if customers is None:
            customers = self.db_manager.fetch_all_customers()  # 加载所有客户数据
        self.table.setRowCount(len(customers))
        self.table.setColumnCount(6)  # 设置6列，包含备注列
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "电话", "地址", "邮箱", "备注"])  # 添加备注列

        for row_idx, row_data in enumerate(customers):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        self.table.setColumnWidth(0, 105)    # 手动调整客户ID列
        self.table.setColumnWidth(5, 1070)  # 调整备注列宽度

    def add_customer(self):
        dialog = AddCustomerDialog(self, self.db_manager)
        if dialog.exec_():
            data = dialog.get_data()
            if data:
                self.db_manager.add_customer(data)
                self.load_customer_data()  # 重新加载所有数据

    def delete_customer(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "警告", "请选择要删除的客户！")
            return
        customer_id = self.table.item(selected, 0).text()
        self.db_manager.delete_customer(customer_id)
        self.load_customer_data()  # 重新加载所有数据

    def search_customers(self):
        """
        根据搜索框输入的客户 ID 或姓名进行过滤，并更新表格显示。
        """
        search_text = self.search_input.text().lower()
        all_customers = self.db_manager.fetch_all_customers()

        # 根据客户ID或姓名进行模糊匹配
        filtered_customers = [
            customer for customer in all_customers 
            if search_text in str(customer[0]).lower() or search_text in customer[1].lower()
        ]
        self.load_customer_data(filtered_customers)

    def back_to_main(self):
        self.main_window.show_main_page()  # 调用 MainWindow 中的 show_main_page 方法
        self.close()  # 关闭当前窗口
