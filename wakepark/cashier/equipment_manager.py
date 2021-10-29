from datetime import datetime, timedelta, timezone


# class EquipmentException(BaseException):
#     def __init__(self, message):
#         self.message = message


class EquipmentManager:
    def __init__(self, units_number):
        self.units_number = units_number
        self.units = [EquipmentUnit() for i in range(units_number)]
        self.countdowns = [''] * units_number
        self.units_statuses = [0] * units_number

    def add_unit(self):
        self.units.append(EquipmentUnit())
        self.countdowns.append('')
        self.units_statuses.append(0)
        self.units_number += 1

    def remove_unit(self):
        del self.units[-1]
        del self.countdowns[-1]
        del self.units_statuses[-1]
        self.units_number -= 1

    def recalculate_units_time(self):
        for unit in self.units:
            unit.recalculate_time()

    def update_statuses_and_countdowns(self):
        self.recalculate_units_time()
        new_units_statuses = []
        new_countdowns = []
        for unit in self.units:
            new_countdowns.append(unit.time_left_str)
            new_units_statuses.append(unit.status)
        self.countdowns = new_countdowns
        self.units_statuses = new_units_statuses

    def reset_unit_status(self, unit_serial: int):
        self.units[unit_serial].reset_status()

    def init_timer(self, unit_serial: int, timedelta_minutes: int):
        self.units[unit_serial].init_timer(timedelta_minutes)


class EquipmentUnit:
    def __init__(self):
        self.init_time = None
        self.end_time = None
        '''
        statuses:
        0 - a boat is not used
        1 - a boat was given, timer was set
        2 - overtime
        '''
        self.status = 0
        self.time_left = None
        self.time_left_str = ''

    # def __set_status(self, status_code):
    #     if status_code in [0, 1, 2]:
    #         self.status = status_code
    #     else:
    #         raise EquipmentException('Incorrect status code for equipment unit')

    def init_timer(self, timedelta_minutes: int):
        self.init_time = datetime.now(timezone(timedelta(hours=3)))
        self.end_time = self.init_time + timedelta(minutes=timedelta_minutes)
        self.status = 1

    # def check_status(self):
    #     status_code = 1 if datetime.now(timezone(timedelta(hours=3))) < self.end_time else 2
    #     self.status = status_code
    #     return self.status

    def reset_status(self):
        self.status = 0
        self.init_time = None
        self.end_time = None
        self.time_left = None
        self.time_left_str = ''

    def recalculate_time(self):
        now_time = datetime.now(timezone(timedelta(hours=3)))
        if self.status == 0:
            return
        elif now_time < self.end_time:
            self.time_left = self.end_time - now_time
            self.status = 1
            prefix = ''
        else:
            self.time_left = now_time - self.end_time
            self.status = 2
            prefix = '-'
        hours_left = self.time_left.seconds // 3600
        minutes_left = (self.time_left.seconds - hours_left * 3600) // 60
        self.time_left_str = f'{prefix}{hours_left}:{minutes_left}'



