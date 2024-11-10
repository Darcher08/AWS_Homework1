from flask import Flask, Blueprint, request, flash, jsonify, make_response
import json 

viewsP = Blueprint('viewsProfesor', __name__)

from .models import Profesor, profesores, profesor_to_dict

#! GET PROFESOR
@viewsP.route('/profesores', methods=['GET'])
def getProfesor():
    profesor_dict = [profesor_to_dict(profesor) for profesor in profesores]
    if len(profesor_dict) > 0:
        return make_response(jsonify({"profesores": profesor_dict}), 200)
    
    return make_response(jsonify({"message": "Sin profesores disponibles para mostrar"}), 404)

#! GET PROFESOR ID
@viewsP.route('/profesores/<int:profesor_id>', methods=['GET'])
def getProfesorId(profesor_id):
    profesor = next((profesor for profesor in profesores if profesor.id == profesor_id), None)
    
    if profesor:
        return make_response(jsonify(profesor_to_dict(profesor)), 200)
    
    return make_response(jsonify({"message": "Profesor no encontrado"}), 404)



#! POST PROFESOR
@viewsP.route('/profesores', methods=['POST'])
def addProfesor():
    data = request.json
    
    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('apellidos') is None or data.get('numeroEmpleado') is None or data.get('horasClase') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos', 'numeroEmpleado' y 'horasClase' son obligatorios y no pueden estar vacíos"}), 400)
    
    # Validar valores específicos
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('numeroEmpleado') < 0 or data.get('horasClase') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    
    nuevo_profesor = Profesor(
        id = data['id'],
        numeroEmpleado = data['numeroEmpleado'],
        nombres = data['nombres'],
        apellidos = data['apellidos'],
        horasClase = data['horasClase']
    )

    profesores.append(nuevo_profesor)
    return make_response(jsonify({"message": "Profesor agregado exitosamente"}), 201)


#! PUT PROFESOR
@viewsP.route('/profesores/<int:profesor_id>', methods=['PUT'])
def updateProfesor(profesor_id):
    data = request.json
    
    # Validar campos obligatorios y sus valores
    if data.get('nombres') is None or data.get('horasClase') is None:
        return make_response(jsonify({"message": "Los campos 'nombres' y 'horasClase' son obligatorios y no pueden estar vacíos"}), 400)
    
    # Validar valores específicos
    if data.get('nombres') == "" or data.get('horasClase') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    
    for profesor in profesores:
        if profesor.id == profesor_id:
            profesor.numeroEmpleado = data.get('numeroEmpleado', profesor.numeroEmpleado)
            profesor.nombres        = data.get('nombres', profesor.nombres)
            profesor.apellidos      = data.get('apellidos', profesor.apellidos)
            profesor.horasClase     = data.get('horasClase', profesor.horasClase)

            return make_response(jsonify({"message": "Profesor actualizado exitosamente", "Profesor": profesor_to_dict(profesor)}), 200)
   
    return make_response(jsonify({"message": f"No se encontró al profesor con id {profesor_id}"}), 404)

#! DELETE PROFESOR
@viewsP.route('/profesores/<int:profesor_id>', methods=['DELETE'])
def deleteProfesor(profesor_id):
    for profesor in profesores: 
        if profesor.id == profesor_id:
            profesores.remove(profesor)
            return make_response(jsonify({"message": "Profesor eliminado exitosamente", "Profesor": profesor_to_dict(profesor)}), 200)
        
    return make_response(jsonify({"message": "Profesor no encontrado"}), 404)
