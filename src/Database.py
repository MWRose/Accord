import sqlite3
from sqlite3 import Error
import datetime


DATABASE_USERNAMES = r"Accord.db"
'''DATABASE WITH USERNAMES'''
def initialize_username_database():
    '''initialize the username database'''
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users
                        (email TEXT, public_key TEXT, ca_signature TEXT)    
                        """)
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()

def check_user(email: str) -> bool:
    '''check if user is in the username database'''
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        return result is not None
    except Exception:
        return False

def add_user_info(email:str, public_key:str, ca_signature:str) -> bool:
    '''add user to the username database'''
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
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
    except Exception:
        return False

def get_user_info(email:str)->dict:
    '''get user info from username database'''
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        cursor = conn.cursor()
        
        if check_user(email):
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            result = cursor.fetchone()
            return {"user": result[0], "public_key": result[1], "ca_signature": result[2]} 
        else:
            return {}
    except Exception:
        return {}

def get_all_users()->list:
    '''get all users from the username database'''
    try:
        conn = sqlite3.connect(DATABASE_USERNAMES)
        c = conn.cursor()
        return_list = []
        for row in c.execute('SELECT * FROM users'):
            return_list.append({"user": row[0], "public_key": row[1], "ca_signature": row[2]})
        conn.close()
        return return_list
    except Exception:
        return []


DATABASE_SAVED_ACCOUNTS = r"Accord_saved_accounts.db"
def initialize_saved_accounts_database():
    '''initialize Users and Contacts database'''
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
    except Exception:
        if conn:
            conn.close()
    finally:
        if conn:
            conn.close()

def add_user_account(email:str, private_key:str,aes_iv:str,tag:str) -> bool:
    '''add user account to the Users data'''
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
    except Exception:
        return False

def get_user_accounts() -> list:
    '''get all users from the Users database'''
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM users'):
            return_list.append({"user": row[0], "private_key": row[1], "aes_iv": row[2],"tag":row[3]})
        conn.close()
        return return_list
    except Exception:
        return return_list

def get_user_account(user:str) -> dict:
    '''get the user info from the Users database'''
    return_dict = {}
    try:
        conn = sqlite3.connect(DATABASE_SAVED_ACCOUNTS)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (user,))
        result  = c.fetchone()
        return_dict = {"user": result[0], "private_key": result[1], "aes_iv": result[2],"tag":result[3]}
        conn.close()
        return return_dict
    except Exception:
        return return_dict


def add_contact_info(email:str,contact:str,contact_aes:str,signature:str,iv_aes:str,hmac_key:str,iv_hmac:str,public_key="")->bool:
    '''add contact info into Contacts database'''
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
    except Exception:
        return False

def get_user_contact_info(email:str)->list:
    '''get all user's contacts from the database'''
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
    '''inittialize group database'''
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE groups
                        (email TEXT, group_name TEXT, participant TEXT, signature TEXT, aes_key TEXT, aes_iv TEXT, hmac_key TEXT, hmac_iv TEXT)    
                        """)
        return True
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def check_group(group_name:str):
    '''check if group exists in the database'''
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=?", (group_name,))
        result = cursor.fetchone()
        return True if result else False
    except Exception:
        return False
    finally:
        if conn:
            conn.close()

def add_group(email:str, group_name:str, participant:str, signature:str, aes_key:str, aes_iv:str, hmac_key:str, hmac_iv:str) -> bool:
    '''add a group to the group database'''
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()

        sqlite_insert_with_param = """
                    INSERT INTO groups
                    (email, group_name , participant , signature, aes_key , aes_iv, hmac_key , hmac_iv)        
                    VALUES(?,?,?,?,?,?,?,?);
                    """

        cursor.execute(sqlite_insert_with_param, (email, group_name , participant , signature, aes_key , aes_iv, hmac_key , hmac_iv,))
        conn.commit()
        
        conn.close()
        return True
    except Exception:
        return False    

def delete_group(group_name:str):
    '''delete group from database'''
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=?", (group_name,))
        return True 
    except Exception:
        return False

def get_group_participants(user:str, group_name:str)->list:
    '''get all members in a group'''
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE group_name=? and email=?", (group_name,user,))
        results = cursor.fetchall()
        if results is None:
            return return_list
        for r in results:
            return_list.append({"group_name": r[1] , "participant": r[2] ,"signature": r[3], "aes_key": r[4] , "aes_iv": r[5], "hmac_key": r[6] , "hmac_iv": r[7]})

        return return_list       
    except Exception:
        return [] 

def get_username_groups(username:str):
    '''get all instances of the user in groups database'''
    return_list = []
    try:
        conn = sqlite3.connect(DATABASE_GROUPS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM groups WHERE email=?", (username,))
        results = cursor.fetchall()
        if results is None:
            return return_list
        ls_groups = []
       
        for r in results:
            if r[1] in ls_groups:
                continue
            else:
                ls_groups.append(r[1])
        
        counter = len(ls_groups)
        while counter != 0:
            #test if the same
            res = get_group_participants(username, r[1])
            for line in res:
                return_list.append(line)
            counter -= 1

        return return_list  
    except Exception:
        return []
