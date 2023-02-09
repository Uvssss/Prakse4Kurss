from main import *
import requests
import json
from datetime import datetime,timedelta
config = ConfigParser()
config.read('config.ini')
mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')
connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)
logger = logging.getLogger('root')


def insert():        
    print('start')
    append_new_battery(3)
    now=datetime.now()
    response = requests.get('https://www.nordpoolgroup.com/api/marketdata/page/59?currency=,,,EUR')
    dateOfInterest = now.strftime('%d-%m-%Y')
    jayson = json.loads (response.text)

    for row in jayson ['data']['Rows'] :
        if row['IsExtraRow']:
            continue
        for dayData in row[ 'Columns']:
            if (dayData[ 'Name'] != dateOfInterest):
                continue
            sSplit = row[ 'StartTime'].replace('T', ' ')  
            eSplit = row[ 'EndTime'].replace('T', ' ')    
            value=dayData['Value'].replace(",",".") 
            sSplit = datetime.strptime(sSplit,"%Y-%m-%d %H:%M:%S") 
            eSplit = datetime.strptime(eSplit,"%Y-%m-%d %H:%M:%S") 
            sSplit=sSplit - timedelta(days=1)
            eSplit=eSplit - timedelta(days=1)
            value=float(value)
            converted_val=value/1000
            insert_nordpool_prices(sSplit,eSplit,converted_val)
            create_consumtion(sSplit,eSplit)
            battery_controller(sSplit,eSplit)
    total_cost(3)

def insert_nordpool_prices(starttime,endtime,price):
    try:
        fixed_cost = float(config.get('fixed_price', 'fixed_LV_price'))
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO prices (`startime`,`endtime`,`nord_price`,`static_price`) 
	                                            VALUES (%s,%s,%s,%s) """       
        record = (starttime,endtime,price,fixed_cost,)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        logger.info("inserted successfully")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))

def select_prices():
    try:
        now=datetime.now()
        dateOfInterest = now.strftime('%Y-%m-%d')
        datetime_object = datetime.strptime(dateOfInterest, '%Y-%m-%d')
        sql_select_Query = "select * from prices where left(startime,10)= left(%s,10)"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,((datetime_object),))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_prices", e)

def create_consumtion(startime,endtime):
    try:
        cursor = connection.cursor()
        consumption=random.uniform(10,60)
        mySql_insert_query = """INSERT INTO total_consumption (`startime`,`endtime`,consumption) 
	    VALUES (%s, %s, %s) """       
        record = (startime,endtime,consumption)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        logger.info("Inserted successfully")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))     

#  YYYY-MM-DD HH:MM:SS
#  2023-01-31 13:00:00
#  2023-01-31 14:00:00


def get_highest(value):
    try:

        sql_select_Query = "select max(best_price),startime from connection where left(startime,10)=left(%s,10) group by startime order by max(best_price) desc limit 1 ;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(value,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)

def get_lowest(value):
    try:
        sql_select_Query = "select min(best_price) as best_price,startime from connection where left(startime,10)=left(%s,10) group by startime order by best_price limit 1 ;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(value,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)

def electricity():
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO electricity (`name`) VALUES (%s) """       
        name=input("insert name")
        cursor.execute(mySql_insert_query, [name])
        connection.commit()
        logger.info("inserted successfully")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))

def append_new_battery(id):
    try:
            capacity=float(config.get('battery', 'capacity'))
            chargepower=float(config.get('battery', 'chargepower'))
            cursor = connection.cursor()       
            mySql_insert_query = """ insert into battery (`id`,`max_capacity`,`charge_power`) Values (%s,%s,%s) """       
            record = (id,capacity,chargepower)
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            logger.info("inserted successfully")         
    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))

