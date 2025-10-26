from CalculosConDiccionarios.CalculaBrutoXHora import calculoDeSalarioBruto
from CalculosConDiccionarios.CalcularDeduccionNormal import calculoDeDeducciones
from CalculosPILAS.PilasParaCalculos import pila

BONO_DEPARTAMENTO = {
    "Ingeniería": 0.5,
    "Administración": 0.3,
    "Ventas": 0.4
}

class obtenerNetoXHoras:
    def __init__(self):
        self.pila = pila()

    def calcular_y_guardar(self, empleado, horas_trabajadas, tarifa_hora):
        if not isinstance(horas_trabajadas, (int, float)) or horas_trabajadas < 0:
            return {"success": False, "detalle": "Horas trabajadas inválidas."}
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            return {"success": False, "detalle": "Tarifa por hora inválida."}

        try:
            bono = BONO_DEPARTAMENTO.get(getattr(empleado, "departamento", ""), 0.0)

            calculador_bruto = calculoDeSalarioBruto(empleado, horas_trabajadas)
            resultado_bruto = calculador_bruto.calcular_bruto_x_hora()
            bruto = float(resultado_bruto.get("Bruto", 0.0))
            bruto = round(bruto, 2)

            bruto_bono = round(bruto * (1 + bono), 2)

            deducciones_obj = calculoDeDeducciones(bruto_bono)
            resultado_deducciones = deducciones_obj.calcular_deducciones()
            monto_deducciones = round(float(resultado_deducciones.get("Total", 0.0)), 2)

            neto = round(bruto_bono - monto_deducciones, 2)

            resultado = {
                "id": getattr(empleado, "id", None),
                "nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "departamento": getattr(empleado, "departamento", ""),
                "horas trabajadas": horas_trabajadas,
                "tarifa hora": tarifa_hora,
                "bono departamento": bono,
                "bruto": bruto,
                "bruto con bono": bruto_bono,
                "deducciones normales": monto_deducciones,
                "neto": neto,
                "proceso": True,
                "detalle": ""
            }

            self.pila.push(resultado)
            return resultado

        except Exception as e:
            return {"success": False, "Detalle": f"Error al calcular... {e}"}

    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()