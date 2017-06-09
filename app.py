from urllib.parse import parse_qs
from html import escape
import sqlite3

# Path to sqlite3 DB file
DB_FILE = './db/test.db'
DB_INITSCRIPT = './db/init.sql'


# Make and init db
def db_init():
    with sqlite3.connect(DB_FILE) as conn:
        #Read init sql script and execute
        with open(DB_INITSCRIPT,'r',encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)
        conn.commit()


# html.escape
def app_wsgi(envire, f_call):
    pass

if __name__ == '__main__':
    db_init()