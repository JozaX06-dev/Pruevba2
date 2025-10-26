class Empleado:
    def __init__(self, id, nombre, apellido, departamento, puesto, salario_base, tipo_contrato):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.departamento = departamento
        self.puesto = puesto
        self.salario_base = salario_base
        self.tipo_contrato = tipo_contrato

    def __str__(self):
        return f"Empleado[ID: {self.id}, Nombre: {self.nombre} {self.apellido}, Departamento: {self.departamento}, Puesto: {self.puesto}, Salario Base: {self.salario_base}, Tipo de Contrato: {self.tipo_contrato}]"



