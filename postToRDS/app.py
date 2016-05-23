import sys
import logging
import rds_config
import pymysql
#rds settings
rds_host  = "billsdata.cducco4lxmzs.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

server_address = (rds_host, port)
try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
def handler(event, context):
	item_count = 0
	cur = conn.cursor()
	for value in event.keys():
		cur.execute('insert into Employee3 (EmpID, Name) values('+value+', "'+event[value]+'")')
		
	conn.commit()
	return "Added %d items from RDS MySQL table" %(item_count)