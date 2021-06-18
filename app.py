from upload import transform_csv
from flask import Flask, render_template, current_app
from assets import register_assets
from utils import LoggingMiddleware


def create_app():
    app = Flask(__name__)
    # UPLOAD_FOLDER = 'temp'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = 'secret'
    with app.app_context():
        from db.db import init_db
        from db.utils import get_db
        import routes
        cur = get_db().cursor()
        init_db()
    register_assets(app)
    return app


if __name__ == '__main__':
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app = create_app()
    app.run(debug=True)
