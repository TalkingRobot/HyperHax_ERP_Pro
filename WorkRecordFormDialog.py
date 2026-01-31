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
from PyQt5.QtGui import QIcon  # 导入 QIcon 类

class WorkRecordFormDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("添加工时记录")
        self.setWindowIcon(QIcon("v_preview.png"))  # 添加图标

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.employee_select = QComboBox()
        self.employee_id_display = QLineEdit()
        self.employee_id_display.setReadOnly(True)
        self.date_input = QLineEdit()
        self.hours_input = QLineEdit()
        self.hours_input.setReadOnly(True)  # 工时输入框只读
        self.project_input = QLineEdit()
        self.remarks_input = QLineEdit()

        # 添加时间选择器
        self.start_time_select = QComboBox()
        self.end_time_select = QComboBox()

        # 填充时间选项 (从00:00到23:45，每15分钟为一个间隔)
        time_list = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 15)]
        self.start_time_select.addItems(time_list)
        self.end_time_select.addItems(time_list)

        self.layout.addRow("选择员工:", self.employee_select)
        self.layout.addRow("员工ID:", self.employee_id_display)
        self.layout.addRow("选择日期:", self.date_input)  # 日期输入框
        self.layout.addRow("上班时间:", self.start_time_select)  # 上班时间
        self.layout.addRow("下班时间:", self.end_time_select)  # 下班时间
        self.layout.addRow("工时:", self.hours_input)
        self.layout.addRow("项目:", self.project_input)
        self.layout.addRow("备注:", self.remarks_input)

        # 添加一个日历控件供选择日期
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.layout.addRow("选择日期:", self.calendar)

        # 设置日历控件的宽度
        self.calendar.setFixedWidth(620)  # 设置一个适当的固定宽度，例如 400

        button_layout = QHBoxLayout()
        self.submit_btn = QPushButton("提交")
        self.submit_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_btn)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        self.layout.addRow(button_layout)
        self.setFixedSize(700, 600)

        self.load_employees(db_manager)

        # 更新日期输入框
        self.calendar.clicked.connect(self.update_date)

        # 绑定时间选择器的变化事件
        self.start_time_select.currentIndexChanged.connect(self.calculate_hours)
        self.end_time_select.currentIndexChanged.connect(self.calculate_hours)


    def load_employees(self, db_manager):
        employees = db_manager.fetch_all_employees()
        for employee in employees:
            self.employee_select.addItem(employee[1], userData=employee[0])

        # 更新员工ID显示
        self.employee_select.currentIndexChanged.connect(self.update_employee_id)

    def update_employee_id(self):
        # 显示选择的员工ID
        selected_employee_id = self.employee_select.currentData()
        self.employee_id_display.setText(str(selected_employee_id))

    def update_date(self, date):
        # 将选中的日期格式化并显示在日期输入框中
        self.date_input.setText(date.toString("yyyy-MM-dd"))

    def calculate_hours(self):
        """根据上班时间和下班时间计算工时"""
        start_time = self.start_time_select.currentText()
        end_time = self.end_time_select.currentText()

        try:
            # 将时间转换为 datetime 对象
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")

            # 计算工时
            if end_dt > start_dt:
                duration = (end_dt - start_dt).seconds / 3600
            else:
                # 跨天处理
                duration = ((end_dt + datetime.strptime("24:00", "%H:%M")) - start_dt).seconds / 3600

            self.hours_input.setText(f"{duration:.2f}")  # 格式化为两位小数
        except Exception as e:
            self.hours_input.setText("0.00")
            QMessageBox.warning(self, "错误", f"时间计算出错: {e}")



    def get_data(self):
        employee_id = self.employee_select.currentData()
        date = self.date_input.text()
        hours = self.hours_input.text()
        project = self.project_input.text()
        remarks = self.remarks_input.text()

        if not employee_id or not date or not hours:
            QMessageBox.warning(self, "警告", "员工、日期和工时是必填项！")
            return None

        return (employee_id, date, float(hours), project, remarks)


    def insert_work_record(self, employee_id, date, hours, project, remarks):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM employees WHERE id = ?', (employee_id,))
            employee_name_result = cursor.fetchone()
        
            if employee_name_result:
                employee_name = employee_name_result[0]
            else:
                employee_name = "未知员工"  # 设置为默认值
                print(f"Warning: Employee with ID {employee_id} not found, using '未知员工' as name.")
        
            cursor.execute('''
            INSERT INTO work_records (employee_id, employee_name, date, hours, project, remarks)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (employee_id, employee_name, date, hours, project, remarks))
            conn.commit()
