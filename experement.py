import requests
import json
from datetime import datetime
from main import *
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

def insert_nordpool_prices(starttime,endtime,price):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO prices (`startime`,`endtime`,price,electricty_id) 
	                                            VALUES (%s, %s, %s,%s) """       
        record = (starttime,endtime,price,1)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        logger.info(" inserted successfully in current")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))



def insert_other_prices(starttime,endtime,price):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO Electricity (`time`,humid,temp,sensor_id) 
	                                            VALUES (%s, %s, %s,%s) """       
        record = ()
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        logger.info(" inserted successfully in current")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))        
        
        
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
        insert_nordpool_prices(sSplit,eSplit, dayData[ 'Value'])