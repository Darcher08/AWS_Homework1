# ORM
from flask import Flask, Blueprint, request, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json

# UUID generador
import uuid

# SKD AWS
import boto3
from boto3.dynamodb.conditions import Attr

# Utiles
from credenciales import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
import time
from . import db
from decimal import Decimal

# para generara un string aleatorio (128)
import secrets
import string


viewsA = Blueprint('viewsAlumno', __name__)
from .models import Alumno, alumnos, alumno_to_dict

# Datos de alumnos
def alumnosAll():
    return Alumno.query.all()


#create all the routes that the REST api gonna use

@viewsA.route('/')
def home(): 
    return '<p>AWS Primera Entrega</p><br><p>Luis Palma</p>'

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
    
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('promedio') < 0:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)
    
    
    nuevo_alumno = Alumno(
        nombres   = data.get('nombres'),
        apellidos = data.get('apellidos'),
        matricula = data.get('matricula'),
        promedio  = data.get('promedio'),
        password =  data.get('password')
    )

    db.session.add(nuevo_alumno)
    db.session.commit() 

    alumno_id = nuevo_alumno.id

    return make_response(jsonify({"id": alumno_id}), 201)


#! PUT ALUMNOS
@viewsA.route('/alumnos/<int:alumnos_id>', methods=['PUT'])
def updateAlumno(alumnos_id):
    """
    Mismo concepto que el POST, solo que ahora no se hace un add
    simplemente se hace un commit para actualizar los datos.
    
    """
    #recuperar la tabla de alumnos
    data = request.json 


    # Validar campos obligatorios y sus valores
    if not data.get('nombres') or data.get('nombres') == None or data.get('apellidos') is None or data.get('promedio') is None:
        return make_response(jsonify({"message": "Los campos 'nombres', 'apellidos' y 'promedio' son obligatorios y no pueden estar vacíos"}), 400)
    
    if data.get('id') == 0 or data.get('nombres') == "" or data.get('promedio') < 0 or data.get('matricula') is None:
        return make_response(jsonify({"message": "Los valores de los campos no son válidos"}), 400)    
    

    # Buscar el alumno por ID
    alumno = Alumno.query.get(alumnos_id)

    if alumno:
        # Actualizar los datos del alumno 
        alumno.nombres   = data.get('nombres', alumno.nombres)
        alumno.apellidos = data.get('apellidos', alumno.apellidos)
        alumno.matricula = data.get('matricula', alumno.matricula)
        alumno.promedio  = data.get('promedio', alumno.promedio)
        alumno.password  = data.get('password', alumno.password)
        
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


#? pendientes a verificar 

#! POST ALUMNOS FOTO DE PERFIL
@viewsA.route('/alumnos/<int:alumnos_id>/fotoPerfil', methods=['POST'])
def addAlumnosFotoPerfil(alumnos_id):
    """
     
    """
    s3 = boto3.client(
        's3',
        region_name='us-east-1',
        aws_access_key_id= AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
        aws_session_token= AWS_SESSION_TOKEN
        )

    #* verificar que todos los campos no esten vacios 
    
    alumno = Alumno.query.get(alumnos_id)
    
    if alumno:

        if 'foto' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['foto']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        # Sube el archivo a S3
        try:
            idAlumno = str(alumno.id)
            filename = f"{idAlumno}.{file.filename.split('.')[-1]}"  # Agrega la extensión original del archivo

            s3.upload_fileobj(
                file,
                'a16004219-api-rest',
                filename,
                ExtraArgs={'ContentType': file.content_type}
            )

            url = f'https://a16004219-api-rest.s3.amazonaws.com/{filename}'
            alumno.fotoPerfilUrl = url
            db.session.commit() 

            return jsonify({'fotoPerfilUrl': url}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return make_response(jsonify({"message": "Error inesperado"}), 500)

#! POST ALUMNOS SNS
@viewsA.route('/alumnos/<int:alumnos_id>/email', methods=['POST'])
def snsAlumnos(alumnos_id):

    sns = boto3.client(
        'sns',
        region_name='us-east-1',
        aws_access_key_id= AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
        aws_session_token= AWS_SESSION_TOKEN

        )
    
    alumno = Alumno.query.get(alumnos_id)

    if alumno:

        message = f'Alumno: {alumno.nombres} {alumno.apellidos}\nCalificación: {alumno.promedio}'
        subject = f'Calificaciones'

        response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:448264529393:sns-topic-PalmaLuis',
        Message= message,
        Subject= subject 
        )

        return make_response(jsonify({"message": "Notificacion enviada"}), 200)
    
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)

