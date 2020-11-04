import sqlite3
from sqlite3 import Error

from datetime import datetime

DATABASE_FILE = r"Accord.db"
DATABASE_LOGS_FILE = r"Accord_logs.db"
DATABASE_MESSAGES = r"Accord_messages.db"
DATABASE_SAVED_ACCOUNTS = r"Accord_saved_accounts"

#new database with 
def initialize_database():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users
                        (email TEXT, public_key TEXT, ca_signature TEXT)    
                        """)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def check_user(email: str) -> bool:
    """ checking if email exists in the SQLite database """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        return result is not None
    except Error:
        return False

def add_user_info(email:str, public_key:str, ca_signature:str) -> bool:
    """ adding user email & password  into the SQLite database """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO users
                    (email,public_key,signature)
                    VALUES(?,?,?);
                    """
        cursor.execute(sqlite_insert_with_param, (email, public_key,ca_signature))
        conn.commit()
        #
        #for x in cursor.execute("SELECT * FROM users").fetchall():
        #    print(x,type(x))
        conn.close()
        return True
    except Error as e:
        return False

def get_user_info(email:str)->dict:
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        if check_user(email):
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            result = cursor.fetchone()
            (user,public_key,signature)= result
            return {"user": result[0], "public_key": result[1], "ca_signature": result[2]} 
        else:
            raise Exception("User not in database")

    except Exception as e:
        pass


'''
def check_password(email:str, password:str)->bool:
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        (user, correct_pass) = result
        return password == correct_pass
    except Error:
        return False
'''


'''
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
'''

'''
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
'''
'''
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
'''
'''
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
'''

if __name__ == '__main__':
    print(initialize_database())
    print(check_user("email@com.com"))
    print(add_user_info("email@com.com","KEY","SIGNATURE"))
    print(check_user("email@com.com"))
    print(get_user_info("email@com.com"))


    #print(add_user_info("at@gmail.com","StronkPass1"))
    #print(check_password("at@gmail.com","StronkPass1"))
    #print(check_password("at@gmail.com","StronkPass2"))
    #print(add_user_email("pavle.rohalj@pomona.edu"))
    #print(add_user_info("at@gmail.com","StronkPass1"))
    #print(check_email("pavle.rohalj@pomona.edu"))
    