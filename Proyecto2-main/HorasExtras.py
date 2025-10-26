#Para empleados
#Y registros en el csv
class HorasExtras:
    def __init__(self, horas_extra, valor_hora):
        self.horas_extra = horas_extra
        self.valor_hora = valor_hora

    def calcular_horas_extras(self):
        if self.horas_extra > 0:
            return self.horas_extra * self.valor_hora * 1.5
        else:
            return 0

#Aqui posible diccionaria ya que las seria como nombre empleado(o cedula): horas extras acumuladas