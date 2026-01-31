from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QCalendarWidget, QLabel, QDialog,
    QPushButton, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect


class ScheduleCalendar(QCalendarWidget):
    def __init__(self, schedule_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule_data = schedule_data
        self.header_height = 20  # 设置灰色表头区域的固定高度（可以调整此数值）






    def paintCell(self, painter, rect, date):
        header_height = self.header_height
        header_rect = QRect(rect.x(), rect.y(), rect.width(), header_height)
        remaining_rect = rect.adjusted(0, header_height, 0, -header_height)

        painter.setPen(Qt.transparent)
        painter.drawRect(rect)

        if date != QDate.currentDate():
            painter.fillRect(header_rect, QColor(250, 250, 250))
        else:
            painter.fillRect(header_rect, QColor("lightblue"))

        painter.setFont(QFont("Arial", 10))
        painter.setPen(QColor("black"))

        if date == QDate.currentDate():
            painter.drawText(header_rect, Qt.AlignHCenter | Qt.AlignVCenter, "今天")
        else:
            painter.drawText(header_rect, Qt.AlignHCenter | Qt.AlignVCenter, date.toString("d"))

        date_str = date.toString("yyyy-MM-dd")
        if date_str in self.schedule_data:
            self.draw_schedule_info(painter, remaining_rect, self.schedule_data[date_str])

    def draw_schedule_info(self, painter, rect, info):
        working = info.get("working", [])
        on_leave = info.get("on_leave", [])

        all_employees = ["张三", "李四", "王五", "赵六", "刘七"]
        total_employees = len(all_employees)
        working_count = len(working)

        painter.setFont(QFont("Arial", 9))
        metrics = painter.fontMetrics()
        line_height = metrics.height()
        y_offset = 5

        text = f"出勤 ： {working_count}/{total_employees}"
        painter.setPen(QColor("purple"))
        painter.drawText(rect.adjusted(5, y_offset, -5, 0), Qt.AlignLeft | Qt.AlignTop, text)
        y_offset += line_height + 5

        if on_leave:
            leave_text = "休假 ： " + ", ".join(on_leave)
            painter.setPen(QColor("darkorange"))
            painter.drawText(rect.adjusted(5, y_offset, -5, 0), Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, leave_text)
        else:
            leave_text = "休假 ： 无"
            painter.setPen(QColor("gray"))
            painter.drawText(rect.adjusted(5, y_offset, -5, 0), Qt.AlignLeft | Qt.AlignTop, leave_text)



class ScheduleWidget(QWidget):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)  # 确保 parent 参数传递给 QWidget
        self.parent = parent
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 示例排班数据
        self.schedule_data = {
            "2024-12-29": {"working": ["张三", "李四"], "on_leave": ["王五"]},
            "2024-12-30": {"working": ["赵六"], "on_leave": ["张三"]},
        }

        # 搜索框布局
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入员工姓名进行搜索")
        self.search_input.textChanged.connect(self.search_schedule)
        self.search_layout.addWidget(self.search_input)
        layout.addLayout(self.search_layout)

        # 自定义日历组件
        self.calendar = ScheduleCalendar(self.schedule_data)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.show_day_details)
        layout.addWidget(self.calendar)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 添加记录按钮
        add_button = QPushButton("添加排班记录")
        add_button.clicked.connect(self.add_record)
        button_layout.addWidget(add_button)

        # 删除记录按钮
        delete_button = QPushButton("删除排班记录")
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(delete_button)

        # 返回按钮
        return_button = QPushButton("返回")
        return_button.clicked.connect(self.return_to_main)
        button_layout.addWidget(return_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_record(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        name, ok = self.get_input_dialog("添加记录", "请输入员工姓名：")
        if ok and name.strip():
            if date not in self.schedule_data:
                self.schedule_data[date] = {"working": [], "on_leave": []}
            self.schedule_data[date]["working"].append(name)
            self.calendar.update()  # 更新日历
            QMessageBox.information(self, "添加成功", f"已为 {date} 添加员工 {name} 的记录！")
        else:
            QMessageBox.warning(self, "输入错误", "员工姓名不能为空！")

    def delete_record(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        name, ok = self.get_input_dialog("删除记录", "请输入要删除的员工姓名：")
        if ok and name.strip():
            if date in self.schedule_data and name in self.schedule_data[date]["working"]:
                self.schedule_data[date]["working"].remove(name)
                self.calendar.update()  # 更新日历
                QMessageBox.information(self, "删除成功", f"已从 {date} 删除员工 {name} 的记录！")
            else:
                QMessageBox.warning(self, "记录不存在", f"未找到 {name} 在 {date} 的记录！")
        else:
            QMessageBox.warning(self, "输入错误", "员工姓名不能为空！")

    def show_day_details(self, date):
        """
        显示选中日期的排班和休假人员详情。
        """
        date_str = date.toString("yyyy-MM-dd")
        info = self.schedule_data.get(date_str, {"working": [], "on_leave": []})

        # 假设您有一个固定的员工名单，所有员工的列表
        all_employees = ["张三", "李四", "王五", "赵六", "刘七"]  # 示例员工名单
        total_employees = len(all_employees)

        # 上班人员数量
        working_count = len(info["working"])
        working_ratio = f"{working_count}/{total_employees}"

        # 休假人员
        on_leave = ", ".join(info["on_leave"]) or "无"

        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle(f"{date_str} 排班详情")
        detail_dialog.setFixedSize(400, 200)  # 设置窗口大小为宽400，高200
        detail_layout = QVBoxLayout()

        working_label = QLabel(f"上班人数: {working_ratio}")
        on_leave_label = QLabel(f"休假人员: {on_leave}")

        detail_layout.addWidget(working_label)
        detail_layout.addWidget(on_leave_label)

        close_button = QPushButton("关闭")
        close_button.clicked.connect(detail_dialog.accept)
        detail_layout.addWidget(close_button)

        detail_dialog.setLayout(detail_layout)
        detail_dialog.exec_()

    def search_schedule(self):
        """
        根据搜索框输入的员工姓名进行过滤，并更新显示。
        """
        search_text = self.search_input.text().lower()

        # 根据员工姓名过滤排班数据
        filtered_schedule = {}
        for date_str, info in self.schedule_data.items():
            working = [name for name in info["working"] if search_text in name.lower()]
            on_leave = [name for name in info["on_leave"] if search_text in name.lower()]
            if working or on_leave:
                filtered_schedule[date_str] = {"working": working, "on_leave": on_leave}

        self.calendar.schedule_data = filtered_schedule
        self.calendar.update()

    def get_input_dialog(self, title, label):
        """
        获取用户输入的通用对话框
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()

        input_label = QLabel(label)
        layout.addWidget(input_label)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(lambda: dialog.done(1))
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        if dialog.exec_() == 1:
            return input_field.text(), True
        else:
            return "", False


    def return_to_main(self):
        self.parent.show_main_page()
