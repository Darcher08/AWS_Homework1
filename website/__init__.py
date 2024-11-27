from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Inicializar Flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'askldjlasd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Aaggh5kj7@flaskappdb.c21fjnvngsvf.us-east-1.rds.amazonaws.com:3306/flaskappdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Importar las páginas creadas
    from .viewsAlumno import viewsA
    from .viewsProfesor import viewsP

    # Blueprints
    app.register_blueprint(viewsA, url_prefix='/')
    app.register_blueprint(viewsP, url_prefix='/')

    return app

