from main import *
config = ConfigParser()
config.read('config.ini')
mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')
connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)
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

# Gets all values that match todays date
def select_prices():
    try:
        now=datetime.now()
        dateOfInterest = now.strftime('%Y-%m-%d')
        datetime_object = datetime.strptime(dateOfInterest, '%Y-%m-%d')
        sql_select_Query = "select * from prices where left(startime,10)= left(%s,10)"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(datetime_object,))
            # get all records
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_hourly", e)

#  Create math function from previous values
#  Convert nordpool EUR/MWH to eur/kwh get from config constant price and amount for the hour
#  in this function check what is cheaper  and how much cheaper it is. get the difference from both amounts, add that to saved column in electricity_connection
#  create function that inserts amount used with random int, put run then function in experement.py at the where they do the insert
