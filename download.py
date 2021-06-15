from flask import make_response


def download(filename, file_contents):
    response = make_response(file_contents)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
