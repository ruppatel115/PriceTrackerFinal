import sqlite3
from sqlite3 import Error



conn = sqlite3.connect('PriceWatcher.db')
c = conn.cursor()
def create_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Items(id integer, url Text, price integer, emailid integer, userid integer )')
    c.execute('CREATE TABLE IF NOT EXISTS Users(id integer, name Text, password integer, emailid integer)')
    c.execute('CREATE TABLE IF NOT EXISTS Email(id integer, email Text)')

if __name__ == '__main__':
    create_table()