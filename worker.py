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
        logger.info("inserted successfully")    

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

def consumption_item(startime):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO electricity_item_used (`startime`,`electricity_used_item_id`,amount) 
	                                            VALUES (%s, %s, %s) """       
        for i in range(0,2):
            consumntion=random.randint(1,10)
            electricity_item_id=random.randint(1,3)
            record=[startime,electricity_item_id,consumntion]
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            logger.info(" inserted successfully")

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))     
def item_consumption(startime):
    try:
        sum=0
        sql_select_Query = "select amount from `electricity_item_used` where startime=%s;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(startime,))
        records = cursor.fetchall()
        for i in range(0,len(records)):
            for x in range(0,len(records[i])):
                sum=sum+records[i][x]
        return sum
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)

def create_consumtion(startime,endtime,consumntion):
    try:
        cursor = connection.cursor()
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

def get_highest(value):
    try:
        #  make a for loop that changes the endtime part of the list to -1 day so its possible to get that days lowest
        #  same with highest
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


def get_consumption(startime):
    try:
        sql_select_Query = "select used from electricity_used where startime = %s;"
        cursor = connection.cursor()
        record=[startime,]
        cursor.execute(sql_select_Query,record)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using electricity_used", e)

        
def insert_batteryinfo(startime,endtime,amount,charged,electricity_id):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """ insert into battery_info (startime,endtime,charge_amount,charge_power,electricty_id) values (%s,%s,%s,%s,%s) """       
        record = (startime,endtime,amount,charged,electricity_id)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        logger.info(" inserted successfully")    

    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))  

def automaticsaving(prices,consumption,battery,min_list,max_list):
    fixed_cost = config.get('fixed_price', 'fixed_LV_price')
    battery_capacity= config.get('battery', 'capacity')
    battery_chargepower= config.get('battery', 'chargepower')
    fixed_list=[]
    nordpool_list=[]
    saved_list=[]
   
    if bool(battery) == False:        
        for i in consumption: # Loop makes fixed prices list with consumption
            cost=int(i[2])
            fixed_price=cost*float(fixed_cost)
            temp_list=[i[0],i[1],fixed_price,2]
            fixed_list.append(temp_list)
            
        for x in range(0,len(prices)):
            cost=float(consumption[x][2])
            nordpool_price=cost*float(prices[x][2])
            temp_list1=[prices[x][0],prices[x][1],nordpool_price,prices[x][3]]
            nordpool_list.append(temp_list1)
        for index in range(0,len(nordpool_list)):
            if prices[index][2]==max_list[0][2]: 
                consump=get_consumption(prices[index][0])
                if float(consump[0][0])<float(battery_capacity) or float(consump[0][0])==float(battery_capacity):
                    difference=nordpool_list[index][2]
                    capacity=float(battery_capacity)-float(consump[0][0])
                    temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,3] 
                    saved_list.append(temp_list2)
                    insert_batteryinfo(nordpool_list[index][0],nordpool_list[index][1],capacity,0,3) 
                    continue
                if float(consump[0][0])>float(battery_capacity):
                    difference=fixed_list[index][2]-nordpool_list[index][2]
                    temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,nordpool_list[index][3]]
                    saved_list.append(temp_list2)
                    continue
            
            if nordpool_list[index][0] == fixed_list[index][0]:
                                
                if nordpool_list[index][2]<fixed_list[index][2]:                
                    difference=fixed_list[index][2]-nordpool_list[index][2]
                    temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,nordpool_list[index][3]]
                    saved_list.append(temp_list2)
                    
                if nordpool_list[index][2]>fixed_list[index][2]:
                    difference=nordpool_list[index][2]-fixed_list[index][2]
                    temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,fixed_list[index][3]]
                    saved_list.append(temp_list2)
                    
        return saved_list
        
    else:
        for i in consumption: # Loop makes fixed prices list with consumption
            cost=int(i[2])
            fixed_price=cost*float(fixed_cost)
            temp_list=[i[0],i[1],fixed_price,2]
            fixed_list.append(temp_list)
            
        for x in range(0,len(prices)):
            cost=float(consumption[x][2])
            nordpool_price=cost*float(prices[x][2])
            temp_list1=[prices[x][0],prices[x][1],nordpool_price,prices[x][3]]
            nordpool_list.append(temp_list1)
             
        for index in range(0,len(nordpool_list)):
            if nordpool_list[index][0] == fixed_list[index][0]:    
                if prices[index][2]==max_list[0][2]:
                    consump=get_consumption(max_list[0][0])
                    if float(consump[0][0])<float(battery_capacity) or float(consump[0][0])==float(battery_capacity):
                        difference=nordpool_list[index][2]
                        capacity=float(battery_capacity)-float(consump[0][0])
                        temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,3]
                        saved_list.append(temp_list2)
                        insert_batteryinfo(nordpool_list[index][0],nordpool_list[index][1],0,capacity,3)
                        continue
                    
                    if float(consump[0][0])>float(battery_capacity):
                        difference=fixed_list[index][2]-nordpool_list[index][2]
                        temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,nordpool_list[index][3]]
                        saved_list.append(temp_list2)
                        continue
                    
                if prices[index][2]==min_list[0][2]:
                    if float(battery[0][2])<float(battery_capacity):
                        new_cap=float(battery_chargepower)+float(battery[0][2])
                        if new_cap>40:
                            new_cap=40
                        insert_batteryinfo(nordpool_list[index][0],nordpool_list[index][1],new_cap,battery_chargepower,3) # dies 
                        
                if nordpool_list[index][2]<fixed_list[index][2]:
                    difference=fixed_list[index][2]-nordpool_list[index][2]
                    temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,nordpool_list[index][3]]
                    saved_list.append(temp_list2)
                    
                if nordpool_list[index][2]>fixed_list[index][2]:
                    difference=nordpool_list[index][2]-fixed_list[index][2]
                    temp_list2=[nordpool_list[index][0],nordpool_list[index][1],difference,fixed_list[index][3]]
                    saved_list.append(temp_list2)
                    
        return saved_list

def insert_saved_list(saved_list):
    try:
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO electricity_connection (`startime`,`endtime`,`savedEUR`,electricty_id) 
	                                            VALUES (%s, %s, %s,%s) """
        for record in saved_list:
            cursor.execute(mySql_insert_query, record)
            connection.commit()
            logger.info(" inserted successfully")    
    except mysql.connector.Error as error:
        logger.error("Failed to insert into MySQL table {}".format(error))     
    
def select_bateryinfo(id):
    try:
        sql_select_Query = "select * from battery_info where electricty_id = %s order by startime DESC limit 1;"
        cursor = connection.cursor()
        record=(3,)
        cursor.execute(sql_select_Query,record)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        logger.error("Error using select_bateryinfo", e)


