import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

env_loaded = False

def load_environment():
    global env_loaded
    if not env_loaded:
        load_dotenv()
        env_loaded = True
        print("Environment variables loaded.")

def create_db_connection():
    load_environment()  # 确保环境变量被加载

    host_name = os.getenv("DB_HOST")
    user_name = os.getenv("DB_USER")
    user_password = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")
    
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    
    return connection

load_environment()
