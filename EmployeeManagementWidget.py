import sys
import datetime
import time
from datetime import datetime
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QLabel, QComboBox
)
from PyQt5.QtWidgets import QCalendarWidget
from EmployeeFormDialog import EmployeeFormDialog



# 插入员工数据的方法
class EmployeeManagementWidget(QWidget):
    def __init__(self, main_window, db_manager):
        super().__init__()
        self.main_window = main_window
        self.db_manager = db_manager
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 添加搜索框
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入员工ID或姓名进行搜索")
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.load_data()  # 初始加载所有员工数据

        # 搜索框输入时触发查询
        self.search_input.textChanged.connect(self.search_employees)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加员工记录")
        self.delete_btn = QPushButton("删除员工记录")
        self.back_btn = QPushButton("返回")
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)
        self.layout.addLayout(button_layout)

        self.add_btn.clicked.connect(self.add_employee)
        self.delete_btn.clicked.connect(self.delete_employee)
        self.back_btn.clicked.connect(self.main_window.show_main_page)

    def load_data(self, employees=None):
        """
        加载员工数据到表格。如果没有提供员工数据，则加载所有员工。
        """
        if employees is None:
            employees = self.db_manager.fetch_all_employees()  # 加载所有员工数据
        self.table.setRowCount(len(employees))
        self.table.setColumnCount(8)  # 设置8列，包含备注列
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "职位", "电话", "工资类型", "工资率", "入职日期", "备注"])  # 添加备注列

        for row_idx, row_data in enumerate(employees):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        self.table.setColumnWidth(0, 105)    # 手动调整员工ID列
        self.table.setColumnWidth(7, 860)  # 调整备注列宽度

    def add_employee(self):
        dialog = EmployeeFormDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if data:
                self.db_manager.insert_employee(data)
                self.load_data()  # 重新加载所有数据

    def delete_employee(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "警告", "请选择要删除的员工！")
            return
        employee_id = self.table.item(selected, 0).text()
        self.db_manager.delete_employee(employee_id)
        self.load_data()  # 重新加载所有数据

    def search_employees(self):
        """
        根据搜索框输入的员工 ID 或姓名进行过滤，并更新表格显示。
        """
        search_text = self.search_input.text().lower()
        all_employees = self.db_manager.fetch_all_employees()

        # 根据员工ID或姓名进行模糊匹配
        filtered_employees = [
            employee for employee in all_employees 
            if search_text in str(employee[0]).lower() or search_text in employee[1].lower()
        ]
        self.load_data(filtered_employees)  # 加载过滤后的数据
