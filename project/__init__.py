from flask import Flask

def create_app(config_file):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file, silent=True)
    
    from .site.views import site

    app.register_blueprint(site)

    return app

app = create_app('flask.cfg')