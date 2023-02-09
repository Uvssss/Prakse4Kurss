
import schedule
import time
from main import *
from worker import *

schedule.every().day.at("00:00").do(insert)
schedule.every().hour.do(battery_controller,3)

check=bool(select_prices())
if check== False:
    insert()
    append_new_battery(3)
    battery_controller(3)

while True:
    schedule.run_pending()
    time.sleep(10)