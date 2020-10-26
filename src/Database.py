import sqlite3
from sqlite3 import Error

from datetime import datetime

DATABASE_FILE = r"Accord.db"
DATABASE_LOGS_FILE = r"Accord_logs.db"

def initialize_database():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users
                        (email text)    
                        """)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def check_email(email: str) -> bool:
    """ checking if email exists in the SQLite database """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        return result is not None
    except Error:
        return False


def add_user_email(email:str) -> bool:
    """ adding user email into the SQLite database """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO users
                    (email)
                    VALUES(?);
                    """
        cursor.execute(sqlite_insert_with_param, (email,))
        conn.commit()
        return True
    except Error:
        return False

def initialize_log_database():
    """ create a database connection to a log SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_LOGS_FILE)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS chat_logs
                        (log text)
                        """)
        print("Successful log initialization")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def add_log(sender:str, recipient:str)->bool:  
    """ add a log about who send and received a message; using a timestamp from the server side"""     
    try:
        conn = sqlite3.connect(DATABASE_LOGS_FILE)
        cursor = conn.cursor()
        sqlite_insert_with_param = """INSERT INTO chat_log 
                        (log text)
                        VALUES(?);
                        """
        server_time_stamp = str(datetime.now())
        new_log =  sender +  " to "  + recipient + " @ " +server_time_stamp
        print(new_log)
        cursor.execute(sqlite_insert_with_param,(new_log,))
        conn.commit()
        return True
    except Error as e:
        return False

def print_logs():
    try:
        conn = sqlite3.connect(DATABASE_LOGS_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_logs")
        print("-----Printing Logs------")
        for row in c.execute('SELECT * FROM chat_logs'):
            print(row)
        conn.close()
    except Error as e:
        print(e)
    

if __name__ == '__main__':
    #initalize_database()
    #print(check_email("pavle.rohalj@pomona.edu"))
    #print(add_user_email("pavle.rohalj@pomona.edu"))
    #print(check_email("pavle.rohalj@pomona.edu"))
    #initialize_log_database()
    add_log("BOB","ALICE")
    add_log("ALICE","BOB")
    print_logs()