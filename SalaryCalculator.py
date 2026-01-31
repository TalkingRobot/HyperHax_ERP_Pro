class SalaryCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.basic_hourly_rate = 9620  # 基本时薪

    def calculate_salary_for_period(self, employee_id, start_date, end_date):
        work_records = self.db_manager.fetch_work_records()

        total_hours = 0
        overtime_hours = 0
        holiday_hours = 0
        regular_hours = 0

        for record in work_records:
            if record[1] == employee_id:  # 根据员工ID匹配
                work_date = datetime.strptime(record[2], "%Y-%m-%d")
                if start_date <= work_date <= end_date:
                    worked_hours = record[3]  # 工时

                    # 判断是否为加班或节假日
                    if worked_hours > 8:
                        overtime_hours += worked_hours - 8
                        regular_hours += 8
                    else:
                        regular_hours += worked_hours

                    if record[4] == "假期":
                        holiday_hours += worked_hours
                    else:
                        total_hours += worked_hours

        # 工资计算
        regular_salary = regular_hours * self.basic_hourly_rate
        overtime_salary = overtime_hours * self.basic_hourly_rate * 1.5
        holiday_salary = holiday_hours * self.basic_hourly_rate * 2

        return {
            "regular_salary": regular_salary,
            "overtime_salary": overtime_salary,
            "holiday_salary": holiday_salary,
            "total_salary": regular_salary + overtime_salary + holiday_salary,
        }
