from flask import Flask
from assets import register_assets


# Entry point to application
def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'
    with app.app_context():
        from db.db import init_db
        import routes  # Contrary to PEP, this import here is vital
        init_db()
    register_assets(app)
    return app


if __name__ == '__main__':
    # from utils import LoggingMiddleware
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    reg_state_app = create_app()
    reg_state_app.run(debug=True)
