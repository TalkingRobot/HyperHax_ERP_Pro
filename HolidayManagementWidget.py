from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QFormLayout, QLineEdit, QLabel
from PyQt5.QtCore import QDate
import sqlite3
from PyQt5.QtGui import QIcon  # 导入 QIcon 类
from PyQt5.QtWidgets import QHBoxLayout
from AddHolidayDialog import AddHolidayDialog  # 确保正确导入 AddHolidayDialog 类


class HolidayManagementWidget(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent = parent
        self.setWindowTitle("假期管理")
        self.setWindowIcon(QIcon("v_preview.png"))  # 添加图标

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 添加搜索框
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入员工ID或姓名进行搜索")
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)




        # Initialize the table for displaying holidays
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.load_holiday_data()

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Button to add a new holiday
        self.add_holiday_btn = QPushButton("添加假期")
        button_layout.addWidget(self.add_holiday_btn)
        self.add_holiday_btn.clicked.connect(self.add_holiday)

        # Button to delete a holiday
        self.delete_holiday_btn = QPushButton("删除假期")
        button_layout.addWidget(self.delete_holiday_btn)
        self.delete_holiday_btn.clicked.connect(self.delete_holiday)

        # Button to go back to the main screen
        self.back_btn = QPushButton("返回")
        button_layout.addWidget(self.back_btn)
        self.back_btn.clicked.connect(self.back_to_main)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

    def load_holiday_data(self):
        """
        加载假期数据到表格。
        """
        rows = self.db_manager.fetch_all_holidays()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(4)  # ID, Employee, Holiday Start, Holiday End
        self.table.setHorizontalHeaderLabels(["ID", "员工", "假期开始", "假期结束"])

        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def add_holiday(self):
        dialog = AddHolidayDialog(self)  # 确保导入了 AddHolidayDialog 类
        dialog.exec_()
        
    def delete_holiday(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "警告", "请选择要删除的假期！")
            return
        holiday_id = self.table.item(selected, 0).text()
        self.db_manager.delete_holiday(holiday_id)
        self.load_holiday_data()  # 重新加载所有数据

    def back_to_main(self):
        self.parent.show_main_page()  # 调用 MainWindow 中的 show_main_page 方法
        self.close()  # 关闭当前窗口
