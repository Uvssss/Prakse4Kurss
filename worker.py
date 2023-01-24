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
        # Dabū šodienas datumu
        now=datetime.now()
        # Pārmaina datuma formātu un datu tipu uz string un formatu uz YYYY-MM-DD
        dateOfInterest = now.strftime('%Y-%m-%d')
        # Iepriekšējais string datu tips tiek mainīts uz datetime datu tipu, ar iepriekš iznāmu formātu
        datetime_object = datetime.strptime(dateOfInterest, '%Y-%m-%d')
        # Tiek izveidots query, ar mainīgo kas tiks nākamajā ievadīts
        sql_select_Query = "select startime,endtime,price,electricty_id from prices where left(startime,10)= left(%s,10)"
        # Sagatavo savienojumu ar datubazi un python
        cursor = connection.cursor()
        # Palaiz izveidoto query ar izveidotiem datiem
        cursor.execute(sql_select_Query,((datetime_object),))
            # get all records
        records = cursor.fetchall()
        # Padod tālāk datus
        return records
    except mysql.connector.Error as e:
        # Izvada kļūdas ja ir
        logger.error("Error using select_prices", e)

def create_consumtion(startime,endtime):
    try:
        cursor = connection.cursor()
        consumntion=random.randint(10,100)
        mySql_insert_query = """INSERT INTO electricity_used (`startime`,`endtime`,used) 
	                                            VALUES (%s, %s, %s) """       
        record = (startime,endtime,consumntion)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        logger.info(" inserted successfully")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))     

def select_consumption():
    try:
        # Dabū šodienas datumu
        now=datetime.now()
        # Pārmaina datuma formātu un datu tipu uz string un formatu uz YYYY-MM-DD
        dateOfInterest = now.strftime('%Y-%m-%d')
        # Iepriekšējais string datu tips tiek mainīts uz datetime datu tipu, ar iepriekš iznāmu formātu
        datetime_object = datetime.strptime(dateOfInterest, '%Y-%m-%d')
        # Tiek izveidots query, ar mainīgo kas tiks nākamajā ievadīts
        sql_select_Query = "select startime,endtime,used from electricity_used where left(startime,10)= left(%s,10)"
        # Sagatavo savienojumu ar datubazi un python
        cursor = connection.cursor()
        # Palaiz izveidoto query ar izveidotiem datiem
        cursor.execute(sql_select_Query,(datetime_object,))
            # get all records
        records = cursor.fetchall()
        # Padod tālāk datus
        return records
    except mysql.connector.Error as e:
        # Izvada kļūdas ja ir
        logger.error("Error using select_consumption", e)

def automaticsaving(prices,consumption):
    fixed_cost = config.get('fixed_price', 'fixed_LV_price')
    fixed_list=[]
    nordpool_list=[]
    for i in consumption:
        cost=int(i[2])
        fixed_price=cost*float(fixed_cost)
        temp_list=[i[0],i[1],fixed_price,2]
        fixed_list.append(temp_list)
    for x in range(0,len(prices)):
        cost=int(consumption[x][2])
        nordpool_price=cost*float(prices[x][2])
        temp_list1=[prices[x][0],prices[x][1],nordpool_price,prices[x][3]]
        nordpool_list.append(temp_list1)
    print(nordpool_list)
    print(fixed_list)
        
        
    

#  Create math function from previous values
#  Convert nordpool EUR/MWH to eur/kwh get from config constant price and amount for the hour
#  in this function check what is cheaper  and how much cheaper it is. get the difference from both amounts, add that to saved column in electricity_connection
#  create function that inserts amount used with random int, put run then function in experement.py at the where they do the insert
