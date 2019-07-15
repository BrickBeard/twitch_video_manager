from os import environ
from flask import Flask
from flask_cors import CORS
from .models import db

def create_app(config_file):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file, silent=True)
    if environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

    environ.update(
         USER_ID = str(app.config['TWITCH_USER_ID'])
    )
    
    print(app.config)

    CORS(app)

    db.init_app(app)
    
    from .site.views import site
    from .api.admin.routes import admin

    app.register_blueprint(site)
    app.register_blueprint(admin, url_prefix='/admin')

    return app

app = create_app('flask.cfg')