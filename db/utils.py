import sqlite3
from flask import g
DATABASE = ':memory:'


def query_db(query, args=(), one=False, exec_many=False):
    con = get_db()
    if exec_many:
        cur = con.executemany(query, args)
    else:
        cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    con.commit()
    return (rv[0] if rv else None) if one else rv


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def print_table(table):
    rows = query_db(f'''SELECT * FROM {table}''')
    for row in rows:
        print(dict(row))