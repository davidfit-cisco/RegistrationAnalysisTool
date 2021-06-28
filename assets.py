from flask_assets import Environment, Bundle
from flask import current_app


def register_assets():
    assets = Environment(current_app)
    css = Bundle('css/main.scss', filters='pyscss', output='gen/all.css')
    assets.register('all_css', css)
