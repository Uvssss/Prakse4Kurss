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

def create_consumtion():
    try:
        cursor = connection.cursor()
        consumption=random.uniform(10,60)
        now=datetime.now()
        dateOfInterest = now.strftime('%Y-%m-%d %H:%M:%S')
        startime = datetime.strptime(dateOfInterest, '%Y-%m-%d %H:%M:%S')
        endtime = startime + timedelta(hours=1)
        endtime=endtime.strftime('%Y-%m-%d %H:00:00')
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

        sql_select_Query = "select startime,endtime,max(price),electricty_id from prices where left(startime,10)=left(%s,10);"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(value,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)

def get_lowest(value):
    try:
        sql_select_Query = "select startime,endtime,min(price),electricty_id from prices where left(startime,10)=left(%s,10);"
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

def append_new_battery(id,):
    try:
        if bool(config.get('battery', 'capacity')) == False:
            capacity=float(input("Input battery Capacity: "))
            chargepower=float(input("Input battery Charge Power: "))
        if bool(config.get('battery', 'capacity')) == True:
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

def insert_battery_info(id,status):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO battery_info (`id`,`startime`,`endtime`,`capacity`,`KW`,`price`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s) """  
        now=datetime.now()
        dateOfInterest = now.strftime('%Y-%m-%d %H:%M:%S')
        startime = datetime.strptime(dateOfInterest, '%Y-%m-%d %H:%M:%S')
        endtime = startime + timedelta(hours=1)
        endtime=endtime.strftime('%Y-%m-%d %H:00:00')             
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
            kw=random.uniform(1,10)
            record = (id,startime,endtime,cap[0][0],kw,price[0][0],0)
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            logger.info("inserted successfully")

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error)) 
# hopefully done


def battery_controller():
    try:
        a=True
        cursor = connection.cursor()
        id="""select battery.id, name from battery 
            inner join electricity on electricity.id=battery.id"""
        cursor.execute(id)
        main_records = cursor.fetchall()
        while a==True:
            print("If you want to create a new battery write 'new' ")
            for row in main_records:
                print("id = ", row[0], )
                print("name = ", row[1])
            id=input("input battery id : ")
            if id=="new":
                    electricity()
                    new_id="""select id from electricity order by id desc limit 1"""
                    cursor.execute(new_id)
                    records = cursor.fetchall()
                    append_new_battery(records[0][0])
                    id=records[0][0]
                    a=False
            for row in main_records:
                if int(id)==int(row[0]):
                    a=False
            print(id)

        #  we got id

    # current cup, max cup, charge power,minmaxprice, consumption
    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))