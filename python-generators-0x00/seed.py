import mysql.connector
import csv


def connect_db():
    """connect to mysql server only"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        return conn
    except Exception as e:
        print("Error connecting:", e)
        return None


def create_database(connection):
    """create ALX_prodev db if it does not exist"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()


def connect_to_prodev():
    """connect directly to ALX_prodev"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return conn
    except Exception as e:
        print("Error connecting to ALX_prodev:", e)
        return None


def create_table(connection):
    """create user_data table"""
    cursor = connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS user_data(
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


def insert_data(connection, csv_file):
    """insert into user_data from csv only if row does not exist"""
    cursor = connection.cursor()

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("SELECT user_id FROM user_data WHERE user_id=%s;", (row['user_id'],))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(
                    "INSERT INTO user_data(user_id, name, email, age) VALUES(%s, %s, %s, %s);",
                    (row['user_id'], row['name'], row['email'], row['age'])
                )
                connection.commit()

    cursor.close()
