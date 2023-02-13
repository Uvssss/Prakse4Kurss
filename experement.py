
import schedule
from main import *
from worker import *

schedule.every().day.at("00:00").do(insert)
check=bool(select_prices())
if check== False:
    append_new_battery(3)
    insert()
while True:
    schedule.run_pending()
    time.sleep(10)