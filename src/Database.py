import sqlite3
from sqlite3 import Error
import datetime

"""
DISCLAIMER: user/email the same thing

DATABASE WITH USERNAMES:
-contains: email,public_key,ca_signature

---Functions:---
initialize_username_database()                          init database
check_user(user)  -> bool:                              checks user in the database
add_user_info(email, public_key, ca_signature) -> bool: adds user
get_user_info(email)-> dict :                           get user info
get_all_users() -> list of dict:                        gets all users

DATABASE WITH SAVED ACCOUNTS:
-contains 2 tables: (1) USERS: email, private_key, aes_iv, tag 
                    (2) CONTACTS: email, contact,contact_aes, signature , iv_aes , hmac_key ,iv_hmac ,public_key    

---Functions for table (1) USERS:---
initialize_saved_accounts_database()                     init both tables
add_user_account(email, private_key,aes_iv,tag)-> bool   add user account
get_user_accounts() -> list of dict                      get all users 
get_user_account(user) -> dict                           info of the user

---Functions for table (2) CONTACTS:---
initialize_saved_accounts_database()                                                             init both tables
add_contact_info(email,contact,contact_aes,signature,iv_aes,hmac_key,iv_hmac,public_key)->bool:  add contact info
get_user_contact_info(email)-> list of dict                                                      list of contacts

DATABASE WITH GROUPS:
-contains: groups inside the server 

---Functions:---
initialize_groups_database()                                                                    init database
add_group(group_name, participant, signature, aes_key, aes_iv, hmac_key, hmac_iv) -> bool:      adds a person is affiliated with a group individually
get_username_groups(username) -> list of dict                                                   gets all instances of the user in groups
get_group_participants(group_name) -> list of dict                                              gets all members in a group 
delete_group(group_name) -> bool                                                                deletes group_name
"""

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
                        (email TEXT, private_key TEXT,aes_iv TEXT,tag TEXT)    
                        """)
        cursor.execute("""CREATE TABLE contacts
                        (email TEXT, contact TEXT, contact_aes TEXT, signature TEXT, iv_aes TEXT, hmac_key TEXT, iv_hmac TEXT,public_key TEXT)    
                        """)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
#email, private_key, aes_iv, tag
def add_user_account(email:str, private_key:str,aes_iv:str,tag:str) -> bool:
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
                        (email,private_key,aes_iv,tag)
                        VALUES(?,?,?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (email, private_key,aes_iv,tag,))
        else:
            sqlite_insert_with_param = """
                        INSERT INTO users
                        (email,private_key,aes_iv,tag)
                        VALUES(?,?,?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (email, private_key,aes_iv,tag,))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_user_accounts() -> list:
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM users'):
            return_list.append({"user": row[0], "private_key": row[1], "aes_iv": row[2],"tag":row[3]})
        conn.close()
        return return_list
    except Exception as e:
        print(e)
        return return_list

