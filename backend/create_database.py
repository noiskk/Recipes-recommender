import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
import os
load_dotenv()

def create_database():
    try:
        # MySQL 서버에 연결
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 데이터베이스 생성
            cursor.execute("CREATE DATABASE IF NOT EXISTS recipe_db")
            print("데이터베이스가 성공적으로 생성되었습니다.")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL 연결이 종료되었습니다.")

if __name__ == "__main__":
    create_database() 