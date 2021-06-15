import csv
import os
from io import StringIO
import openpyxl
from flask import render_template

from utils import is_date, add_date_to_main_data, should_process_row, is_registered, is_unregistered


def process_csv(file_contents):
    main_data = {}
    readfile = csv.reader(StringIO(file_contents))
    column_indexes = process_title_row(readfile, main_data)
    closed_stores = get_closed_stores()

    for index, row in enumerate(list(readfile)):
        if should_process_row(closed_stores, column_indexes, row):
            process_row(row, column_indexes, main_data)

    print(main_data)
    return render_template('processed.html', main_data=main_data, days=list(main_data.keys()))


def process_row(row, column_indexes, main_data):
    device_type = row[column_indexes["device type"]]
    for day in list(main_data.keys()):
        initialise_day_data(day, device_type, main_data)
        add_registration_to_main_data(day, device_type, main_data, row)


def add_registration_to_main_data(day, device_type, main_data, row):
    reg_count = 0
    unregistered_count = 0
    column_count = len(main_data[day]["columns"])
    for column_index in main_data[day]["columns"]:
        cell = row[column_index]
        if is_registered(cell):
            reg_count += 1
        if is_unregistered(cell):
            unregistered_count += 1
    if reg_count == column_count:
        main_data[day]['Always'][device_type] += 1
    elif unregistered_count == column_count:
        main_data[day]['Never'][device_type] += 1
    else:
        main_data[day]['Sometimes'][device_type] += 1


def initialise_day_data(day, device_type, main_data):
    if device_type not in main_data[day]['Always']:
        for option in ('Always', 'Sometimes', 'Never'):
            main_data[day][option][device_type] = 0


def process_title_row(readfile, main_data):
    title_row = next(readfile)

    column_indexes = {}
    for index, column_name in enumerate(title_row):
        column_indexes[column_name.lower()] = index
        if is_date(column_name):
            add_date_to_main_data(index, column_name, main_data)
    return column_indexes


def get_closed_stores(closed_stores_filename="Closed_DG_Stores_27_May.xlsx"):
    wb = openpyxl.load_workbook(os.path.join("docs", closed_stores_filename))
    closed_sheet = wb["closed shops"]
    return [row[0].value for row in closed_sheet.rows if row[0].value]


# Constraints

# First row of csv file must be column titles
