from worker import *
from main import *
from worker import *
import requests
from datetime import datetime,timedelta

# insert()
# create_consumtion()
# append_new_battery(3)
# insert_battery_info(3,0)
# battery_controller()
# now=datetime.now()
# dateOfInterest = now.strftime('%Y-%m-%d %H:%M:%S')
# startime = datetime.strptime(dateOfInterest, '%Y-%m-%d %H:%M:%S')
# select_consumption(startime)
# print(bool(select_battery_info(3)))
select_battery_info(3)
get_battery_sum(3,'2023-02-06 13:12:08')