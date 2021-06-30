from flask import Flask
from assets import register_assets


# Entry point to application
def create_app():
    reg_state_app = Flask(__name__)
    reg_state_app.secret_key = 'secret'
    with reg_state_app.app_context():
        import routes  # Contrary to PEP, this import here is vital
        # from db.db import init_db
        # init_db()
        register_assets()
    return reg_state_app


if __name__ == '__main__':
    # from utils import LoggingMiddleware
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app = create_app()
    app.run(debug=True)
