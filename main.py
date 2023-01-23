
from ast import Try
import mysql.connector
import json
import datetime
import time
import random
import logging
import logging.config
import yaml


from datetime import datetime
from configparser import ConfigParser
from mysql.connector import Error

def init_db():
	global connection
	connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)

def get_cursor():
	global connection
	try:
		connection.ping(reconnect=True, attempts=1, delay=0)
		connection.commit()
	except mysql.connector.Error as err:
		connection = init_db()
		connection.commit()
	return connection.cursor()
if __name__ == "__main__":

	# Loading logging configuration
	with open('./log_main.yaml', 'r') as stream:
		log_config = yaml.safe_load(stream)

		logging.config.dictConfig(log_config)

	# Creating logger
	logger = logging.getLogger('root')

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


