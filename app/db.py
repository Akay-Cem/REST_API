import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE')
    )

def initialize_database():
    # Step 1: Connect without specifying the database initially
    conn = mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD')
    )
    cursor = conn.cursor()

    # Step 2: Create the database if it doesn't exist
    database_name = os.environ.get('MYSQL_DATABASE')
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    
    # Close the initial connection
    cursor.close()
    conn.close()

    # Step 3: Reconnect with the database specified
    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 4: Execute schema.sql file
    with open('app/schema.sql', 'r') as f:
        sql_commands = f.read()
    for command in sql_commands.split(';'):
        if command.strip():
            cursor.execute(command)
    
    cursor.close()
    conn.close()
