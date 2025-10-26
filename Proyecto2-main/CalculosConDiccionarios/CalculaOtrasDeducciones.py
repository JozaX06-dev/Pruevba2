class calculoDeDeduccionesExtras:
    def __init__(self, bruto, deduccion_extra, tipo_deduccion):
        if bruto < 0:
            raise ValueError("El bruto no puede ser negativo.")
        else:
            self.bruto = float(bruto)
        self.deduccion_extra = deduccion_extra
        self.tipo_deduccion = tipo_deduccion


    #El ROUND ES REDONDEAR A 2 DECIMALES
    def tipo_seleccionada(self):
        bruto = self.bruto
        return {
            "Voluntaria": {
                "Seguro privado": round(bruto * 0.03, 2),
                "Fondo de Pensiones": round(bruto * 0.05, 2),
                "Donacion Opcional": 10000.0
            },
            "Contrato": {
                "Prestamo privado": round(bruto * 0.05, 2),
                "Ahorro": round(bruto * 0.02, 2)
            },
            "Judicial": {
                "Embargo": round(bruto * 0.15, 2),
                "Pensión alimentaria": round(bruto * 0.35, 2)
            }
        }.get(self.tipo_deduccion, {})

    def calcular_deduccion_extra(self):
        tipo = self.tipo_seleccionada()
        monto = tipo.get(self.deduccion_extra)

        if monto is None:
            return {
                "Desglose": {},
                "Total": 0.0,
                "Proceso": False,
                "Detalle": f"Deducción '{self.deduccion_extra}' no encontrada en tipo '{self.tipo_deduccion}'."
            }

        return {
            "Desglose": {self.deduccion_extra: monto},
            "Total": monto,
            "Proceso": True,
            "Detalle": f"Deducción '{self.deduccion_extra}' aplicada correctamente."
        }
