from flask import Flask
from os import path


JSON_NAME = 'jsonData.js'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'askldjlasd'

    from .viewsAlumno import viewsA
    from .viewsProfesor import viewsP
    app.register_blueprint(viewsA, url_prefix='/')
    app.register_blueprint(viewsP, url_prefix='/')
    
    return app
