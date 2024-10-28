class Alumno():
    def __init__(self, id, nombres, apellidos, matricula, promedio):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio

class Profesor():
    def __init__(self, id, numeroEmpleado, nombres, apellidos, horasClase):
        self.id = id
        self.numeroEmpleado = numeroEmpleado
        self.nombres = nombres
        self.apellidos = apellidos
        self.horasClase = horasClase


alumnos = [
    Alumno(1, "Juan", "Pérez", "A001", 9.5),
    Alumno(2, "Ana", "García", "A002", 8.7),
    Alumno(3, "Luis", "Martínez", "A003", 9.0)
]


profesores = [

    Profesor(1, "P001", "Carlos", "López", 20),
    Profesor(2, "P002", "María", "Fernández", 15)
]


def alumno_to_dict(alumno):
    return {
        "id": alumno.id,
        "nombres": alumno.nombres,
        "apellidos": alumno.apellidos,
        "matricula": alumno.matricula,
        "promedio": alumno.promedio
    }

def profesor_to_dict(profesor):
    return {
        "id": profesor.id,
        "numeroEmpleado": profesor.numeroEmpleado,
        "nombres": profesor.nombres, 
        "apellidos": profesor.apellidos, 
        "horasClase": profesor.horasClase
    }


def actualizarID(id, lista):
    for i in range(id-1,len(lista)):
        lista[i].id = i + 1