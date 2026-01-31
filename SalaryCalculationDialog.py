from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QComboBox, QPushButton, QMessageBox, QCalendarWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
)
from PyQt5.QtCore import QDate
from datetime import datetime



class SalaryCalculationDialog(QDialog):
    def __init__(self, parent, db_manager, salary_calculator):
        super().__init__(parent)
        self.db_manager = db_manager
        self.salary_calculator = salary_calculator
        self.setWindowTitle("工资计算")
        self.setFixedSize(700, 550)

        main_layout = QVBoxLayout()

        # 员工选择部分
        form_layout = QFormLayout()
        self.employee_combo = QComboBox()
        employees = self.db_manager.fetch_all_employees()
        for employee in employees:
            self.employee_combo.addItem(f"{employee[1]} (ID: {employee[0]})", employee[0])
        form_layout.addRow("选择员工:", self.employee_combo)
        main_layout.addLayout(form_layout)

        # 开始日期部分
        start_date_layout = QHBoxLayout()  # Use horizontal layout for label and input

        self.start_date_label = QLabel("开始日期:")
        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText("输入开始日期 (YYYY-MM-DD)")
        self.start_date_input.textChanged.connect(self.update_start_date_display_from_input)

        start_date_layout.addWidget(self.start_date_label)
        start_date_layout.addWidget(self.start_date_input)

        main_layout.addLayout(start_date_layout)

        # Start calendar in next row
        self.start_calendar = QCalendarWidget()
        self.start_calendar.setGridVisible(True)
        self.start_calendar.setSelectedDate(QDate.currentDate())  # 默认当前日期
        self.start_calendar.selectionChanged.connect(self.update_start_date_display)

        main_layout.addWidget(self.start_calendar)

        # 结束日期部分
        end_date_layout = QHBoxLayout()  # Use horizontal layout for label and input

        self.end_date_label = QLabel("结束日期:")
        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText("输入结束日期 (YYYY-MM-DD)")
        self.end_date_input.textChanged.connect(self.update_end_date_display_from_input)

        end_date_layout.addWidget(self.end_date_label)
        end_date_layout.addWidget(self.end_date_input)

        main_layout.addLayout(end_date_layout)

        # End calendar in next row
        self.end_calendar = QCalendarWidget()
        self.end_calendar.setGridVisible(True)
        self.end_calendar.setSelectedDate(QDate.currentDate())  # 默认当前日期
        self.end_calendar.selectionChanged.connect(self.update_end_date_display)

        main_layout.addWidget(self.end_calendar)

        # 按钮
        self.calculate_button = QPushButton("计算工资")
        self.calculate_button.clicked.connect(self.calculate_salary)
        main_layout.addWidget(self.calculate_button)

        self.setLayout(main_layout)

    def update_start_date_display(self):
        # 更新开始日期显示
        selected_start_date = self.start_calendar.selectedDate().toString('yyyy-MM-dd')
        self.start_date_input.setText(selected_start_date)

    def update_end_date_display(self):
        # 更新结束日期显示
        selected_end_date = self.end_calendar.selectedDate().toString('yyyy-MM-dd')
        self.end_date_input.setText(selected_end_date)

    def update_start_date_display_from_input(self):
        # 更新开始日期显示 (从输入框获取)
        input_text = self.start_date_input.text()
        if self.is_valid_date(input_text):
            self.start_calendar.setSelectedDate(QDate.fromString(input_text, 'yyyy-MM-dd'))

    def update_end_date_display_from_input(self):
        # 更新结束日期显示 (从输入框获取)
        input_text = self.end_date_input.text()
        if self.is_valid_date(input_text):
            self.end_calendar.setSelectedDate(QDate.fromString(input_text, 'yyyy-MM-dd'))

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def calculate_salary(self):
        try:
            employee_id = self.employee_combo.currentData()
            start_date_str = self.start_date_input.text()
            end_date_str = self.end_date_input.text()

            # 将日期字符串转为日期对象
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # 检查时间范围有效性
            if start_date > end_date:
                QMessageBox.warning(self, "错误", "开始日期不能晚于结束日期！")
                return

            # 使用 SalaryCalculator 计算工资
            salary_info = self.salary_calculator.calculate_salary_for_period(employee_id, start_date, end_date)

            # 显示工资信息
            QMessageBox.information(
                self,
                "工资计算结果",
                f"总工资: {salary_info['total_salary']} 韩元\n"
                f"正常工时工资: {salary_info['regular_salary']} 韩元\n"
                f"加班工资: {salary_info['overtime_salary']} 韩元\n"
                f"假期工资: {salary_info['holiday_salary']} 韩元",
            )
        except Exception as e:
            QMessageBox.warning(self, "错误", f"计算失败: {str(e)}")
