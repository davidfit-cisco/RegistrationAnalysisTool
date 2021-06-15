from flask_assets import Environment, Bundle


def register_assets(app):
    assets = Environment(app)
    css = Bundle('css/main.scss', filters='pyscss', output='gen/all.css')
    assets.register('all_css', css)