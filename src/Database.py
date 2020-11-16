import sqlite3
from sqlite3 import Error
import datetime

DATABASE_USERNAMES = r"Accord.db"
'''Username Database'''
def initialize_username_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users
                        (email TEXT, public_key TEXT, ca_signature TEXT)    
                        """)
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()

def check_user(email: str) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        return False

def add_user_info(email:str, public_key:str, ca_signature:str) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        sqlite_insert_with_param = """
                    INSERT INTO users
                    (email,public_key,ca_signature)
                    VALUES(?,?,?);
                    """
        if check_user(email):
            cursor.execute("DELETE FROM users WHERE email = ?", (email,))
            cursor.execute(sqlite_insert_with_param, (email, public_key,ca_signature,))
            conn.commit()
        else:
            cursor.execute(sqlite_insert_with_param, (email, public_key,ca_signature,))
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
            return {}
    except Exception as e:
        return {}

def get_all_users()->list:
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        c = conn.cursor()
        return_list = []
        for row in c.execute('SELECT * FROM users'):
            return_list.append({"user": row[0], "public_key": row[1], "ca_signature": row[2]})
        conn.close()
        if row is None:
            return []
        else:
            return return_list
    except Exception as e:
        return []




DATABASE_SAVED_ACCOUNTS = r"Accord_saved_accounts.db"
'''Database users & contacts'''
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
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
        print(e)
        return return_list

def add_contact_info(email:str,contact:str,contact_aes:str,signature:str,iv_aes:str,hmac_key:str,iv_hmac:str,public_key="")->bool:
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
    except Exception as e:
        return False

def get_user_contact_info(email:str)->list:
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        c.execute("SELECT * FROM contacts WHERE email=?", (email,))
        for row in c.fetchall():
            return_list.append({"contact":row[1],"contact_aes": row[2] ,"signature": row[3],"iv_aes": row[4] ,"hmac_key":row[5],"iv_hmac": row[6],"public_key":row[7]})
    
        return return_list 
    except Exception:
        return return_list
    

DATABASE_GROUPS = r"Accord_groups.db"
def initialize_groups_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE groups
                        (group_name TEXT, username TEXT, aes_key TEXT)    
                        """)
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()

def add_group(group_name:str,participants:list,aes_key:str) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=?", (group_name,))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute("DELETE FROM groups WHERE group_name = ?", (group_name,)) 
            sqlite_insert_with_param = """
                        INSERT INTO groups
                        (group_name, username , aes_key)    
                        VALUES(?,?,?);
                        """
            for participant in participants:            
                cursor.execute(sqlite_insert_with_param, (group_name, participant , aes_key,))
                conn.commit()
        else:
            sqlite_insert_with_param = """
                        INSERT INTO groups
                        (group_name, username , aes_key)    
                        VALUES(?,?,?);
                        """
            for participant in participants:            
                cursor.execute(sqlite_insert_with_param, (group_name, participant , aes_key,))
                conn.commit()
            
        conn.close()
        return True
    except Exception as e:
        return False    


def get_group_participants(group_name:str)->list:
    try:
        return_list = []
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=?", (group_name,))
        results = cursor.fetchall()
        if results is None:
            return return_list
        for r in results:
            return_list.append({"group_name":group_name,"username":r[1],"aes_key":r[2]})

        return return_list       
    except Exception as e:
        return [] 

def get_username_groups(username:str):
    try:
        return_list = []
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE username=?", (username,))
        results = cursor.fetchall()
        if results is None:
            return return_list
        for r in results:
            return_list.append({"group_name":r[0],"username":username,"aes_key":r[2]})

        return return_list  
    except Exception as e:
        return []

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
        return True
    except Exception as e:
        print(e)
        return False
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
    except Exception as e:
        print(e)
        pass


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
    except Exception as e:
        print(e)
        return False

#if __name__ == '__main__':

