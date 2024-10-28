from flask import Flask, Blueprint, request ,flash, jsonify
import json 

viewsP = Blueprint('viewsProfesor', __name__)

from .models import Profesor, profesores, profesor_to_dict, actualizarID

#! GET PROFESOR
@viewsP.route('/profesores', methods=['GET'])
def getProfesor():
    profesor_dict = [profesor_to_dict(profesor) for profesor in profesores]
    if len(profesor_dict) > 0:
        return jsonify({"profesores": profesor_dict})

    return jsonify({"message": "Sin profesores disponibles para mostrar"})


#! GET PROFESOR ID
@viewsP.route('/profesores/<int:profesor_id>')
def getProfesorId(profesor_id):
    profesor_ditc = [profesor_to_dict(profesor) for profesor in profesores if profesor.id == profesor_id]
    
    if len(profesor_ditc) > 0:
        return jsonify({"Profesor": profesor_ditc[0]})
    
    return jsonify({"message": "Profesor no encontrado"})


#! POST PROFESOR
@viewsP.route('/profesores', methods=['POST'])
def addProfesor():
    last_profesor = len(profesores)

    data = request.json
    fields = ['nombres','apellidos','numeroEmpleado', 'horasClase']

    for field in fields:
        if not data.get(field):
            return jsonify({"message": f"El campo {field} es obligatorio y no puede estar vacio"})
    
    nuevo_profesor = Profesor(
        id = int(last_profesor +  1),
        numeroEmpleado= request.json['numeroEmpleado'],
        nombres= request.json['nombres'],
        apellidos= request.json['apellidos'],
        horasClase= request.json['horasClase']
    )

    profesores.append(nuevo_profesor)
    return jsonify({"message": "Profesor agregado exitosamente"})


#! PUT PROFESOR
@viewsP.route('/profesores/<int:profesor_id>', methods=['PUT'])
def updateProfesor(profesor_id):
    data = request.json

    for profesor in profesores:
        if profesor.id == profesor_id: 

            profesor.numeroEmpleado = data.get('numeroEmpleado', profesor.numeroEmpleado)
            profesor.nombres        = data.get('nombres', profesor.nombres)
            profesor.apellidos      = data.get('apellidos', profesor.apellidos)
            profesor.horasClase     = data.get('horasClase', profesor.horasClase)

            return jsonify({"message": "Profesor actualizado exitosamente", "Profesor": profesor_to_dict(profesor)})
   
    return jsonify({"message": "No se encontro al profesor con id {profesor_id}"})


#! DELETE PROFESOR
@viewsP.route('/profesores/<int:profesor_id>', methods=['DELETE'])
def deleteProfesor(profesor_id):
    for profesor in profesores: 
        if profesor.id == profesor_id:
            profesores.remove(profesor)
            actualizarID(profesor_id, profesores)
            return jsonify({"message": "Profesor eliminado exitosamente", "Alumno": profesor_to_dict(profesor)})
        
    return jsonify({"message": "Profesor no encontrado"})