def insert_battery_info(id,status,startime,endtime):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO battery_info (`id`,`startime`,`endtime`,`capacity`,`KW`,`price`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s) """  
        price = """select best_price from connection where left(startime,13)= left(%s,13) order by startime desc limit 1 """   
        cursor.execute(price, [startime])  
        price = cursor.fetchall()
        cap= """Select capacity from battery_info where left(startime,13)= left(%s,13) and id=%s order by startime DESC limit 1  """
        cursor.execute(cap, [startime,id])
        cap = cursor.fetchall()
        if bool(cap)== False:
            cap="select max_capacity from battery where id=%s"
            cursor.execute(cap, [id])
            cap = cursor.fetchall()
        if status==1:
            kw = """SELECT consumption FROM total_consumption where left(startime,13)= left(%s,13) order by startime DESC limit 1"""
            cursor.execute(kw, [startime])
            kw1 = cursor.fetchall()
            record = (id,startime,endtime,float(cap[0][0])-float(kw1[0][0]),kw1[0][0],price[0][0],1)
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            logger.info("inserted successfully")
        if status ==0:
            max_cap= select_battery(id)
            max_cap = max_cap[0][1]
            kw=random.uniform(1,25)
            if max_cap < cap[0][0]+kw:
                kw6=(cap[0][0]+kw)-max_cap               
                record = (id,startime,endtime,max_cap,kw6,price[0][0],0)
            else:
                record = (id,startime,endtime,cap[0][0]+kw,kw,price[0][0],0)
            cursor.execute(mySql_insert_query,record)
            connection.commit()
            logger.info("inserted successfully")
    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error)) 
# hopefully done
def select_battery_info(id):
    try:
        sql_select_Query = "select * from battery_info where id = %s and `status`= 0 order by endtime desc limit 1;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(id,))
        records = cursor.fetchall()
        return records
        # print(records)
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)
        
def get_battery_sum(id,startime):
    try:
        sql_select_Query = "select sum(kw) from battery_info where id = %s and `status`=0 and left(startime,10)=left(%s,10);"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(id,startime))
        records = cursor.fetchall()
        return records[0][0]
        # print(records)
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)

def select_battery(id):
    try:
        sql_select_Query = "select * from battery where id = %s limit 1"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(id,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e)

def select_connection(startime):
    try:
        sql_select_Query = "select * from connection where left(startime,10)= left(%s,10)"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(startime,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e) 

def connection_update(id, startime):
    try:
        sql_select_Query = "UPDATE `electricityprice`.`connection`SET `connection` = %s where left(startime,13)= left(%s,13)"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(id,startime))
        connection.commit()
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e) 

def get_consumption(startime):
    try:
        sql_select_Query = "select consumption from total_consumption where left(startime,10) = left(%s,10) order by startime desc limit 1;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(startime,))
        records = cursor.fetchall()
        return records[0][0]
        # print(records)
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e) 

def getprice(startime):
    try:
        cursor = connection.cursor()
        price="select best_price from connection where startime=%s order by startime desc limit 1"
        cursor.execute(price,(startime,))
        records = cursor.fetchall()
        return records[0][0]
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e)

def get_status(id,startime):
    try:
        cursor = connection.cursor()
        price="select status from battery_info where left(startime,10)=left(%s,10) and id=%s order by startime desc limit 1"
        cursor.execute(price,(startime,id))
        records = cursor.fetchall()
        return records[0][0]
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e)
def battery_controller(startime,endtime):
    try:
        max_price=get_highest(startime)
        min_price=get_lowest(startime)
        if max_price[0][1]==startime:
            connection_update(id, startime)
            insert_battery_info(3,1,startime,endtime)
        if min_price[0][1]==startime:
            insert_battery_info(3,1,startime,endtime)
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e)

def get_dates(startime):
    try:
        cursor = connection.cursor()
        price="select startime,endtime from connection left(startime,10)=left(%s,10) "
        cursor.execute(price,(startime))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e)


def total_cost(id):
    # startime v endtime V           price v consumption v expenses, ja status 0 get battery consumption add it to total consump
    try:
        now=datetime.now()
        dateOfInterest = now.strftime('%Y-%m-%d')
        datetime_object = datetime.strptime(dateOfInterest, '%Y-%m-%d')
        dates=get_dates(datetime_object)
        for i in range(0,len(dates)):
            startime=dates[i][0]
            endtime=dates[i][1]
            price=getprice(startime)
            consumption=get_consumption(startime)
            status=get_status(id,startime)
            battery_consumption=get_battery_sum(id,startime)
            if status==1:
                cursor = connection.cursor()
                mySql_insert_query = """INSERT INTO total_cost (startime,endtime,price,consumption,expenses) 
                VALUES (%s,%s,%s,%s,%s) """  
                record = (startime,endtime,price,consumption,price*consumption)
                cursor.execute(mySql_insert_query, record)
                connection.commit()
                logger.info("inserted successfully")    
            if status==0:
                cursor = connection.cursor()
                mySql_insert_query = """INSERT INTO total_cost (startime,endtime,price,consumption,expenses) 
                VALUES (%s,%s,%s,%s,%s) """       
                record = (startime,endtime,price,consumption+battery_consumption,price*(consumption+battery_consumption))
                cursor.execute(mySql_insert_query, record)
                connection.commit()
                logger.info("inserted successfully")    
    except mysql.connector.Error as e:
        logger.error("Error using select_batery_info", e) 