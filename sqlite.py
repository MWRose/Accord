import sqlite3
from sqlite3 import Error


def initalize_database(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users
                        (email text)    
                        """)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def check_email(db_file,user:str) -> bool:
    """ checking if email exists in the SQLite database """
    try:
        conn = sqlite3.connect(r"Accord.db")
        cursor = conn.cursor()
        for query in c.fetchall():
            if user in query:
                return True
            else:
                return False
    except Error as e:
        return False


def add_user_email(db_file,user:str) -> bool:
    """ adding user email into the SQLite database """
    try:
        conn = sqlite3.connect(r"Accord.db")
        cursor = conn.cursor()
        sqlite_insert_with_param = """
                    INSERT INTO users
                    (email)
                    VALUES(?);
                    """
        cursor.execute(sqlite_insert_with_param,user)
        conn.commit()
        return True
    except Error as e:
        return False
    

if __name__ == '__main__':
    initalize_database(r"Accord.db")
    