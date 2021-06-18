from flask import g, current_app

from db.dummy import create_dummy_data
from db.tables import create_stores, create_devices, create_days, create_snapshots
from db.utils import query_db, print_table


def init_db():
    # Create Tables
    create_stores()
    create_devices()
    create_days()
    create_snapshots()

    # Populate DB with test data
    create_dummy_data()

    for table in ["stores", "devices", "days", "snapshots"]:
        print_table(table)


@current_app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
