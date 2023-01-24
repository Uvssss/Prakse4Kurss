import requests
import json
from datetime import datetime,timedelta
from main import *
from worker import *
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
        msg=sSplit+ ' ' + '-' + ' ' + eSplit+ ' ' + 'Value: ' + dayData[ 'Value']
        # print (msg)
        sSplit=startime - timedelta(days=1)
        eSplit=endtime - timedelta(days=1)
        value=dayData['Value'].replace(",",".")
        value=float(value)
        converted_val=value/1000
        insert_nordpool_prices(sSplit,eSplit,converted_val)
        create_consumtion(sSplit,eSplit)