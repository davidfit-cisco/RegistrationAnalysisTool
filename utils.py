import pprint
import re
from calendar import month_name
from copy import deepcopy

short_month_names = [month[:3] for month in month_name[1:]]


def is_date(cell):
    month_pattern = '|^'.join(short_month_names)
    return True if re.search(month_pattern, cell, re.IGNORECASE) else False


def is_registered(cell):
    return True if re.search(r'REG', cell, re.IGNORECASE) else False


def is_unregistered(cell):
    return False if re.search(r'REG|AGE', cell, re.IGNORECASE) else True


def add_date_to_data(index, cell, main_data):
    daily_data = {
        "Always": {},
        "Sometimes": {},
        "Never": {},
        "columns": []
    }
    month = re.search(r'[a-zA-Z]+', cell).group()
    date = re.search(r'\d+', cell).group()
    date_string = f'{month} {date}'
    if date_string not in main_data:
        main_data[date_string] = deepcopy(daily_data)
    main_data[date_string]["columns"].append(index)


class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']

        pprint.pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)


def is_open_dg_store(closed_stores, column_indexes, row):
    return "lab" not in row[column_indexes["name1"]].lower() \
           and "Dollar General" in row[column_indexes["name2"]] \
           and row[column_indexes["name1"]] not in closed_stores


def is_tcp_store(tcp_stores, column_indexes, row):
    return row[column_indexes["name1"]] in tcp_stores
