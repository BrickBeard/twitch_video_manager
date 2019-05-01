from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('dev.cfg')
    
    from .site.views import site

    app.register_blueprint(site)

    return app

app = create_app()
