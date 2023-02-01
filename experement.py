
import schedule
import time
from main import *
from worker import *

schedule.every().day.at("00:01").do(insert())
schedule.every().hour.do(create_consumtion())

while True:
    schedule.run_pending()
    time.sleep(1200)