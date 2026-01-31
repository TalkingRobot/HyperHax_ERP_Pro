from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox

class WarehouseWidget(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__()
        self.parent = parent
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()


        # 添加搜索框
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入物流ID或商品名称进行搜索")
        self.search_layout.addWidget(self.search_input)
        layout.addLayout(self.search_layout)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["物流ID", "商品名称", "数量", "状态", "日期"])
        layout.addWidget(self.table)
        self.load_warehouse_data()  # 初始加载所有仓库数据

        # 搜索框输入时触发查询
        self.search_input.textChanged.connect(self.search_warehouse)

        # 功能按钮
        button_layout = QHBoxLayout()
        add_button = QPushButton("添加物流记录")
        delete_button = QPushButton("删除物流记录")
        return_button = QPushButton("返回")

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(return_button)
        layout.addLayout(button_layout)

        # 连接按钮功能
        add_button.clicked.connect(self.add_warehouse_record)
        delete_button.clicked.connect(self.delete_warehouse_record)
        return_button.clicked.connect(self.return_to_main)

        self.setLayout(layout)

    def load_warehouse_data(self, warehouse_data=None):
        """
        加载仓库数据到表格。如果没有提供仓库数据，则加载所有仓库。
        """
        if warehouse_data is None:
            warehouse_data = self.db_manager.fetch_warehouse_data()  # 加载所有仓库数据
        self.table.setRowCount(len(warehouse_data))
        for row_idx, row_data in enumerate(warehouse_data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_warehouse_record(self):
        print("添加物流记录功能开发中...")  # 这里可以弹出一个对话框，让用户填写新增的物流记录

    def delete_warehouse_record(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            self.table.removeRow(selected_row)
            print("物流记录已删除")
        else:
            print("请选择要删除的物流记录")

    def search_warehouse(self):
        """
        根据搜索框输入的物流ID或商品名称进行过滤，并更新表格显示。
        """
        search_text = self.search_input.text().lower()
        all_warehouse_data = self.db_manager.fetch_warehouse_data()

        # 根据物流ID或商品名称进行模糊匹配
        filtered_data = [
            row for row in all_warehouse_data 
            if search_text in str(row[0]).lower() or search_text in str(row[1]).lower()
        ]
        self.load_warehouse_data(filtered_data)

    def return_to_main(self):
        self.parent.show_main_page()  # 调用 MainWindow 中的 show_main_page 方法
        self.close()  # 关闭当前窗口
