class calculoDeDeducciones:
    def __init__(self, bruto):
        if bruto < 0:
            raise ValueError("El bruto no puede ser negativo.")
        self.bruto = float(bruto)

    def impuesto_sobre_la_renta(self):
        b = self.bruto
        if b <= 922000:
            return 0.0
        elif b <= 1352000:
            return (b - 922000) * 0.10
        elif b <= 2373000:
            return (1352000 - 922000) * 0.10 + (b - 1352000) * 0.15
        elif b <= 4745000:
            return (1352000 - 922000) * 0.10 + (2373000 - 1352000) * 0.15 + (b - 2373000) * 0.20
        else:
            return ((1352000 - 922000) * 0.10 +
                    (2373000 - 1352000) * 0.15 +
                    (4745000 - 2373000) * 0.20 +
                    (b - 4745000) * 0.25)

    def calcular_deducciones(self):
        try:
            ccss = round(self.bruto * 0.105, 2)
            banco = round(self.bruto * 0.01, 2)
            renta = round(self.impuesto_sobre_la_renta(), 2)

            total = round(ccss + banco + renta, 2)

            desglose = {
                "CCSS": ccss,
                "Banco": banco,
                "Impuesto sobre la Renta": renta
            }

            return {
                "Desglose": desglose,
                "Total": total,
                "Proceso": True,
                "Detalle": ""
            }

        except Exception as e:
            return {
                "Desglose": {},
                "Total": 0.0,
                "Proceso": False,
                "Detalle": f"Error al calcular deducciones: {e}"
            }

