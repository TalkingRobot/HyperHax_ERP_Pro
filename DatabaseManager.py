import sys
import time
from datetime import datetime
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QLabel, QComboBox
)
from PyQt5.QtWidgets import QCalendarWidget


# 数据库操作封装
class DatabaseManager:
    def __init__(self, db_name="company.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)
        
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT
            )
        """)



        conn.commit()
        conn.close()

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT,
                phone TEXT,
                salary_type TEXT NOT NULL,
                salary_rate REAL NOT NULL,
                hire_date TEXT,
                remarks TEXT
            )
            ''')
            # 修改部分：添加 start_time 和 end_time 字段
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                employee_name TEXT NOT NULL, 
                date TEXT NOT NULL,
                hours REAL NOT NULL,
                start_time TEXT,   -- 新增字段
                end_time TEXT,     -- 新增字段
                project TEXT,
                remarks TEXT,
                FOREIGN KEY(employee_id) REFERENCES employees(id)
            )
            ''')
            conn.commit()

    # 修改部分：动态添加上下班时间字段
    def add_columns_to_work_records(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("ALTER TABLE work_records ADD COLUMN start_time TEXT")
                cursor.execute("ALTER TABLE work_records ADD COLUMN end_time TEXT")
            except sqlite3.OperationalError:
                # 如果字段已经存在，忽略错误
                pass
            conn.commit()


    def fetch_all_employees(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, position, phone, salary_type, salary_rate, hire_date, remarks FROM employees")
            rows = cursor.fetchall()
        return rows

    def fetch_work_records_by_employee(self, employee_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT employee_id, employee_name, date, start_time, end_time, SUM(hours) AS total_hours, project, GROUP_CONCAT(remarks, ", ") AS all_remarks
                FROM work_records
                WHERE employee_id = ?
                GROUP BY date, project
                ORDER BY date ASC
            ''', (employee_id,))
            rows = cursor.fetchall()
        return rows

    def insert_employee(self, data):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO employees (name, position, phone, salary_type, salary_rate, hire_date, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()

    def delete_employee(self, employee_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
            conn.commit()

    def fetch_work_records(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM work_records")
            rows = cursor.fetchall()
        return rows

    # 修改部分：更新插入工时记录方法，添加上下班时间字段
    def insert_work_record(self, employee_id, date, hours, start_time, end_time, project, remarks):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM employees WHERE id = ?', (employee_id,))
            employee_name_result = cursor.fetchone()

            employee_name = employee_name_result[0] if employee_name_result else "未知员工"

            cursor.execute('''
            INSERT INTO work_records (employee_id, employee_name, date, hours, start_time, end_time, project, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employee_id, employee_name, date, hours, start_time, end_time, project, remarks))
            conn.commit()
            

    def delete_work_record(self, record_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM work_records WHERE id=?", (record_id,))
            conn.commit()

    def delete_work_record_by_employee_and_date(self, employee_id, date):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM work_records WHERE employee_id = ? AND date = ?", (employee_id, date))
            conn.commit()


#-----------------------------------------------------

    def fetch_schedule_data(self):
        # 示例：从数据库获取排班数据
        return [
            (1, "张三", "2024-01-01 09:00"),
            (2, "李四", "2024-01-01 10:00")
        ]

    def fetch_flow_data(self):
        # 示例：从数据库获取公司流水数据
        return [
            (1, "2024-01-01", 1000, "销售收入"),
            (2, "2024-01-02", -500, "采购支出")
        ]

    def fetch_warehouse_data(self):
        # 示例：从数据库获取仓库物流数据
        return [
            (1, "商品A", 100, "已发货", "2024-01-01"),
            (2, "商品B", 50, "待发货", "2024-01-02")
        ]
#----------------------------------
    def create_tables(self):
        # 使用数据库连接和游标，而不是 self.cursor
        with self.connect() as conn:
            cursor = conn.cursor()  # 每次都创建新的 cursor
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    position TEXT,
                    phone TEXT,
                    salary_type TEXT,
                    salary_rate REAL,
                    join_date TEXT,
                    remark TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    address TEXT,
                    email TEXT,
                    remark TEXT
                )
            """)
            conn.commit()

    def fetch_all_customers(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
        return rows

    def add_customer(self, name, phone, address, email, remark):
        self.cursor.execute("""
        INSERT INTO customers (name, phone, address, email, remark)
        VALUES (?, ?, ?, ?, ?)
        """, (name, phone, address, email, remark))
        self.conn.commit()

    def delete_customer(self, customer_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            conn.commit()
    def add_columns_to_work_records(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("ALTER TABLE work_records ADD COLUMN start_time TEXT")
                cursor.execute("ALTER TABLE work_records ADD COLUMN end_time TEXT")
            except sqlite3.OperationalError:
                # 如果字段已经存在，忽略错误
                pass
            conn.commit()



    def create_holidays_table():
        # Connect to your database (replace 'database.db' with your database file)
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()

        # SQL query to create the holidays table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT,
            start_date TEXT,
            end_date TEXT
        );
        '''

        # Execute the query
        cursor.execute(create_table_query)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    # Call the function to create the table
    create_holidays_table()


    def fetch_all_holidays(self):
        # Fetch all holiday data from the database
        query = "SELECT * FROM holidays"
        # Execute the query and return the result
        return self.execute_query(query)

    def add_holiday(self, employee_name, start_date, end_date):
        # Insert a new holiday record into the database
        query = f"INSERT INTO holidays (employee_name, start_date, end_date) VALUES ('{employee_name}', '{start_date}', '{end_date}')"
        # Execute the query to insert
        self.execute_query(query)

    def execute_query(self, query):
        # Helper function to execute the queries and return results
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor.fetchall()

            