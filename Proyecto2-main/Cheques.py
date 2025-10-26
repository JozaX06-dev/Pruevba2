#Donde se calculan 
from HorasExtras import HorasExtras

#esto se puede pasar a empresa.py 

class Cheques:
    #info del empleado
    def __init__(self, nombre, apellido, horas, valor_hora, salario_bruto, horas_extra):
        self.nombre = nombre
        self.apellido = apellido
        self.horas = horas
        self.valor_hora = valor_hora
        self.salario_bruto = salario_bruto
        self.horas_extra = horas_extra

    
       
