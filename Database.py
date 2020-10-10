import sqlite3
from sqlite3 import Error

DATABASE_FILE = r"Accord.db"

def initalize_database():
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
    print("here")


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
    

if __name__ == '__main__':
    # initalize_database(r"Accord.db")
    print(check_email("pavle.rohalj@pomona.edu"))
    print(add_user_email("pavle.rohalj@pomona.edu"))
    print(check_email("pavle.rohalj@pomona.edu"))
    