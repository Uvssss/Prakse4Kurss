import requests
import json
from datetime import datetime
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
        msg=sSplit+ ' ' + '-' + ' ' + eSplit+ ' ' + 'Value: ' + dayData[ 'Value']
        print (msg)
        value=dayData['Value'].replace(",",".")
        insert_nordpool_prices(sSplit,eSplit,value)