#! POST ALUMNOS SESSION 
@viewsA.route('/alumnos/<int:alumnos_id>/session/login', methods=['POST'])
def sessionSave(alumnos_id):
    
    """
    Este endpoint recibe la contraseña del alumno y la compara con su contraseña 
    actual en la base de datos.
    """

    def string_creator():
        caracteres = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(128))
    
    data = request.json 
    passwordJson = data['password']
    alumno = Alumno.query.get(alumnos_id)
    
    dynamoDB = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id= AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
        aws_session_token= AWS_SESSION_TOKEN

        )
    
    table_name = 'sesiones-alumnos'

    if alumno:
        # Comparación entre entrada y la base de datos
        if str(alumno.password) == str(passwordJson):
            
            id = str(uuid.uuid4())
            fecha = Decimal(time.time())
            alumnoId = Decimal(alumno.id)
            active = True
            sessionString = string_creator()

            item = {
                "id": {"S": id},
                "fecha": {"N": str(fecha)},
                "alumnoId": {"N": str(alumnoId)},
                "active": {"BOOL": active},
                "sessionString": {"S": sessionString}
            }

            dynamoDB.put_item(TableName=table_name, Item=item)
            
            return jsonify({"sessionString": sessionString}), 200

        return jsonify({"message": "Contraseña incorrecta"}), 400
    
    return make_response(jsonify({"message": "Alumno no encontrado"}), 404)

#! LOGOUT SESSION
@viewsA.route('/alumnos/<int:alumnos_id>/session/logout', methods=['POST'])
def sessionLogout(alumnos_id):
    data = request.json
    sessionString = data.get('sessionString')
    dynamoDB = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
   
    table_name = 'sesiones-alumnos'
    alumno = Alumno.query.get(alumnos_id)
   
    if alumno:
        # Buscar el item específico para actualizar
        response = dynamoDB.scan(
            TableName=table_name,
            FilterExpression='alumnoId = :alumnos_id AND sessionString = :session_string',
            ExpressionAttributeValues={
                ':alumnos_id': {'N': str(alumnos_id)},
                ':session_string': {'S': sessionString}
            },
            ProjectionExpression='id'
        )
        
        if 'Items' in response and response['Items']:
            # Obtener el ID del item
            item_id = response['Items'][0]['id']['S']
            
            try:
                # Actualizar el item para cambiar active a false
                update_response = dynamoDB.update_item(
                    TableName=table_name,
                    Key={'id': {'S': item_id}},
                    UpdateExpression='SET active = :val',
                    ExpressionAttributeValues={':val': {'BOOL': False}},
                    ReturnValues='UPDATED_NEW'
                )
                
                return jsonify({"message": "Sesión cerrada exitosamente"}), 200
            
            except Exception as e:
                # Manejo de errores
                print(f"Error al actualizar la sesión: {e}")
                return jsonify({"message": "Error al cerrar la sesión"}), 500
        
        return jsonify({"message": "Sesión no encontrada"}), 404
    
    return make_response(jsonify({"message": "Alumno no encontrado"})), 404


#! POST ALUMNOS SESSION VERIFY 
@viewsA.route('/alumnos/<int:alumnos_id>/session/verify', methods=['POST'])
def sessionVerify(alumnos_id):

    def convert_dynamo_to_python(dynamo_item):
        """
        Convierte un ítem de DynamoDB a un diccionario Python estándar
        """
        python_item = {}
        for key, value in dynamo_item.items():
            # Determina el tipo de dato y lo convierte
            if 'S' in value:  # String
                python_item[key] = value['S']
            elif 'N' in value:  # Número
                python_item[key] = int(value['N'])
            elif 'BOOL' in value:  # Boolean
                python_item[key] = value['BOOL']
            # Añada más tipos según necesite
        return python_item

    data = request.json
    sessionString = data.get('sessionString')

    dynamoDB = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    
    table_name = 'sesiones-alumnos'
    alumno = Alumno.query.get(alumnos_id)
    
    if alumno:
        # Realizar un Scan en DynamoDB
        response = dynamoDB.scan(
            TableName=table_name,
            FilterExpression='alumnoId = :alumnos_id',
            ExpressionAttributeValues={':alumnos_id': {'N': str(alumnos_id)}},
            ProjectionExpression='sessionString, active'
        )

        
        if 'Items' in response and response['Items']:

            python_item = convert_dynamo_to_python(response['Items'][0])

            # item = response['Items'][0]

            """ 
            dynamoSessionString = item['sessionString']['S']
            dynamoActive = item['active']['BOOL']
            """

            dynamoSessionString = python_item.get('sessionString')
            dynamoActive = python_item.get('active')
                
            if str(sessionString) == str(dynamoSessionString) and dynamoActive == True:
                return jsonify({"message": "Sesión activa"}), 200
        
        return jsonify({"message": "Algo inesperado ha ocurrido"}), 400

    return make_response(jsonify({"message": "Alumno no encontrado"})), 404

