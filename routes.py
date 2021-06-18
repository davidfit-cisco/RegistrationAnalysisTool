from flask import current_app, render_template
from upload import transform_csv


@current_app.route('/', methods=['GET', 'POST'])
def uploadfile():
    return transform_csv(current_app)


@current_app.route('/test')
def test():
    return render_template("test.html")
