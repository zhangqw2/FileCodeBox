'''
author: zhangquanwei
Date: 2025-03-08 22:33:54
'''
import psycopg2

def fetch_test_table_data():
    try:
        # 连接到Docker容器中的PostgreSQL数据库
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        
        # 执行查询语句
        cursor.execute("SELECT * FROM test")
        rows = cursor.fetchall()
        
        # 打印查询结果
        for row in rows:
            print(row)
        
    except Exception as error:
        print(f"Error fetching data: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# 调用函数以测试连接和数据读取
fetch_test_table_data()
