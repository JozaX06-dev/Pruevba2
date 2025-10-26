#La clase que recibe todo los datos de chequeo y empleados
from CalculoConCOLAS.CalculaNetoEmpleado import calculaNetoEmpleado
from ListaEmpleados import ListaEmpleados

TIPO_CHEQUE = {
        #Esto simplemente suma si el usuario escoge estos tipos de cheque
        "Pago de salario": 0,
        "Caja chica": 20000,
        "Otros Gastos": 15000
    }
class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

   
    #aqui hay que cargar TODOS los .csv

    def obtener_empleado(self, id):
        for empleado in self.empleados:
            if empleado.id == id:
                return empleado
        return None

    def guardar_registros_CSV(self, archivo):
        print("guardar")

    #Para el cheque
    def normalizar_tipo_cheque(self, tipo_cheque):
        if tipo_cheque is None:
            return ""
        return str(tipo_cheque).strip().lower()


    # salario con reducciones (procesa todos los empleados)
    def calcular_neto_empleados(self, horas_extras, tipo_cheque):
        if not isinstance(horas_extras, (int, float)) or horas_extras < 0:
            raise ValueError("horas_extras debe ser numérico no negativo.")
        if not isinstance(self.empleados, list):
            raise TypeError("self.empleados debe ser una lista de empleados.")
        

        tipo = self.normalizar_tipo_cheque(tipo_cheque)
        ajuste = TIPO_CHEQUE.get(tipo, 0.0)
        calculador = calculaNetoEmpleado(list(self.empleados), horas_extras, tipo)

        resultados = []
        for empleado in list(self.empleados):
            if getattr(empleado, "id", None) is None:
                res = {"Id": None, "Nombre": "", "Bruto": 0.0, "Deducciones": {"total": 0.0},
                       "Otras_Deducciones": {"total": 0.0}, "Neto": 0.0, "Proceso": False,
                       "Detalle": "Empleado sin id."}
                calculador.encolar(res)
                resultados.append(res)
                continue

            res = calculador.calcula_neto_para_empleado(empleado)

            # aplicar ajuste por tipo de cheque
            if ajuste:
                res["Neto"] = round(float(res.get("Neto", 0.0)) + ajuste, 2)
                res["Detalle"] = (res.get("Detalle", "") + f"; ajuste {tipo} +{int(ajuste)}").lstrip("; ")

            # asegurar campos mínimos y consistencia de claves (minúsculas)
            res.setdefault("Id", getattr(empleado, "id", None))
            res.setdefault("Nombre", f"{getattr(empleado,'nombre','')} {getattr(empleado,'apellido','')}".strip())
            res.setdefault("Bruto", float(res.get("Bruto", 0.0)))
            res.setdefault("Deducciones", res.get("Deducciones", {"total": 0.0}))
            res.setdefault("Otras_Deducciones", res.get("Otras_Deducciones", {"total": 0.0}))
            res.setdefault("Neto", round(float(res.get("Neto", 0.0)), 2))
            res.setdefault("Proceso", bool(res.get("Proceso", True)))
            res.setdefault("Detalle", res.get("Detalle", ""))

            calculador.encolar(res)
            resultados.append(res)

        return resultados

    # procesa cheque para un solo empleado
    def procesa_cheque(self, empleado_id, horas_extras, tipo_cheque):
        if not isinstance(horas_extras, (int, float)) or horas_extras < 0:
            raise ValueError("horas_extras debe ser numérico no negativo.")

        empleado = self.obtener_empleado(empleado_id)
        if empleado is None:
            return {"success": False, "detalle": f"Empleado con ID {empleado_id} no encontrado."}

        tipo = self.normalizar_tipo_cheque(tipo_cheque)
        ajuste = TIPO_CHEQUE.get(tipo, 0.0)

        calculador = calculaNetoEmpleado([empleado], horas_extras, tipo)
        res = calculador.calcula_neto_para_empleado(empleado)

        if ajuste:
            res["neto"] = round(float(res.get("neto", 0.0)) + ajuste, 2)
            res["detalle"] = (res.get("detalle", "") + f"; ajuste {tipo} +{int(ajuste)}").lstrip("; ")

        calculador.encolar(res)
        return res