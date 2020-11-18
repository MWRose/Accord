import sqlite3
from sqlite3 import Error
import datetime

DATABASE_FILE = r"CA.db"

def initialize_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users
                        (username TEXT, public_key TEXT, ca_signature TEXT)    
                        """)
    except Exception as e:
        print("Could not initalize CA database.")
    finally:
        if conn:
            conn.close()

def username_exists(username: str) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        return result is not None
    except Exception as _:
        return False

def add_user(username:str, public_key:str, ca_signature:str) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO users
                    (username,public_key,ca_signature)
                    VALUES(?,?,?);
                    """
        cursor.execute(sqlite_insert_with_param, (username, public_key,ca_signature,))
        conn.commit()
        conn.close()
    except Exception as _:
        print("An exception was raised while adding a username to the database: " + username)