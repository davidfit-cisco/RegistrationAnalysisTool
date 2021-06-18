from db.utils import query_db


def create_stores():
    query_db("""CREATE TABLE stores 
    (
    id INTEGER NOT NULL PRIMARY KEY,
    name1 TEXT,
    name2 TEXT
    )""")


def create_devices():
    query_db("""CREATE TABLE devices
    (
    id INTEGER NOT NULL PRIMARY KEY,
    mac TEXT,
    version TEXT,
    user_agent BOOLEAN NOT NULL CHECK (user_agent IN (0,1)),
    store_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores (id)
    )""")


def create_days():
    query_db("""CREATE TABLE days
    (
    id INTEGER NOT NULL PRIMARY KEY,
    date TEXT
    )""")


def create_snapshots():
    query_db("""CREATE TABLE snapshots
    (
    id INTEGER NOT NULL PRIMARY KEY,
    state TEXT,
    number INTEGER,
    device_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    day_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices (id),
    FOREIGN KEY (store_id) REFERENCES stores (id),
    FOREIGN KEY (day_id) REFERENCES days (id)
    )""")