import logging
import logging.config
import mysql.connector
import os
import time
from datetime import datetime
import yaml


from configparser import ConfigParser
from mysql.connector import Error

# Loading logging configuration
with open('./log_migrate_db.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

logging.config.dictConfig(config)

# Creating logger
logger = logging.getLogger('root')

logger.info('DB migration service')

# Initiating and reading config values
logger.info('Loading configuration from file')

try:
	config = ConfigParser()
	config.read('config.ini')

	mysql_config_mysql_host = config.get('mysql_config', 'mysql_host')
	mysql_config_mysql_db = config.get('mysql_config', 'mysql_db')
	mysql_config_mysql_user = config.get('mysql_config', 'mysql_user')
	mysql_config_mysql_pass = config.get('mysql_config', 'mysql_pass')

except:
	logger.exception('')
logger.info('DONE')

connection = None
connected = False

def init_db():
	global connection
	connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)

init_db()

def get_cursor():
	global connection
	try:
		connection.ping(reconnect=True, attempts=1, delay=0)
		connection.commit()
	except mysql.connector.Error as err:
		logger.error("No connection to db " + str(err))
		connection = init_db()
		connection.commit()
	return connection.cursor()

# Opening connection to mysql DB
logger.info('Connecting to MySQL DB')
try:
	# connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)
	cursor = get_cursor()
	if connection.is_connected():
		db_Info = connection.get_server_info()
		logger.info('Connected to MySQL database. MySQL Server version on ' + str(db_Info))
		cursor = connection.cursor()
		cursor.execute("select database();")
		record = cursor.fetchone()
		logger.debug('Your connected to - ' + str(record))
		connection.commit()
except Error as e :
	logger.error('Error while connecting to MySQL' + str(e))


# Check if table exists
def mysql_check_if_table_exists(table_name):
	records = []
	cursor = get_cursor()
	try:
		cursor = connection.cursor()
		result  = cursor.execute("SHOW TABLES LIKE '" + str(table_name) + "'")
		records = cursor.fetchall()
		connection.commit()
	except Error as e :
		logger.error("query: " + "SHOW TABLES LIKE '" + str(table_name) + "'")
		logger.error('Problem checking if table exists: ' + str(e))
		pass
	return records

# Create migrations table
def mysql_create_migrations_table():
	cursor = get_cursor()
	result = []
	try:
		cursor = connection.cursor()
		result  = cursor.execute( "CREATE TABLE `migration` ( `id` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(255), `exec_ts` INT(10), `exec_dt` varchar(20), PRIMARY KEY (`id`))" )
		connection.commit()
	except Error as e :
		logger.error( "CREATE TABLE `migration` ( `id` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(255), `exec_ts` INT(10), `exec_dt` varchar(20), PRIMARY KEY (`id`))" )
		logger.error('Problem creating migration table in DB: ' + str(e))
		pass
	return result

# Check if table exists
def mysql_check_if_migration_exists(migration_f_name):
	records = []
	cursor = get_cursor()
	try:
		cursor = connection.cursor()
		result  = cursor.execute("SELECT count(*) FROM migration WHERE `name` ='" + str(migration_f_name) + "'")
		records = cursor.fetchall()
		connection.commit()
	except Error as e :
		logger.error("SELECT count(*) FROM migration WHERE `name` ='" + str(migration_f_name) + "'")
		logger.error('Problem checking if migration exists: ' + str(e))
		pass
	return records[0][0]

# Exec any sql on DB
def mysql_exec_any_sql(sql_query):
	cursor = get_cursor()
	status = 0
	try:
		cursor = connection.cursor()
		result  = cursor.execute( sql_query )
		logger.info(result)
		connection.commit()
	except Error as e :
		logger.error( sql_query )
		logger.error('Problem executing sql query on DB: ' + str(e))
		status = 1
		pass
	return status

# Migration value insert
def mysql_migration_value_insert(name, exec_ts, exec_dt):
	cursor = get_cursor()
	try:
		cursor = connection.cursor()
		result  = cursor.execute( "INSERT INTO `migration` (`name`, `exec_ts`, `exec_dt`) VALUES ('" + str(name) + "', '" + str(exec_ts) + "', '" + str(exec_dt) + "')")
		connection.commit()
	except Error as e :
		logger.error( "INSERT INTO `migration` (`name`, `exec_ts`, `exec_dt`) VALUES ('" + str(name) + "', '" + str(exec_ts) + "', '" + str(exec_dt) + "')")
		logger.error('Problem inserting migration values into DB: ' + str(e))
		pass

if mysql_check_if_table_exists("migrations") == []:
	mysql_create_migrations_table()
