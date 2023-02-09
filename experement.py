
import schedule
import time
from main import *
from worker import *

schedule.every().day.at("00:00").do(insert)

check=bool(select_prices())
if check== False:
    insert()
while True:
    schedule.run_pending()
    time.sleep(10)