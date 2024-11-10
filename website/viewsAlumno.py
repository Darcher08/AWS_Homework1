from flask import Flask, Blueprint, request, flash, jsonify, make_response
import json

viewsA = Blueprint('viewsAlumno', __name__)
from .models import Alumno, alumnos, alumno_to_dict

#create all the routes that the REST api gonna use

@viewsA.route('/')
def home():
    return '<p>AWS Primera Entrega</p><br><p>Luis Palma</p>'

#! GET ALUMNOS
@viewsA.route('/alumnos', methods=['GET'])
def getAlumnos():
    alumnos_dict = [alumno_to_dict(alumno) for alumno in alumnos]
    if len(alumnos_dict) > 0:
        return make_response(jsonify({"alumnos": alumnos_dict}), 200)
    return make_response(jsonify({"message": "Sin alumnos disponibles para mostrar"}), 404)

#! GET ALUMNOS ID
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['GET'])
def getAlumnosId(alumnos_id):
    alumno = next((alumno for alumno in alumnos if alumno.id == alumnos_id), None)
    
    if alumno:
        return make_response(jsonify(alumno_to_dict(alumno)), 200)
    
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)


#! POST ALUMNOS
@viewsA.route('/alumnos', methods=['POST'])
def addAlumnos():

    #* verificar que todos los campos no esten vacios
    data = request.json 

    
    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('apellidos') is None or data.get('promedio') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos' y 'promedio' son obligatorios y no pueden estar vacíos"}), 400)
    
    # Validar valores específicos
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('promedio') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    

    nuevo_alumno = Alumno(
        id = request.json['id'],
        nombres = request.json['nombres'],
        apellidos = request.json['apellidos'],
        matricula = request.json['matricula'],
        promedio = request.json['promedio']
    )

    alumnos.append(nuevo_alumno)
    return make_response(jsonify({"message": "Alumno agregado exitosamente"}), 201)

#! PUT ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['PUT'])
def updateAlumno(alumnos_id):
    data = request.json 

    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('apellidos') is None or data.get('promedio') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos' y 'promedio' son obligatorios y no pueden estar vacíos"}), 400)
    
    # Validar valores específicos
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('promedio') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)    
    
    # Buscar el alumno por ID
    for alumno in alumnos:
        if alumno.id == alumnos_id:
            # Actualizar los datos del alumno
            alumno.id        = data.get('id', alumno.id)
            alumno.nombres   = data.get('nombres', alumno.nombres)
            alumno.apellidos = data.get('apellidos', alumno.apellidos)
            alumno.matricula = data.get('matricula', alumno.matricula)
            alumno.promedio  = data.get('promedio', alumno.promedio)
            
            print(str(data.get('nombres', alumno.nombres)))
            return make_response(jsonify({"message": "Alumno actualizado exitosamente", "Alumno": alumno_to_dict(alumno)}), 200)
        
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)



#! DELETE ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['DELETE'])
def deleteAlumno(alumnos_id):
    
    for alumno in alumnos:
        if alumno.id == alumnos_id:
            alumnos.remove(alumno)
            return make_response(jsonify({"message": "Alumno eliminado exitosamente", "Alumno": alumno_to_dict(alumno)}), 200)
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)
