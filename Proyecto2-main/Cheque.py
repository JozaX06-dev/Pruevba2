class Cheque:
    def __init__(self, empleado, tipo, monto, fecha_emision, fecha_cobro):
        self.empleado = empleado
        self.tipo = tipo
        self.monto = monto
        self.fecha_emision = fecha_emision
        self.fecha_cobro = fecha_cobro

    def __str__(self):
        return f"Empleado: {self.empleado}, Tipo: {self.tipo}, Monto: {self.monto}, Fecha de Emisión: {self.fecha_emision}, Fecha de Cobro: {self.fecha_cobro}"
