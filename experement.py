import requests
import json
from datetime import datetime,timedelta
import schedule
import time
from main import *
from worker import *

def insert():        
    print('start')
    now=datetime.now()
    response = requests.get('https://www.nordpoolgroup.com/api/marketdata/page/59?currency=,,,EUR')
    dateOfInterest = now.strftime('%d-%m-%Y')

    jayson = json.loads (response.text)
    config = ConfigParser()
    config.read('config.ini')
    mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
    mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
    mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
    mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')
    connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)
    # Loading logging configuration
    logger = logging.getLogger('root')

    for row in jayson ['data']['Rows'] :
        if row['IsExtraRow']:
            continue
        for dayData in row[ 'Columns']:
            if (dayData[ 'Name'] != dateOfInterest):
                continue
            sSplit = row[ 'StartTime'].replace('T', ' ')  
            eSplit = row[ 'EndTime'].replace('T', ' ')    
            startime=datetime.strptime(sSplit,"%Y-%m-%d %H:%M:%S")
            endtime=datetime.strptime(eSplit,"%Y-%m-%d %H:%M:%S")
            value=dayData['Value'].replace(",",".")
            value=float(value)
            converted_val=value/1000
            insert_nordpool_prices(sSplit,eSplit,converted_val)
            # consumption_item(startime)
            # consumption=item_consumption(startime)
            
            
            
            # create_consumtion(startime,endtime,consumption)


    prices=select_prices()
    consumption=select_consumption()

    lowest=get_lowest(startime)
    highest=get_highest(startime)
    
    battery=select_bateryinfo(3)
    saved_list=automaticsaving(prices,consumption,battery,lowest,highest)
    insert_saved_list(saved_list)




schedule.every().day.at("00:01").do(insert)

# schedule.every().hour.do()


while True:

    schedule.run_pending()
    time.sleep(1)