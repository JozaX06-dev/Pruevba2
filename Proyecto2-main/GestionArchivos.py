import csv
import os
from collections import deque

class GestionArchivos:
    Empleados_csv = 'empleados.csv'
    Cola_Cheques_csv = 'cola_cheques.csv'
    Pila_Horas_csv = 'pila_horas.csv'
    Pila_Contratos_csv = 'pila_contratos.csv'
    Diccionario_csv = 'diccionario_calculos.csv'
    Lista_Impresion_csv = 'lista_impresion.csv'
    
    @staticmethod
    def guardar_lista(objetos, path: str):
        if not objetos:
            return
        
        if isinstance(objetos[0], dict):
            fieldnames = list(objetos[0].keys())
            with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for obj in objetos:
                    writer.writerow(obj)
        else:
            fieldnames = list(objetos[0].to_dict().keys())
            with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for obj in objetos:
                    writer.writerow(obj.to_dict())
    
    @staticmethod
    def cargar_lista(cls, path: str):
        objetos = []
        try:
            with open(path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if cls is None:
                        objetos.append(dict(row))
                    else:
                        objetos.append(cls.from_dict(row))
        except FileNotFoundError:
            pass
        return objetos
    
    @staticmethod
    def guardar_empleados(empleados):
        GestionArchivos.guardar_lista(empleados, GestionArchivos.Empleados_csv)
    
    @staticmethod
    def cargar_empleados():
        return GestionArchivos.cargar_lista(None, GestionArchivos.Empleados_csv)
    
    @staticmethod
    def guardar_cola_cheques(cola_cheques):
        if isinstance(cola_cheques, deque):
            lista = list(cola_cheques)
        else:
            lista = cola_cheques
        GestionArchivos.guardar_lista(lista, GestionArchivos.Cola_Cheques_csv)
    
    @staticmethod
    def cargar_cola_cheques():
        lista = GestionArchivos.cargar_lista(None, GestionArchivos.Cola_Cheques_csv)
        return deque(lista)
    
    @staticmethod
    def guardar_pila_horas(pila_horas):
        GestionArchivos.guardar_lista(pila_horas, GestionArchivos.Pila_Horas_csv)
    
    @staticmethod
    def cargar_pila_horas():
        return GestionArchivos.cargar_lista(None, GestionArchivos.Pila_Horas_csv)
    
    @staticmethod
    def guardar_pila_contratos(pila_contratos):
        GestionArchivos.guardar_lista(pila_contratos, GestionArchivos.Pila_Contratos_csv)
    
    @staticmethod
    def cargar_pila_contratos():
        return GestionArchivos.cargar_lista(None, GestionArchivos.Pila_Contratos_csv)
    
    @staticmethod
    def guardar_diccionario(diccionario):
        datos = []
        for key, valores in diccionario.items():
            if isinstance(valores, dict):
                for subkey, subvalor in valores.items():
                    datos.append({
                        'empleado_id': key,
                        'tipo_calculo': subkey,
                        'valor': subvalor
                    })
            else:
                datos.append({
                    'empleado_id': key,
                    'tipo_calculo': 'valor',
                    'valor': valores
                })
        GestionArchivos.guardar_lista(datos, GestionArchivos.Diccionario_csv)
    
    @staticmethod
    def cargar_diccionario():
        datos = GestionArchivos.cargar_lista(None, GestionArchivos.Diccionario_csv)
        diccionario = {}
        for item in datos:
            key = item.get('empleado_id')
            tipo = item.get('tipo_calculo')
            valor = item.get('valor')
            
            if key not in diccionario:
                diccionario[key] = {}
            diccionario[key][tipo] = valor
        return diccionario
    
    @staticmethod
    def guardar_lista_impresion(lista_impresion):
        datos = []
        for item in lista_impresion:
            if isinstance(item, tuple):
                datos.append({
                    'empleado_id': item[0],
                    'nombre': item[1],
                    'monto': item[2],
                    'concepto': item[3],
                    'fecha': item[4]
                })
            elif isinstance(item, dict):
                datos.append(item)
        GestionArchivos.guardar_lista(datos, GestionArchivos.Lista_Impresion_csv)
    
    @staticmethod
    def cargar_lista_impresion():
        datos = GestionArchivos.cargar_lista(None, GestionArchivos.Lista_Impresion_csv)
        lista = []
        for item in datos:
            tupla = (
                item.get('empleado_id', ''),
                item.get('nombre', ''),
                item.get('monto', '0.0'),
                item.get('concepto', ''),
                item.get('fecha', '')
            )
            lista.append(tupla)
        return lista
    
    @staticmethod
    def guardar_todos_los_datos(cola_cheques, pila_horas, pila_contratos, diccionario, lista_impresion):
        GestionArchivos.guardar_cola_cheques(cola_cheques)
        GestionArchivos.guardar_pila_horas(pila_horas)
        GestionArchivos.guardar_pila_contratos(pila_contratos)
        GestionArchivos.guardar_diccionario(diccionario)
        GestionArchivos.guardar_lista_impresion(lista_impresion)
    
    @staticmethod
    def cargar_todos_los_datos():
        cola_cheques = GestionArchivos.cargar_cola_cheques()
        pila_horas = GestionArchivos.cargar_pila_horas()
        pila_contratos = GestionArchivos.cargar_pila_contratos()
        diccionario = GestionArchivos.cargar_diccionario()
        lista_impresion = GestionArchivos.cargar_lista_impresion()
        return cola_cheques, pila_horas, pila_contratos, diccionario, lista_impresion
    
    @staticmethod
    def existe_archivo(path: str):
        return os.path.exists(path)
    
    @staticmethod
    def limpiar_archivo(path: str):
        if GestionArchivos.existe_archivo(path):
            os.remove(path)