from upload import transform_csv
from flask import Flask, render_template
from assets import register_assets
from utils import LoggingMiddleware

# UPLOAD_FOLDER = 'temp'


app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret'

register_assets(app)


@app.route('/', methods=['GET', 'POST'])
def uploadfile():
    return transform_csv(app)


if __name__ == '__main__':
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(debug=True)