def get_user_account(user:str) -> dict:
    return_dict = {}
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (user,))
        result  = c.fetchone()
        return_dict = {"user": result[0], "private_key": result[1], "aes_iv": result[2],"tag":result[3]}
        conn.close()
        return return_dict
    except Exception as e:
        return return_dict




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
                        (group_name TEXT, participant TEXT, signature TEXT, aes_key TEXT, aes_iv TEXT, hmac_key TEXT, hmac_iv TEXT)    
                        """)
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def add_group(group_name:str, participant:str, signature:str, aes_key:str, aes_iv:str, hmac_key:str, hmac_iv:str) -> bool:
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=? AND participant=?", (group_name,participant,))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute("DELETE FROM groups WHERE group_name = ?", (group_name,)) 
            sqlite_insert_with_param = """
                        INSERT INTO groups
                        (group_name , participant , signature, aes_key , aes_iv, hmac_key , hmac_iv)    
                        VALUES(?,?,?,?,?,?,?);
                        """
            cursor.execute(sqlite_insert_with_param, (group_name , participant , signature, aes_key , aes_iv, hmac_key , hmac_iv,))
            conn.commit()
        else:
            sqlite_insert_with_param = """
                        INSERT INTO groups
                        (group_name , participant , signature, aes_key , aes_iv, hmac_key , hmac_iv)        
                        VALUES(?,?,?,?,?,?,?);
                        """

            cursor.execute(sqlite_insert_with_param, (group_name , participant , signature, aes_key , aes_iv, hmac_key , hmac_iv,))
            conn.commit()
            
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False    

def delete_group(group_name:str):
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=?", (group_name,))
        return True 
    except Exception as e:
        return False

def get_group_participants(group_name:str)->list:
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=?", (group_name,))
        results = cursor.fetchall()
        if results is None:
            return return_list
        for r in results:
            return_list.append({"group_name": r[0] , "participant": r[1] ,"signature": r[2], "aes_key": r[3] , "aes_iv": r[4], "hmac_key": r[5] , "hmac_iv": r[6]})

        return return_list       
    except Exception as e:
        return [] 

def get_username_groups(username:str):
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE participant=?", (username,))
        results = cursor.fetchall()
        if results is None:
            return return_list
        ls_groups = []
        for r in results:
            ls_groups.append(r[0])

        for group in ls_groups:
            return_list.append(get_group_participants(group))

        return return_list  
    except Exception as e:
        print(e)
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

    #import pprint 
    #initialize_groups_database()
    #pprint.pprint(add_group("group1","a","SIGNATURE","AES_KEY","AES_IV","HMAC","HMAC_IV"))
    #pprint.pprint(add_group("group1","xd","SIGNATURE","AES_KEY","AES_IV","HMAC","HMAC_IV"))
    #pprint.pprint(add_group("group2","b","SIGNATURE2","AES_KEY2","AES_IV2","HMAC2","HMAC_IV2"))
    #pprint.pprint(add_group("group3","c","SIGNATURE3","AES_KEY3","AES_IV3","HMAC3","HMAC_IV3"))
    #pprint.pprint(add_group("group3","d","SIGNATURE3","AES_KEY3","AES_IV3","HMAC3","HMAC_IV3"))
    #pprint.pprint(add_group("group3","f","SIGNATURE3","AES_KEY3","AES_IV3","HMAC3","HMAC_IV3"))
    #pprint.pprint(get_group_participants("group3"))
    #pprint.pprint(get_username_groups("a"))
    #pprint.pprint(get_username_groups("c"))
    #pprint.pprint(add_group("group1","a","NEWSIGNATURE","NEWAES_KEY","NEWAES_IV","NEWHMAC","NEWHMAC_IV"))
    #pprint.pprint(get_group_participants("group1"))
    '''
    initialize_saved_accounts_database()
    print(add_user_account("a","AKEY","AESIV","ATAG"))
    print(add_user_account("B","BKEY","BESIV","BTAG"))
    print(add_user_account("C","CKEY","CESIV","CTAG"))
    print(get_user_accounts())
    print(get_user_account("a"))
    print(get_user_account("gaa"))
    print(add_user_account("a","new","newIV","newTAG"))
    print(get_user_account("a"))
    
    
    
    import os
    os.remove("Accord_saved_accounts.db")
    '''


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
   # import pprint 
    #print()
    #initialize_groups_database()
    #pprint.pprint(add_group("group1","a","SIGNATURE","AES_KEY","AES_IV","HMAC","HMAC_IV"))
    #pprint.pprint(add_group("group1","xd","SIGNATURE","AES_KEY","AES_IV","HMAC","HMAC_IV"))
    #pprint.pprint(add_group("group2","b","SIGNATURE2","AES_KEY2","AES_IV2","HMAC2","HMAC_IV2"))
    #pprint.pprint(add_group("group3","c","SIGNATURE3","AES_KEY3","AES_IV3","HMAC3","HMAC_IV3"))
    #pprint.pprint(add_group("group3","d","SIGNATURE3","AES_KEY3","AES_IV3","HMAC3","HMAC_IV3"))
    #pprint.pprint(add_group("group3","f","SIGNATURE3","AES_KEY3","AES_IV3","HMAC3","HMAC_IV3"))
    #pprint.pprint(get_group_participants("group3"))
    #pprint.pprint(get_username_groups("a"))
    #pprint.pprint(get_username_groups("c"))
    #pprint.pprint(add_group("group1","a","NEWSIGNATURE","NEWAES_KEY","NEWAES_IV","NEWHMAC","NEWHMAC_IV"))
    #pprint.pprint(get_group_participants("group1"))
    '''
    initialize_saved_accounts_database()
    print(add_user_account("a","AKEY","AESIV","ATAG"))
    print(add_user_account("B","BKEY","BESIV","BTAG"))
    print(add_user_account("C","CKEY","CESIV","CTAG"))
    print(get_user_accounts())
    print(get_user_account("a"))
    print(get_user_account("gaa"))
    print(add_user_account("a","new","newIV","newTAG"))
    print(get_user_account("a"))
    
    
    
    import os
    os.remove("Accord_saved_accounts.db")
    '''