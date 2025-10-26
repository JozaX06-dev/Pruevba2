#Ojo trabajemos con los empleados ya hechos para no estar metiendo esos datos
from Empleado import Empleado
import csv

class ListaEmpleados:
    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def eliminar_empleado(self, empleado):
        if empleado in self.empleados:
            self.empleados.remove(empleado)

    def obtener_empleados(self):
        return self.empleados
    
    def guardar_en_CSV(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
                escritor_csv = csv.writer(archivo)
                escritor_csv.writerow(['id', 'nombre', 'apellido', 'edad', 'telefono', 'correo'])
                
                # 3. Escribir los datos de los empleados
                for empleado in self.empleados:
                    escritor_csv.writerow([empleado.id, 
                                           empleado.nombre, 
                                           empleado.apellido, 
                                           empleado.edad, 
                                           empleado.telefono, 
                                           empleado.correo]) 
            print(f"Empleados guardados exitosamente en {nombre_archivo}.")
        except Exception as e:
            print(f"Error al guardar en CSV: {e}")

    #ya funcionan los dos
    def cargar_empleados_desde_CSV(self, nombre_archivo):
        try:
            self.empleados = []         #(utf-8) es para leer tíldes
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                #salta la fila de encabezado
                next(lector_csv, None) 
                
                for fila in lector_csv:
                    if len(fila) == 6:
                        id_emp, nombre, apellido, edad_str, telefono, correo = fila
                        try:
                            empleado = Empleado(id_emp, nombre, apellido, int(edad_str), telefono, correo)
                            self.agregar_empleado(empleado)
                        except ValueError:
                            print(f"Advertencia: Fila omitida. Edad '{edad_str}' no es un número válido: {fila}")
                    else:
                        print(f"Advertencia: Fila omitida por formato incorrecto (se esperaban 6 columnas): {fila}")
            
            print(f"Empleados cargados exitosamente desde {nombre_archivo}.")

        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no fue encontrado.")
        except Exception as e:
            print(f"Error al cargar desde CSV: {e}")