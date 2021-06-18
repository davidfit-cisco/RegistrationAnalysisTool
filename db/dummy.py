from db.utils import query_db


def create_dummy_data():
    query_db('''
    INSERT INTO stores (name1, name2) 
    VALUES (?, ?)
    ''', [("DGC#17458", "Dollar General Corporation"),
          ("DGC#99999", "Dollar General Corporation")], exec_many=True)

    query_db('''
    INSERT INTO devices (mac, version, user_agent, store_id)
    VALUES (?, ?, ?, ?)
    ''', [("MAC_ADDRESS_1", "V1", 0, 1),
          ("MAC_ADDRESS_2", "V1", 1, 2)], exec_many=True)

    for i in range(5):
        query_db(f'''
        INSERT INTO days (date)
        VALUES (DATE(datetime('now', '-{i} day', 'localtime')))
        ''')

    for i in range(1, 5):
        query_db('''
        INSERT INTO snapshots (state, number, device_id, store_id, day_id)
        VALUES (?, ?, ?, ?, ?)
        ''', ("REGISTERED", i, 1, 1, 1))