else:
	logger.info("Migrations table exists")

migrations_list = []
# Reading all migration file names into an array
cur_dir = os. getcwd()
migrations_files_list = os.listdir(cur_dir + "/migrations/")
for f_name in migrations_files_list:
	if f_name.endswith('.sql'):
		migrations_list.append(f_name)

# Sorting list to be processed in the correct order
migrations_list.sort(reverse=False)

counter = 0
for migration in migrations_list:
	if mysql_check_if_migration_exists(migration) == 0:
		with open(cur_dir + "/migrations/" + migration,'r') as file:
			migration_sql = file.read()
			logger.debug(migration_sql)
			logger.info("Executing: " + str(migration))
			if mysql_exec_any_sql(migration_sql) == 0:
				mig_exec_ts = int(time.time()) 
				mig_exec_dt = datetime.utcfromtimestamp(mig_exec_ts).strftime('%Y-%m-%d %H:%M:%S')
				mysql_migration_value_insert(migration, mig_exec_ts, mig_exec_dt)
				logger.info("OK")
				counter += 1
			else:
				logger.error("Problem applying migration. Aborting")
				break 
if counter == 0:
	logger.info("No migrations to execute")	

def trigger():
	try: 
		cursor.execute("drop trigger if exists `trigger`")
		trigger = """
		create trigger `trigger` after insert
        on total_consumption for each row
        begin
            set @startime=(select startime from total_consumption order by startime desc limit 1);
            set @endtime=(select endtime from total_consumption order by startime desc limit 1);
            set @cons=(select consumption from total_consumption order by startime desc limit 1);
            set @price=(select best_price from connection where left(startime,13)=left(@startime,13) limit 1);
            set @expenses=(select @price*@cons);
            INSERT INTO electricityprice.total_cost
                (startime,endtime,price,consumption,expenses) VALUES
                (@startime,@endtime,@price,@cons,@expenses);
        end"""
		cursor.execute(trigger)
		connection.commit()
		logger.info("trigger made")
	except mysql.connector.Error as err:
		logger.error("No connection to db " + str(err))

def establish_conn():
	try:
		cursor.execute("drop trigger if exists `establish_connection`")
		trigger="""
		create trigger `establish_connection` after insert
		on prices for each row
		begin
			set @startime=(select startime from prices order by startime desc limit 1);
			set @endtime=(select endtime from prices order by startime desc limit 1);
			set @nord_price=(select nord_price from prices where @startime=startime order by startime desc limit 1);
			set @static_price=(select static_price from prices where @startime=startime order by startime desc limit 1);
			if @static_price > @nord_price then
				INSERT INTO `electricityprice`.`connection`
				(`startime`,`endtime`,`best_price`,`connection`)
				VALUES(@startime,@endtime,@nord_price,2);
			end if;
			if @nord_price > @static_price then
				INSERT INTO `electricityprice`.`connection`
				(`startime`,`endtime`,`best_price`,`connection`)
				VALUES(@startime,@endtime,@static_price,1);
			end if;
		end"""
		cursor.execute(trigger)
		connection.commit()
		logger.info("trigger made")


	except mysql.connector.Error as err:
		logger.error("No connection to db " + str(err))

def trigger22():
	try:
		cursor.execute("drop trigger if exists `trigger22`")
		trigger="""
		create trigger `trigger22` after insert
        on battery_info for each row
        begin
            set @startime=(select startime from total_consumption order by startime desc limit 1);
            set @endtime=(select endtime from total_consumption order by startime desc limit 1);
            set @cons=(select consumption from total_consumption order by startime desc limit 1);
            set @price=(select best_price from connection where endtime=@endtime limit 1);
            set @statuss=(select `status` from battery_info where @endtime=endtime order by startime desc limit 1);
            set @battery_consump=(select kw from battery_info where @endtime=endtime and @statuss=status);
            if @statuss = 1 then
                set @expenses=(select 0*@cons);
                UPDATE `electricityprice`.`total_cost` SET
                price=@price,
                consumption=@cons,
                expenses=@expenses
                WHERE @endtime=endtime;
            end if;
            if @statuss =0 then
                set @expenses=(select (@cons+@battery_consump)*@price);
             UPDATE `electricityprice`.`total_cost` SET
                price=@price,
                consumption=@cons,
                expenses=@expenses
                WHERE @endtime=endtime;
            end if; 
        end """
		cursor.execute(trigger)
		connection.commit()
		logger.info("trigger made")   


	except mysql.connector.Error as err:
		logger.error("No connection to db " + str(err))
establish_conn()
trigger()
trigger22()
