from worker import *
from main import *
from worker import *
import requests
from datetime import datetime,timedelta

insert()
append_new_battery(3)
battery_controller(3)

# max_cap="select max_capacity from battery where id = 3"
# cursor = connection.cursor()
# cursor.execute(max_cap)
# records = cursor.fetchall()
# print(records)
# now=datetime.now()
# dateOfInterest = now.strftime('%Y-%m-%d %H:%M:%S')
# startime = datetime.strptime(dateOfInterest, '%Y-%m-%d %H:%M:%S')
# select_consumption('2023-02-07 11:50:38')
# get_consumption('2023-02-07 12:21:16')
# print(bool(select_battery_info(3)))
# select_battery_info(3)
# get_battery_sum(3,startime)

# insert_battery_info(3,0)