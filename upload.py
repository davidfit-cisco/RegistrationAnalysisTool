import os

from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from process_csv import process_csv
from download import download

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

            filename = secure_filename(file_to_upload.filename)
            filetype = file_to_upload.filename.split(".")[-1]
            file_contents = file_to_upload.stream.read().decode('utf-8')

            return process_csv(file_contents)
            # return download(f"{filename}_edited.{filetype}", edited_file)
            # file_to_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash(f"Filetype {file_to_upload.content_type} not allowed")
            flash(f"Allowed filetypes are: {', '.join(list(ALLOWED_EXTENSIONS))}")
    return render_template('upload.html')
