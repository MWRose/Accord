import sqlite3
from sqlite3 import Error
import datetime


DATABASE_USERNAMES = r"Accord.db"
'''Username Database'''
def initialize_username_database():
    """ """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
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
    """  """
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        return result is not None
    except Error:
        return False

def add_user_info(email:str, public_key:str, ca_signature:str) -> bool:
    """ """
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO users
                    (email,public_key,ca_signature)
                    VALUES(?,?,?);
                    """
        cursor.execute(sqlite_insert_with_param, (email, public_key,ca_signature))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_user_info(email:str)->dict:
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        
        if check_user(email):
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            result = cursor.fetchone()
            return {"user": result[0], "public_key": result[1], "ca_signature": result[2]} 
        else:
            raise Exception("User not in database")
    except Exception as e:
        pass

def get_all_users()->list:
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        c = conn.cursor()
        return_list = []
        for row in c.execute('SELECT * FROM users'):
            return_list.append({"user": row[0], "public_key": row[1], "ca_signature": row[2]})
        conn.close()
        return return_list
    except Error as e:
        print(e)
'''Username Database'''



DATABASE_SAVED_ACCOUNTS = r"Accord_saved_accounts"
'''Database saved accounts'''
# USERNAME, ENCRYPTED(private key, contacts, groups)
def initialize_saved_accounts_database():
    """ """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE saved_accounts
                        (email TEXT, encrypted_data TEXT)    
                        """)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def check_user_saved_accounts(email: str) -> bool:
    """ """
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_accounts WHERE email=?", (email,))
        result = cursor.fetchone()
        return result is not None
    except Error:
        return False

def add_saved_account(email:str, data:str) -> bool:
    """ """
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO saved_accounts
                    (email,encrypted_data)
                    VALUES(?,?);
                    """
        cursor.execute(sqlite_insert_with_param, (email, data))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        return False

def get_saved_account_info(email:str)->dict:
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()
        
        if check_user(email):
            cursor.execute("SELECT * FROM saved_accounts WHERE email=?", (email,))
            result = cursor.fetchone()
            return {"user": result[0], "encrypted_data": result[1]} 
        else:
            raise Exception("User not in database")
    except Exception as e:
        pass

def get_all_saved_accounts()->list:
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        return_list = []
        for row in c.execute('SELECT * FROM saved_accounts'):
            return_list.append({"user": row[0], "encrypted_data": row[1]})
        conn.close()
        return return_list
    except Error as e:
        print(e)

'''Database saved accounts'''

DATABASE_MESSAGES = r"Accord_messages.db"
'''Database messages'''
def initialize_messages_database():
    """ initialize message database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_MESSAGES)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE messages
                        (sender TEXT, recipient TEXT, message TEXT,timestamp DATETIME)    
                        """)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def add_message(sender:str, recipient:str, message:str) -> bool:
    """ adding message to database"""
    try:
        #timestamp created here 
        timestamp = datetime.datetime.now()
        print(timestamp)
        conn = sqlite3.connect(DATABASE_MESSAGES)
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO messages
                    (sender,recipient,message,timestamp)
                    VALUES(?,?,?,?);
                    """
        cursor.execute(sqlite_insert_with_param, (sender, recipient,message,timestamp))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_all_messages()->list:
    try:
        conn = sqlite3.connect(DATABASE_MESSAGES)
        c = conn.cursor()
        return_list = []
        for row in c.execute('SELECT * FROM messages'):
            return_list.append({"sender": row[0], "recipient": row[1],"message": row[2],"timestamp": row[3]})
        conn.close()
        return return_list
    except Error as e:
        print(e)


def erase_msg_timestamp(timestamp:str):
    """erasing message with timestamp less than"""
    try:
        conn = sqlite3.connect(DATABASE_MESSAGES)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM messages'):
            date_time_obj = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f')
            duration = datetime.datetime.now() - date_time_obj                      
            duration_in_s = duration.total_seconds()
            print(duration_in_s)
            if duration_in_s > 20:
                c.execute("DELETE FROM messages WHERE timestamp = ?", (row[3],))
        
        conn.close()
        return
    except Error as e:
        print(e)

'''Database messages'''





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
    '''
    initialize_username_database()
    print(check_user("email@com.com"))
    print(add_user_info("email@com.com","KEY","SIGNATURE"))
    print(add_user_info("YAHOO@com.com","KEY2","SGINATURE2"))
    print(check_user("YAHOO@com.com"))
    print(get_user_info("email@com.com"))
    print(get_all_users())
    '''
    '''
    initialize_saved_accounts_database()
    print(check_user_saved_accounts("email@com.com"))
    print(add_saved_account("email@com.com","2U9H3917H291H2DBDHADA"))
    print(add_saved_account("YAHOO@com.com","N19E7H217191D12D12"))
    print(check_user_saved_accounts("YAHOO@com.com"))
    print(get_saved_account_info("email@com.com"))
    print(get_all_saved_accounts())
    '''

    
    initialize_messages_database()
    #print(add_message("bob","alice","hello hows life"))
    #print(add_message("alice","bob","its good i think"))
    #print(add_message("bob","alice","ok epic"))
    #print(get_all_messages())
    #mport time
    #import datetime
    #time.sleep(2)
    timestamp = datetime.datetime.now()
    erase_msg_timestamp(timestamp)
    print(len(get_all_messages()))

    