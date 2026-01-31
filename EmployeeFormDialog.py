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

from RegisterDialog import RegisterDialog
from PyQt5.QtGui import QIcon  # 导入 QIcon 类

class EmployeeFormDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("添加员工记录")
        self.setWindowIcon(QIcon("v_preview.png"))  # 添加图标

        self.setFixedSize(700, 550)

        # 输入框和标签
        self.name_label = QLabel("姓名:")
        self.name_input = QLineEdit()
        
        self.position_label = QLabel("职位:")
        self.position_input = QLineEdit()
        
        self.phone_label = QLabel("电话:")
        self.phone_input = QLineEdit()
        
        self.salary_type_label = QLabel("工资类型:")
        self.salary_type_input = QLineEdit()
        
        self.salary_rate_label = QLabel("工资率:")
        self.salary_rate_input = QLineEdit()

        self.hire_date_label = QLabel("入职日期:")

        # 日历选择器和显示框
        self.hire_date_calendar = QCalendarWidget()
        self.hire_date_calendar.setGridVisible(True)  # 显示网格线
        self.hire_date_calendar.setMaximumDate(datetime.today().date())  # 限制日期为今天或之前
        self.hire_date_calendar.setFixedSize(620, 260)  # 设置日历控件大小        
        self.hire_date_display = QLineEdit()  # 用于显示选中的日期
        self.hire_date_display.setReadOnly(True)  # 设置为只读

        # 初始日期显示为当前日期
        today = datetime.today().strftime("%Y-%m-%d")
        self.hire_date_display.setText(today)
        self.hire_date_calendar.selectionChanged.connect(self.update_hire_date_display)

        self.remarks_label = QLabel("备注:")
        self.remarks_input = QLineEdit()

        # 按钮定义
        self.submit_button = QPushButton("提交")
        self.submit_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)

        # 布局设置
        layout = QFormLayout()
        layout.addRow(self.name_label, self.name_input)
        layout.addRow(self.position_label, self.position_input)
        layout.addRow(self.phone_label, self.phone_input)
        layout.addRow(self.salary_type_label, self.salary_type_input)
        layout.addRow(self.salary_rate_label, self.salary_rate_input)

        # 日历和显示框布局
        calendar_layout = QVBoxLayout()
        calendar_layout.addWidget(self.hire_date_display)
        calendar_layout.addWidget(self.hire_date_calendar)
        layout.addRow(self.hire_date_label, calendar_layout)

        layout.addRow(self.remarks_label, self.remarks_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addRow(button_layout)

        self.setLayout(layout)

    def update_hire_date_display(self):
        """
        更新日期显示框内容为日历当前选中的日期。
        """
        selected_date = self.hire_date_calendar.selectedDate().toString("yyyy-MM-dd")
        self.hire_date_display.setText(selected_date)

    def get_data(self):
        # 获取输入的员工信息
        name = self.name_input.text()
        position = self.position_input.text()
        phone = self.phone_input.text()
        salary_type = self.salary_type_input.text()
        salary_rate = self.salary_rate_input.text()
        hire_date = self.hire_date_display.text()  # 从显示框中获取日期
        remarks = self.remarks_input.text()

        if not name or not salary_type or not salary_rate:
            QMessageBox.warning(self, "警告", "姓名、工资类型和工资率是必填项！")
            return None

        return (name, position, phone, salary_type, float(salary_rate), hire_date, remarks)

