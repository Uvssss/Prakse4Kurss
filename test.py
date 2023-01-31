from worker import *
from main import *
import requests
from datetime import datetime,timedelta
# prices=select_prices()
# consumption=select_consumption()
# # saved_list=automaticsaving(prices,consumption,3)
# # print(saved_list)
# # # insert_saved_list(saved_list)

response = requests.get('https://www.nordpoolgroup.com/api/marketdata/page/59?currency=,,,EUR')
jayson = json.loads (response.text)
min_date=jayson["data"]["Rows"][24]["EndTime"].replace("T"," ")
max_date=jayson["data"]["Rows"][25]["EndTime"].replace("T"," ")

max_date_obj = datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S')
min_date_obj = datetime.strptime(min_date, '%Y-%m-%d %H:%M:%S')

min_date=min_date_obj - timedelta(days=1)
max_date= max_date_obj- timedelta(days=1)


create_consumtion()

# lowest=get_lowest(min_date)
# highest=get_highest(max_date)

# battery=select_bateryinfo(3)
# # saved_list=automaticsaving(prices,consumption,battery,lowest,highest)

# # insert_saved_list(saved_list)

# automaticsaving(prices,consumption,battery,lowest,highest)




