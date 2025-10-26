from collections import deque
from CalculosPILAS.CalcularNetoXContrato import calcularNetoXContrato
from CalculosPILAS.ObtenerNetoXHoras import obtenerNetoXHoras
class calculaNetoEmpleado:
    def __init__(self, empleados, horas_extras, tipo_cheque):
        self.empleados = empleados
        if horas_extras < 0:
            raise ValueError("horas_extras no puede ser negativo.")
        else:
            self.horas_extras = float(horas_extras)
        self.tipo_cheque = tipo_cheque
        #para cola
        self.cola_empleados = deque(list(empleados))
        self.cola_resultado = deque()

#esta clase manda a las otras hacer los calculos

#COLA PARA GUARDAR LOS RESULTADOS--------------------------------------------------------
    def encolar(self, resultado):
        self.cola_resultado.append(resultado)

    def desencolar(self):
        if not self.esta_vacia():
            return self.cola_resultado.popleft()
        return None
    
    def esta_vacia(self):
        cant = 0
        for _ in self.cola_resultado:
            cant += 1
        return cant == 0

#-----------------------------------------------------------------------------------------
    #def calcula_neto(self, empleado: Empleado)
    def obtener_neto_por_horas_extras(self, empleado):
        tarifa_hora = getattr(empleado, "salario_base", 0.0)
        #Esta manda a la otra clase hacer el calculo
        calculador = obtenerNetoXHoras()
        resultado = calculador.calcular_y_guardar(empleado, self.horas_extras, tarifa_hora)
        return resultado

    def obtener_neto_por_contrato(self, empleado):
        #Aqui igual
        deduccion_extra = getattr(empleado, "deduccion_extra", "")
        tipo_deduccion = getattr(empleado, "tipo_deduccion", "")
        calculador = calcularNetoXContrato()
        resultado_contrato = calculador.calcular_y_guardar(empleado, deduccion_extra, tipo_deduccion)
        return resultado_contrato
    
    def calcula_neto_para_empleado(self, empleado):
        if empleado is None:
            raise ValueError("No hay empleado.")
        tipo_contrato_raw = getattr(empleado, "tipo_contrato", "")
        tipo = (tipo_contrato_raw or "").strip().lower()

        #agarra el contrato que tiene el men

        tipoContrato = empleado.tipo_contrato

        #esto seria para la salida
        try:
            if "horas" in tipo or "semanal" in tipo:
                resultado = self.obtener_neto_por_horas_extras(empleado)
            elif "quincenal" in tipo or "contrato" in tipo or "mensual" in tipo:
                resultado = self.obtener_neto_por_contrato(empleado)
            else:
                return {
                    "Id": getattr(empleado, "id", None),
                    "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                    "Bruto": 0.0,
                    "Deducciones": {"total": 0.0},
                    "Otras Deducciones": {"total": 0.0},
                    "Neto": 0.0,
                    "Proceso": False,
                    "Detalle": f"Tipo de contrato no reconocido: '{tipo_contrato_raw}'"
                }
        except Exception as e:
            return {
                "Id": getattr(empleado, "id", None),
                "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "Bruto": 0.0,
                "Deducciones": {"total": 0.0},
                "Otras Deducciones": {"total": 0.0},
                "Neto": 0.0,
                "Proceso": False,
                "Detalle": f"Error al calcular neto: {e}"
            }
    
        resultado.setdefault("Id", getattr(empleado, "id", None))
        resultado.setdefault("Nombre", f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip())
        resultado.setdefault("Bruto", float(resultado.get("Bruto", 0.0)))
        resultado.setdefault("Deducciones", resultado.get("Deducciones", {"total": 0.0}))
        resultado.setdefault("Otras Deducciones", resultado.get("Otras Deducciones", {"total": 0.0}))
        resultado.setdefault("Neto", float(resultado.get("Neto", 0.0)))
        resultado.setdefault("Proceso", bool(resultado.get("Proceso", True)))
        resultado.setdefault("Detalle", resultado.get("Detalle", ""))

        return resultado

 
    def procesar_todos_empleados(self):
        resultados = []
        for empleado in self.empleados:
            res = self.calcula_neto_para_empleado(empleado)
            self.encolar(res)
            resultados.append(res)
        return resultados

        

       