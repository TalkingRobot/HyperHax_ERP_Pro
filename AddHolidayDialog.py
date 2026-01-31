from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton

class AddHolidayDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("添加假期")
        self.layout = QFormLayout(self)

        self.employee_name = QLineEdit()
        self.start_date = QLineEdit()
        self.end_date = QLineEdit()

        self.layout.addRow("员工姓名:", self.employee_name)
        self.layout.addRow("假期开始日期 (YYYY-MM-DD):", self.start_date)
        self.layout.addRow("假期结束日期 (YYYY-MM-DD):", self.end_date)

        self.submit_btn = QPushButton("提交")
        self.layout.addWidget(self.submit_btn)
        self.submit_btn.clicked.connect(self.submit_holiday)

    def submit_holiday(self):
        employee_name = self.employee_name.text()
        start_date = self.start_date.text()
        end_date = self.end_date.text()

        # Validation and submission to database
        if employee_name and start_date and end_date:
            self.parent().db_manager.add_holiday(employee_name, start_date, end_date)
            self.accept()
        else:
            # Handle validation error
            pass
