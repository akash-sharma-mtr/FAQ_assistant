import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def fetch_knowledge_base():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM knowledge_base")
    rows = cursor.fetchall()
    connection.close()
    return rows

def log_interaction(query, response):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO logs (query, response) VALUES (%s, %s)", (query, response))
    connection.commit()
    connection.close()
