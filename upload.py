import chardet
import pandas as pd
from flask import render_template, request, flash, redirect
from process_csv import process_csv


ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}


def file_is_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def transform_csv(app):
    if request.method == 'POST':
        file_to_upload = request.files['file_to_upload']
        if not file_to_upload:
            flash('No file selected')
        elif file_is_allowed(file_to_upload.filename):
            filetype = file_to_upload.filename.split(".")[-1]
            if filetype == 'xlsx':
                df = pd.read_excel(file_to_upload.stream.read())
                file_contents = df.to_csv()
            else:
                blob = file_to_upload.stream.read()
                encoding = chardet.detect(blob)['encoding']
                file_contents = blob.decode(encoding)
            return process_csv(file_contents)
        else:
            flash(f"Filetype {file_to_upload.content_type} not allowed")
            flash(f"Allowed filetypes are: {', '.join(list(ALLOWED_EXTENSIONS))}")
    return render_template('homepage.html')
