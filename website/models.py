from flask_sqlalchemy import SQLAlchemy
from . import db

# Definir los modelos
class Alumno(db.Model):
    __tablename__ = 'Alumno'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(150))
    apellidos = db.Column(db.String(150))
    matricula = db.Column(db.String(45), unique=True)
    promedio = db.Column(db.Float)
    password = db.Column(db.String(45))
    fotoPerfilUrl = db.Column(db.String(150))

class Profesor(db.Model):
    __tablename__ = 'Profesor'
    id = db.Column(db.Integer, primary_key=True)
    numeroEmpleado = db.Column(db.String(150), unique=True)
    nombres = db.Column(db.String(150))
    apellidos = db.Column(db.String(150))
    horasClase = db.Column(db.Integer)


alumnos = []
profesores = []
 
def alumno_to_dict(alumno):
    return {
        "id": alumno.id,
        "nombres": alumno.nombres,
        "apellidos": alumno.apellidos,
        "matricula": alumno.matricula,
        "promedio": alumno.promedio,
        "fotoPerfilUrl": alumno.fotoPerfilUrl,
        "password": alumno.password
    }
    
def profesor_to_dict(profesor):
    return {
        "id": profesor.id,
        "numeroEmpleado": profesor.numeroEmpleado,
        "nombres": profesor.nombres, 
        "apellidos": profesor.apellidos, 
        "horasClase": profesor.horasClase
    }
