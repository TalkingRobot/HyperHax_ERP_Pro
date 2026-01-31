from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class FlowWidget(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__(parent)

        self.main_window = parent
        self.db_manager = db_manager

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 添加搜索框
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入流水ID或日期进行搜索")
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        # 流水数据表格
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.load_flow_data()  # 初始加载所有流水数据

        # 搜索框输入时触发查询
        self.search_input.textChanged.connect(self.search_flows)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加流水记录")
        self.delete_btn = QPushButton("删除流水记录")
        self.back_btn = QPushButton("返回")

        # 按钮添加到布局中
        self.add_btn.setIcon(QIcon("add_icon.png"))  # 根据需要替换图标路径
        self.delete_btn.setIcon(QIcon("delete_icon.png"))
        self.back_btn.setIcon(QIcon("back_icon.png"))

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)
        self.layout.addLayout(button_layout)

        self.add_btn.clicked.connect(self.add_flow_record)
        self.delete_btn.clicked.connect(self.delete_flow_record)
        self.back_btn.clicked.connect(self.return_to_main)

    def load_flow_data(self, flow_data=None):
        """
        加载流水数据到表格。如果没有提供流水数据，则加载所有流水。
        """
        if flow_data is None:
            flow_data = self.db_manager.fetch_flow_data()  # 加载所有流水数据
        self.table.setRowCount(len(flow_data))
        self.table.setColumnCount(4)  # 设置4列
        self.table.setHorizontalHeaderLabels(["流水ID", "日期", "金额", "备注"])

        for row_idx, row_data in enumerate(flow_data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # 调整列宽
        self.table.setColumnWidth(0, 100)    # 流水ID列
        self.table.setColumnWidth(1, 150)    # 日期列
        self.table.setColumnWidth(3, 250)    # 备注列
        self.table.setColumnWidth(2, 130)    # 金额列

    def add_flow_record(self):
        print("添加流水功能开发中...")  # 可以在这里弹出一个对话框，让用户填写新增的流水信息

    def delete_flow_record(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "警告", "请选择要删除的流水记录！")
            return
        flow_id = self.table.item(selected, 0).text()
        self.db_manager.delete_flow_record(flow_id)
        self.load_flow_data()  # 重新加载所有数据

    def search_flows(self):
        """
        根据搜索框输入的流水ID或日期进行过滤，并更新表格显示。
        """
        search_text = self.search_input.text().lower()
        all_flows = self.db_manager.fetch_flow_data()

        # 根据流水ID或日期进行模糊匹配
        filtered_flows = [
            flow for flow in all_flows 
            if search_text in str(flow[0]).lower() or search_text in str(flow[1]).lower()
        ]
        self.load_flow_data(filtered_flows)

    def return_to_main(self):
        self.main_window.show_main_page()  # 调用 MainWindow 中的 show_main_page 方法
        self.close()  # 关闭当前窗口
