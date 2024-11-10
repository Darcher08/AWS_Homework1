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


alumnos = []


profesores = []


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
