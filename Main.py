import sys
import datetime
import time
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PyQt5.QtGui import QIcon  

from RegisterDialog import RegisterDialog
from DatabaseManager import DatabaseManager
from LoginDialog import LoginDialog
from EmployeeFormDialog import EmployeeFormDialog
from EmployeeManagementWidget import EmployeeManagementWidget
from WorkRecordFormDialog import WorkRecordFormDialog
from WorkRecordManagementWidget import WorkRecordManagementWidget 
from ScheduleWidget import ScheduleWidget
from FlowWidget import FlowWidget
from WarehouseWidget import WarehouseWidget
from CustomerManagementWidget import CustomerManagementWidget
from SalaryCalculationDialog import SalaryCalculationDialog
from SalaryCalculator import SalaryCalculator
from HolidayManagementWidget import HolidayManagementWidget


# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HyperHax AOP")
        self.setWindowIcon(QIcon("v_preview.png"))  # 添加图标
        self.setGeometry(100, 100, 1600, 800)

        # 创建 DatabaseManager 实例（避免重复创建）
        self.db_manager = DatabaseManager()
        self.db_manager.init_db()  
        self.db_manager.create_tables()  
        self.db_manager.add_columns_to_work_records()  

        # 初始化工资计算器
        self.salary_calculator = SalaryCalculator(self.db_manager)

        self.show_main_page()

    def calculate_salary(self):
        dialog = SalaryCalculationDialog(self, self.db_manager, self.salary_calculator)
        dialog.exec_()

    def show_main_page(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        top_layout = QHBoxLayout()
        self.employee_btn = QPushButton("员工管理")
        self.work_record_btn = QPushButton("工时记录")
        self.holiday_btn = QPushButton("假期管理")        
        self.salary_calculate_btn = QPushButton("工资计算")
        self.schedule_btn = QPushButton("工作日程")
        self.flow_btn = QPushButton("财务管理")
        self.warehouse_btn = QPushButton("仓库物流")
        self.customer_btn = QPushButton("客户管理")

        # 添加按钮到布局
        for btn in [
            self.employee_btn, self.work_record_btn, self.holiday_btn, 
            self.salary_calculate_btn, self.schedule_btn, self.flow_btn, 
            self.warehouse_btn, self.customer_btn
        ]:
            top_layout.addWidget(btn)

        main_layout.addLayout(top_layout)

        # 员工数据表
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        self.load_employee_data()

        # 连接按钮点击事件
        self.employee_btn.clicked.connect(self.show_employee_management)
        self.work_record_btn.clicked.connect(self.show_work_record_management)
        self.salary_calculate_btn.clicked.connect(self.calculate_salary)
        self.holiday_btn.clicked.connect(self.show_holiday_management)
        self.schedule_btn.clicked.connect(self.show_schedule)
        self.flow_btn.clicked.connect(self.show_flow)
        self.warehouse_btn.clicked.connect(self.show_warehouse)
        self.customer_btn.clicked.connect(self.show_customer_management)

        self.setCentralWidget(main_widget)

    # ----------------- 界面切换按钮函数 ---------------    
    def switch_widget(self, new_widget):
        """切换窗口部件时，释放旧部件，避免内存泄漏"""
        old_widget = self.centralWidget()
        if old_widget:
            old_widget.deleteLater()
        self.setCentralWidget(new_widget)

    def show_schedule(self):
        self.switch_widget(ScheduleWidget(self, self.db_manager))

    def show_flow(self):
        self.switch_widget(FlowWidget(self, self.db_manager))

    def show_warehouse(self):
        self.switch_widget(WarehouseWidget(self, self.db_manager))

    def show_customer_management(self):
        self.switch_widget(CustomerManagementWidget(self, self.db_manager))

    def show_employee_management(self):
        self.switch_widget(EmployeeManagementWidget(self, self.db_manager))

    def show_work_record_management(self):
        self.switch_widget(WorkRecordManagementWidget(self, self.db_manager))

    def show_holiday_management(self):
        self.switch_widget(HolidayManagementWidget(self, self.db_manager))

    def load_employee_data(self):
        rows = self.db_manager.fetch_all_employees()
        self.table.clear()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(8)  
        self.table.setHorizontalHeaderLabels(["ID", "姓名", "职位", "电话", "工资类型", "工资率", "入职日期", "备注"]) 

        for row_idx, row_data in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1])))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row_data[3])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row_data[4])))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row_data[5])))
            self.table.setItem(row_idx, 6, QTableWidgetItem(str(row_data[6])))
            self.table.setItem(row_idx, 7, QTableWidgetItem(str(row_data[7])))

        # 调整列宽
        self.table.setColumnWidth(0, 105)    
        self.table.setColumnWidth(7, 860)  

# 启动应用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
