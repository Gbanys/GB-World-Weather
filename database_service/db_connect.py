import pymysql
import os

def connect_to_amazon_rds():

    connection = pymysql.connect(
        host=os.environ['DATABASE_INSTANCE_ENDPOINT'], 
        user=os.environ['RDS_USER'], 
        port = 3306, 
        passwd = os.environ['RDS_PASSWORD'], 
        database=os.environ['DATABASE_NAME']
    )

    return connection