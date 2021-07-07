import csv
import os
import openpyxl
from copy import deepcopy
from io import StringIO
from flask import render_template
from utils import is_date, add_date_to_data, is_open_dg_store, is_registered, is_unregistered, is_tcp_store


def process_csv(file_contents):
    tcp_never_macs = {}
    main_data = {}
    readfile = csv.reader(StringIO(file_contents))
    column_indexes = process_title_row(readfile, main_data)
    tcp_data = deepcopy(main_data)
    closed_stores = get_closed_stores()
    tcp_stores = get_tcp_stores()

    for index, row in enumerate(list(readfile)):
        if is_open_dg_store(closed_stores, column_indexes, row):
            process_row(row, column_indexes, main_data)

            if is_tcp_store(tcp_stores, column_indexes, row):
                process_row(row, column_indexes, tcp_data, tcp_never_macs=tcp_never_macs)

    return render_template('processed.html',
                           main_data=main_data, tcp_data=tcp_data,
                           tcp_never_macs=tcp_never_macs, days=list(main_data.keys()))


def process_row(row, column_indexes, data, tcp_never_macs=None):
    device_type = row[column_indexes["device type"]]
    for day in list(data.keys()):
        initialise_day_data(day, device_type, data, tcp_never_macs=tcp_never_macs)
        add_registration_to_data(day, device_type, data, row, column_indexes, tcp_never_macs=tcp_never_macs)


def add_registration_to_data(day, device_type, data, row, column_indexes, tcp_never_macs=None):
    reg_count = 0
    unregistered_count = 0
    column_count = len(data[day]["columns"])
    for column_index in data[day]["columns"]:
        cell = row[column_index]
        if is_registered(cell):
            reg_count += 1
        if is_unregistered(cell):
            unregistered_count += 1
    if reg_count == column_count:
        data[day]['Always'][device_type] += 1
    elif unregistered_count == column_count:
        data[day]['Never'][device_type] += 1
        if tcp_never_macs is not None and "SPA" in device_type.upper():
            tcp_never_macs[day].append(row[column_indexes["mac"]])
    else:
        data[day]['Sometimes'][device_type] += 1


def initialise_day_data(day, device_type, data, tcp_never_macs=None):
    if device_type not in data[day]['Always']:
        for option in ('Always', 'Sometimes', 'Never'):
            data[day][option][device_type] = 0
    if tcp_never_macs is not None and day not in tcp_never_macs:
        tcp_never_macs[day] = []


def process_title_row(readfile, data):
    title_row = next(readfile)

    column_indexes = {}
    for index, column_name in enumerate(title_row):
        column_indexes[column_name.lower()] = index
        if is_date(column_name):
            add_date_to_data(index, column_name, data)
    return column_indexes


def get_closed_stores(closed_stores_filename="Closed_DG_Stores_27_May.xlsx"):
    wb = openpyxl.load_workbook(os.path.join("docs", closed_stores_filename))
    closed_sheet = wb["closed shops"]
    return [row[0].value for row in closed_sheet.rows if row[0].value]


def get_tcp_stores(closed_stores_filename="TCP Conversion List 063021.xlsx"):
    wb = openpyxl.load_workbook(os.path.join("docs", closed_stores_filename))
    tcp_sheet = wb["TCP Conversion List 063021"]
    return [row[0].value for row in tcp_sheet.rows if row[0].value]


# Constraints
# First row of csv file must be column names
