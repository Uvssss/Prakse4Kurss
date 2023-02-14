
import schedule
from main import *
from worker import *

schedule.every().day.at("00:00").do(insert)
check=bool(select_prices())
bat_check=bool(check_battery(3))
if check== False:
    if bat_check==False:
        append_new_battery(3)
        insert()
    else:
        insert()
while True:
    schedule.run_pending()
    time.sleep(10)