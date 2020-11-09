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


#get_contacts(USERNAME)
#get_groups(USERNAME)
DATABASE_SAVED_ACCOUNTS = r"Accord_saved_accounts.db"
'''Database users & contacts'''
# USERNAME, ENCRYPTED(private key, contacts, groups)
def initialize_saved_accounts_database():
    """ """
    conn = None
    try:
  
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users
                        (email TEXT, private_key TEXT)    
                        """)
        cursor.execute("""CREATE TABLE contacts
                        (email TEXT, contact TEXT, contact_aes TEXT, signature TEXT, iv_aes TEXT, hmac_key TEXT, iv_hmac TEXT,public_key TEXT)    
                        """)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def add_user_account(email:str, private_key:str) -> bool:
    """ """
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        if result is not None:
            cursor.execute("DELETE FROM users WHERE email = ?", (email,)) 
            sqlite_insert_with_param = """
                        INSERT INTO users
                        (email,private_key)
                        VALUES(?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (email, private_key,))
        else:
            sqlite_insert_with_param = """
                        INSERT INTO users
                        (email,private_key)
                        VALUES(?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (email, private_key,))

        conn.commit()
        conn.close()
        return True
    except Error as e:
        return False

def get_user_accounts() -> list:
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        return_list = []
        for row in c.execute('SELECT * FROM users'):
            return_list.append({"user": row[0], "private_key": row[1]})
        conn.close()
        return return_list
    except Error as e:
        print(e)
        return return_list

def add_contact_info(email:str,contact:str,contact_aes:str,signature:str,iv_aes:str,hmac_key:str,iv_hmac:str,public_key="")->True:
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE email=? AND contact= ?", (email,contact,))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute("DELETE FROM contacts WHERE email = ? AND contact = ?", (email,contact,)) 
            sqlite_insert_with_param = """
                        INSERT INTO contacts
                        (email, contact , contact_aes , signature , iv_aes ,hmac_key, iv_hmac ,public_key )    
                        VALUES(?,?,?,?,?,?,?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (email,contact,contact_aes,signature,iv_aes,hmac_key,iv_hmac,public_key,))
            conn.commit()
        else:
            sqlite_insert_with_param = """
                        INSERT INTO contacts
                        (email, contact , contact_aes , signature , iv_aes ,hmac_key, iv_hmac ,public_key )    
                        VALUES(?,?,?,?,?,?,?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (email,contact,contact_aes,signature,iv_aes,hmac_key,iv_hmac,public_key,))
            conn.commit()
            
        conn.close()
        return True
    except Error as e:
        return False

def get_user_contact_info(email:str)->list:
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        return_list = []
        c.execute("SELECT * FROM contacts WHERE email=?", (email,))
        for row in c.fetchall():
            return_list.append({"contact":row[1],"contact_aes": row[2] ,"signature": row[3],"iv_aes": row[4] ,"hmac_key":row[5],"iv_hmac": row[6],"public_key":row[7]})
    
        return return_list 
    except Error:
        return return_list
    

'''
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
            # Contact
            # "pavle@pomona.edu", "max@pomona.edu", "max_aes", "signed under user password"
            # "pavle@pomona.edu", "stefanos@pomona.edu", "max_aes"
            

            # [{"recipient", "enc_aes", "signed"}, {}]
            # Users
            # "pavle@pomona.edu", "private_key", ""
            
            # Groups
            # user0, group_name, user0, aes_key, signature
            # user0, group_name, user1, "                "
            # user0, group_name, user2, "                "
            # user0, group_name, hacker,"                "
            # user1, group_name, user0, aes_key, signature
            # user2, group_name, user0
            # user2, group_name, user1

            # GROUPS
            # accord, username, aes_key, signature
            # accord, username1, aes_key, signature
            

            
             
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
'''
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


def erase_msg_timestamp(timestamp:str)->bool:
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
                c.execute("DELETE FROM messages WHERE timestamp = ?", (row[3],)) #row[3] is the timestamp

        conn.close()
        return True
    except Error as e:
        print(e)
        return False

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

    #print("b")
    #print(get_user_contact_info("b"))
    
    #initialize_messages_database()
    #print(add_message("bob","alice","hello hows life"))
    #print(add_message("alice","bob","its good i think"))
    #print(add_message("bob","alice","ok epic"))
    #print(len(get_all_messages()))
    #import time
    #import datetime
    #time.sleep(2)
    #timestamp = datetime.datetime.now()
    #erase_msg_timestamp(timestamp)
    #print(len(get_all_messages()))

    