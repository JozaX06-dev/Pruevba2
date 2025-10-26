class calculoDeSalarioBruto:
    def __init__(self, empleado, horas_trabajadas):
        self.empleado = empleado
        self.horas_trabajadas = horas_trabajadas
    
    def obtener_precio_por_hora_del_empleado(self):
        try:
            tarifa_hora = float(getattr(self.empleado, "tarifa_hora", 0))
        except (ValueError, TypeError):
            tarifa_hora = 0.0
        return tarifa_hora

    def obtener_tarifa_base(self):
        try:
            tarifa_hora = float(getattr(self.empleado, "tarifa_hora", 0))
        except (ValueError, TypeError):
            tarifa_hora = 0.0
        return tarifa_hora

    def calcular_bruto_x_hora(self):
        tarifa_base = self.obtener_tarifa_base()
        if self.horas_trabajadas <= 8:
            tarifa_final = tarifa_base
            ajuste = "Sin ajuste"
        elif self.horas_trabajadas <= 16:
            tarifa_final = tarifa_base * 1.20
            ajuste = "Ajuste +20%"
        else:
            tarifa_final = tarifa_base * 1.50
            ajuste = "Ajuste +50%"

        bruto = round(self.horas_trabajadas * tarifa_final, 2)

        return {
            "Tarifa_base": round(tarifa_base, 2),
            "Tarifa_final": round(tarifa_final, 2),
            "Horas_trabajadas": self.horas_trabajadas,
            "Ajuste": ajuste,
            "Bruto": bruto
        }
