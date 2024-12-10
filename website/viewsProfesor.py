from flask import Flask, Blueprint, request, flash, jsonify, make_response
from . import db
from flask_sqlalchemy import SQLAlchemy
import json 

viewsP = Blueprint('viewsProfesor', __name__)
from .models import Profesor, profesores, profesor_to_dict

# Datos de los profesores
def profesoresAll():
    return Profesor.query.all()

#! GET PROFESOR
@viewsP.route('/profesores', methods=['GET'])
def getProfesor():
    """
    Se obtienen todos los profesores y se convierten a un diccionario
    con el motivo de poder jsonificarlos y mostrarlos.
    Se verifica que haya al menos un profesor
    """
    profesores = profesoresAll()
    profesor_dict = [profesor_to_dict(profesor) for profesor in profesores]
    
    if len(profesor_dict) > 0:
        return make_response(jsonify({"profesores": profesor_dict}), 200)
    
    return make_response(jsonify({"message": "Sin profesores disponibles para mostrar"}), 404)

#! GET PROFESOR ID
@viewsP.route('/profesores/<int:profesor_id>', methods=['GET'])
def getProfesorId(profesor_id):
    """
    Se hace directamente el query que busca el id del alumno
    si no lo encuentra te arroja un mensaje de que no se hallo.

    """

    profesor = Profesor.query.get(profesor_id)

    if profesor:
        return make_response(jsonify(profesor_to_dict(profesor)), 200)
    
    return make_response(jsonify({"message": "Profesor no encontrado"}), 404)



#! POST PROFESOR
@viewsP.route('/profesores', methods=['POST'])
def addProfesor():
    """
    Se recupera la entrada json y se filtra para ver que no se haya
    ingresado algun tipo de dato erroneo. 
    Se crea la instancia alumno a la cual se le hara el commit
    """

    data = request.json
    
    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('apellidos') is None or data.get('numeroEmpleado') is None or data.get('horasClase') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos', 'numeroEmpleado' y 'horasClase' son obligatorios y no pueden estar vacíos"}), 400)
    
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('numeroEmpleado') < 0 or data.get('horasClase') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    
    nuevo_profesor = Profesor(
        id             = data.get('id'),
        numeroEmpleado = data.get('numeroEmpleado'),
        nombres        = data.get('nombres'),
        apellidos      = data.get('apellidos'),
        horasClase     = data.get('horasClase')
    )

    db.session.add(nuevo_profesor)
    db.session.commit()

    profesor_id = nuevo_profesor.id

    return make_response(jsonify({"id": profesor_id}), 201)


#! PUT PROFESOR
@viewsP.route('/profesores/<int:profesor_id>', methods=['PUT'])
def updateProfesor(profesor_id):
    """
    Mismo concepto que el POST, solo que ahora no se hace un add
    simplemente se hace un commit para actualizar los datos.
    
    """
    
    # Recuperar la tabla de profesores
    data = request.json

    # Validar campos obligatorios y sus valores
    if data.get('nombres') is None or data.get('horasClase') is None:
        return make_response(jsonify({"message": "Los campos 'nombres' y 'horasClase' son obligatorios y no pueden estar vacíos"}), 400)

    if data.get('nombres') == "" or data.get('horasClase') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    
    # Buscar el profesor por ID
    profesor = Profesor.query.get(profesor_id)

    if profesor:
        # Actualizar los datos del profesor
        profesor.numeroEmpleado = data.get('numeroEmpleado', profesor.numeroEmpleado)
        profesor.nombres        = data.get('nombres', profesor.nombres)
        profesor.apellidos      = data.get('apellidos', profesor.apellidos)
        profesor.horasClase     = data.get('horasClase', profesor.horasClase)

        db.session.commit()
        return make_response(jsonify({"message": "Profesor actualizado exitosamente", "Profesor": profesor_to_dict(profesor)}), 200)
   
    return make_response(jsonify({"message": f"No se encontró al profesor con id {profesor_id}"}), 404)


#! DELETE PROFESOR
@viewsP.route('/profesores/<int:profesor_id>', methods=['DELETE'])
def deleteProfesor(profesor_id):
    profesor = Profesor.query.get(profesor_id)

    if profesor:
        db.session.delete(profesor)
        db.session.commit()
        return make_response(jsonify({"message": "Profesor eliminado exitosamente", "Profesor": profesor_to_dict(profesor)}), 200)
    
    return make_response(jsonify({"message": "Profesor no encontrado"}), 404)
