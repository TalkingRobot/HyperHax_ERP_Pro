import sys
import datetime
import time
from datetime import datetime
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QLabel, QComboBox,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt
from WorkRecordFormDialog import WorkRecordFormDialog



class WorkRecordManagementWidget(QWidget):
    def __init__(self, main_window, db_manager):
        super().__init__()
        self.main_window = main_window
        self.db_manager = db_manager
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #=======================================================
        # Create search box
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入员工姓名或项目进行搜索")
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.load_data()

        # Search box triggers query on input
        self.search_input.textChanged.connect(self.search_work_records)

        # Create buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加工时记录")
        self.delete_btn = QPushButton("删除工时记录")
        self.back_btn = QPushButton("返回")
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)
        self.layout.addLayout(button_layout)

        self.add_btn.clicked.connect(self.add_work_record)
        self.delete_btn.clicked.connect(self.delete_work_record)
        self.back_btn.clicked.connect(self.main_window.show_main_page)
#=======================================================
    def load_data(self, filtered_records=None):
        rows = filtered_records if filtered_records else self.db_manager.fetch_work_records()
        employees = self.db_manager.fetch_all_employees()

        # 按员工ID合并工时
        aggregated_records = {}
        for row in rows:
            employee_id = row[1]
            total_hours = row[3]  # 总工时

            if employee_id in aggregated_records:
                # 合并总工时
                aggregated_records[employee_id][3] += total_hours
            else:
                aggregated_records[employee_id] = list(row)  # 保持其他字段不变

        # 将合并后的记录存入 rows
        rows = list(aggregated_records.values())

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["员工ID", "员工姓名", "日期", "总工时", "项目", "查看详情", "备注"])

        for row_idx, row_data in enumerate(rows):
            #print(f"填充行 {row_idx}: {row}")  # 调试信息


            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))  # 员工ID
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1]))) # 员工姓名
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2])))  # 日期
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row_data[3])))  # 总工时
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row_data[4])))  # 项目
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row_data[5])))  # 备注

            # 添加“查看”按钮
            button = QPushButton("查看")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #E0E0E0;
                    border: none;
                    padding: 5px;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #FF6347;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #FF4500;
                    color: white;
                }
            """)
            #button.clicked.connect(lambda checked, emp_id=employee_id: self.show_employee_work_records(emp_id))
            button.clicked.connect(lambda checked, emp_id=row_data[0]: self.show_detailed_work_records(emp_id))
 
            self.table.setCellWidget(row_idx, 5, button)

        self.table.setColumnWidth(6, 960)
        self.table.setColumnWidth(0, 105)
#==============================================
    def show_detailed_work_records(self, employee_id):
        # 获取员工的工时详细记录
        work_records = self.db_manager.fetch_work_records_by_employee(employee_id)
        if not work_records:
            QMessageBox.warning(self, "警告", "该员工没有工时记录！")
            return

        # 新建一个对话框来展示详细信息
        dialog = QDialog(self)
        dialog.setWindowTitle(f"详细工时记录 - 员工 {employee_id}")
        dialog.resize(1200, 600)
        layout = QVBoxLayout(dialog)

        # 创建一个表格显示详细信息
        work_table = QTableWidget(dialog)
        work_table.setRowCount(len(work_records))
        work_table.setColumnCount(6)  # 新增列：上班时间和下班时间
        work_table.setHorizontalHeaderLabels(["日期", "上班时间", "下班时间", "项目", "工时", "备注"])

        for row_idx, row in enumerate(work_records):
            employee_id, employee_name, date, start_time, end_time, total_hours, project, all_remarks = row

            work_table.setItem(row_idx, 0, QTableWidgetItem(str(date)))  # 日期
            work_table.setItem(row_idx, 1, QTableWidgetItem(str(start_time)))  # 上班时间
            work_table.setItem(row_idx, 2, QTableWidgetItem(str(end_time)))  # 下班时间
            work_table.setItem(row_idx, 3, QTableWidgetItem(str(project)))  # 项目
            work_table.setItem(row_idx, 4, QTableWidgetItem(str(total_hours)))  # 工时
            work_table.setItem(row_idx, 5, QTableWidgetItem(str(all_remarks)))  # 备注

            # 调整备注列宽度
            work_table.setColumnWidth(5, 660)

        layout.addWidget(work_table)

        # 添加关闭按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Close, Qt.Horizontal)
        close_button = buttons.button(QDialogButtonBox.Close)
        close_button.setText("关闭")
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()


#======================================
    def search_work_records(self):
        search_text = self.search_input.text().lower()
        all_records = self.db_manager.fetch_work_records()

        # 如果搜索框为空，直接返回所有记录
        if not search_text:
            self.load_data(all_records)
            return

        filtered_records = []
        for record in all_records:
            employee_name = str(record[1]).lower()  # 员工姓名
            project = str(record[4]).lower()  # 项目
            date = str(record[2]).lower()  # 日期

            # 如果搜索文本匹配任意字段，加入过滤结果
            if search_text in employee_name or search_text in project or search_text in date:
                filtered_records.append(record)

        self.load_data(filtered_records)

    def add_work_record(self):
        # 创建添加工时记录的对话框
        dialog = WorkRecordFormDialog(self.db_manager)
    
        # 如果用户点击确认，获取数据
        if dialog.exec_():
            data = dialog.get_data()
        
            # 如果数据存在并且正确
            if data:
                # 假设 data 是一个元组，直接解包传递给插入方法
                self.db_manager.insert_work_record(*data)  # 解包元组
                self.load_data()  # 重新加载数据

    def delete_work_record(self):
        # 获取选中的行
        selected_rows = list(set(index.row() for index in self.table.selectedIndexes()))  # 获取所有选中的行
    
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要删除的工时记录！")
            return

        # 确认删除操作
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("确认删除")
        msg_box.setText("确定要删除选中的工时记录吗？")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    
        # 修改按钮文本
        msg_box.button(QMessageBox.Yes).setText("是")
        msg_box.button(QMessageBox.No).setText("否")
    
        # 显示对话框并获取用户选择
        confirm = msg_box.exec()

        if confirm == QMessageBox.No:
            return

        # 遍历选中的行，获取员工ID和日期，删除对应的工时记录
        for row_idx in selected_rows:
            employee_id = self.table.item(row_idx, 0).text()  # 员工ID
            date = self.table.item(row_idx, 2).text()  # 日期
        
            # 调用数据库管理器删除记录
            self.db_manager.delete_work_record_by_employee_and_date(employee_id, date)

        # 重新加载数据
        self.load_data()
        QMessageBox.information(self, "删除成功", "选中的工时记录已删除！")
