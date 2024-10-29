import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='hdb281',
        database='reserva_app'
    )
    return conn