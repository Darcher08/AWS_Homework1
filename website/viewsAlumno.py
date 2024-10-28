from flask import Flask, Blueprint, request, flash, jsonify
import json

viewsA = Blueprint('viewsAlumno', __name__)
from .models import Alumno, alumnos, alumno_to_dict, actualizarID

#create all the routes that the REST api gonna use

#! GET ALUMNOS
@viewsA.route('/alumnos', methods=['GET'])
def getAlumnos():
    alumnos_dict = [alumno_to_dict(alumno) for alumno in alumnos]
    if len(alumnos_dict) > 0:
        return jsonify({"alumnos": alumnos_dict})
    return jsonify({"message": "Sin alumnos disponibles para mostrar"})

#! GET ALUMNOS ID
@viewsA.route('/alumnos/<int:alumnos_id>')
def getAlumnosId(alumnos_id):
    alumnos_dict = [alumno_to_dict(alumno) for alumno in alumnos if alumno.id == alumnos_id]
    
    if len(alumnos_dict) > 0:
        return jsonify({"Alumno": alumnos_dict[0]})
    return jsonify({"message": "Alumno no encontrado"})

#! POST ALUMNOS
@viewsA.route('/alumnos', methods=['POST'])
def addAlumnos():
    lastAlumn = len(alumnos)

    #* verificar que todos los campos no esten vacios
    data = request.json
    fields = ['nombres', 'apellidos', 'matricula', 'promedio']
    for field in fields:
        if not data.get(field):
            return jsonify({"message": f"El campo {field} es obligatorio y no puede estar vacio"})

    nuevo_alumno = Alumno(
        id = int(lastAlumn + 1),
        nombres = request.json['nombres'],
        apellidos = request.json['apellidos'],
        matricula = request.json['matricula'],
        promedio = request.json['promedio']
    )

    alumnos.append(nuevo_alumno)
    return jsonify({"message": "Alumno agregado exitosamente"})

#! PUT ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['PUT'])
def updateAlumno(alumnos_id):
    data = request.json
    
    # Buscar el alumno por ID
    for alumno in alumnos:
        if alumno.id == alumnos_id:
              # Actualizar los datos del alumno
            
            alumno.nombres   = data.get('nombres', alumno.nombres)
            alumno.apellidos = data.get('apellidos', alumno.apellidos)
            alumno.matricula = data.get('matricula', alumno.matricula)
            alumno.promedio  = data.get('promedio', alumno.promedio)
    
            return jsonify({"message": "Alumno actualizado exitosamente", "Alumno": alumno_to_dict(alumno)})
    return jsonify({"message": "Alumno no encontrado"})


#! DELETE ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['DELETE'])
def deleteAlumno(alumnos_id):
    
    for alumno in alumnos:
        if alumno.id == alumnos_id:
            alumnos.remove(alumno)
            actualizarID(alumnos_id, alumnos)
            return jsonify({"message": "Alumno eliminado exitosamente", "Alumno": alumno_to_dict(alumno)})
    return jsonify({"message": "Alumno no encontrado"})

