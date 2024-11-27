from flask import Flask, Blueprint, request, flash, jsonify, make_response
from . import db
from flask_sqlalchemy import SQLAlchemy
import json

viewsA = Blueprint('viewsAlumno', __name__)
from .models import Alumno, alumnos, alumno_to_dict

# Datos de alumnos
def alumnosAll():
    return Alumno.query.all()


#create all the routes that the REST api gonna use

@viewsA.route('/')
def home():
    return '<p>AWS Primera Entrega</p><br><p>Luis Palma</p>'

@viewsA.route('/test')
def test():
    # Crear un nuevo alumno
    nuevo_alumno = Alumno(
        nombres='Luis',
        apellidos='Palma',
        matricula='123456',
        promedio=9.5
    )
    
    # Agregar el nuevo alumno a la sesión de la base de datos
    db.session.add(nuevo_alumno)
    db.session.commit()
    
    # Devolver una respuesta JSON con los datos del nuevo alumno
    return jsonify(alumno_to_dict(nuevo_alumno))

#! GET ALUMNOS
@viewsA.route('/alumnos', methods=['GET'])
def getAlumnos():  

    """
    Se obtienen todos los alumnos y se convierten a un diccionario
    con el motivo de poder jsonificarlos y mostrarlos.
    Se verifica que haya al menos un alumno
    """
    alumnos = alumnosAll()
    alumnos_dict = [alumno_to_dict(alumno) for alumno in alumnos]

    if len(alumnos_dict) > 0:
        return make_response(jsonify({"alumnos": alumnos_dict}), 200)
    
    return make_response(jsonify({"message": "Sin alumnos disponibles para mostrar"}), 404)

#! GET ALUMNOS ID 
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['GET'])
def getAlumnosId(alumnos_id):
    """
    Se hace directamente el query que busca el id del alumno
    si no lo encuentra te arroja un mensaje de que no se hallo.

    """
    alumno = Alumno.query.get(alumnos_id)

    if alumno:
        return make_response(jsonify(alumno_to_dict(alumno)), 200)
    
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)


#! POST ALUMNOS
@viewsA.route('/alumnos', methods=['POST'])
def addAlumnos():
    """
    Se recupera la entrada json y se filtra para ver que no se haya
    ingresado algun tipo de dato erroneo. 
    Se crea la instancia alumno a la cual se le hara el commit
    """
    #* verificar que todos los campos no esten vacios
    data = request.json 

    
    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('apellidos') is None or data.get('promedio') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos' y 'promedio' son obligatorios y no pueden estar vacíos"}), 400)
    
    # Validar valores específicos
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('promedio') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    
    nuevo_alumno = Alumno(
        nombres = request.json['nombres'],
        apellidos = request.json['apellidos'],
        matricula = request.json['matricula'],
        promedio = request.json['promedio']
    )

    db.session.add(nuevo_alumno)
    db.session.commit() 

    return make_response(jsonify({"message": "Alumno agregado exitosamente"}), 201)

#! PUT ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['PUT'])
def updateAlumno(alumnos_id):
    """
    Mismo concepto que el POST, solo que ahora no se hace un add
    simplemente se hace un commit para actualizar los datos.
    
    """
    data = request.json 
    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('apellidos') is None or data.get('promedio') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos' y 'promedio' son obligatorios y no pueden estar vacíos"}), 400)
    
    # Validar valores específicos
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('promedio') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)    
    
    # Buscar el alumno por ID
    alumno = Alumno.query.get(alumnos_id)

    if alumno:
        # Actualizar los datos del alumno 
        alumno.nombres   = data.get('nombres', alumno.nombres)
        alumno.apellidos = data.get('apellidos', alumno.apellidos)
        alumno.matricula = data.get('matricula', alumno.matricula)
        alumno.promedio  = data.get('promedio', alumno.promedio)
        
        db.session.commit()
        return make_response(jsonify({"message": "Alumno actualizado exitosamente", "Alumno": alumno_to_dict(alumno)}), 200)
        
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)



#! DELETE ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['DELETE'])
def deleteAlumno(alumnos_id):
    alumno = Alumno.query.get(alumnos_id)
    if alumno:
        db.session.delete(alumno)
        db.session.commit()
        return make_response(jsonify({"message": "Alumno eliminado exitosamente", "Alumno": alumno_to_dict(alumno)}), 200)
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)
