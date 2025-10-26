import csv
import os
from Ordenamiento import merge_sort
from Busqueda_binaria import binary_search

class DataManager:
    """Gestiona la carga y manipulación de datos de empleados"""
    
    def __init__(self):
        self.empleados = []
        self.empleados_ordenados = []
        self.csv_path = None
        self.empleado_seleccionado = None
    
    def cargar_csv(self, archivo):
        """Carga empleados desde un archivo CSV"""
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                self.empleados = list(csv_reader)
                self.csv_path = archivo
            return True, f"Se cargaron {len(self.empleados)} empleados correctamente"
        except Exception as e:
            return False, f"Error al cargar el archivo: {str(e)}"
    
    def guardar_csv(self):
        """Guarda los cambios en el archivo CSV"""
        if not self.csv_path:
            return False, "No hay archivo CSV cargado"
        
        try:
            empleados_a_guardar = self.empleados_ordenados if self.empleados_ordenados else self.empleados
            
            if not empleados_a_guardar:
                return False, "No hay empleados para guardar"
            
            with open(self.csv_path, 'w', encoding='utf-8', newline='') as file:
                fieldnames = empleados_a_guardar[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(empleados_a_guardar)
            
            return True, "Cambios guardados correctamente en CSV"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"
    
    def agregar_empleado(self, empleado_dict):
        """Agrega un nuevo empleado"""
        self.empleados.append(empleado_dict)
        if self.empleados_ordenados:
            self.empleados_ordenados.append(empleado_dict)
        return True, "Empleado agregado correctamente"
    
    def actualizar_empleado(self, id_empleado, datos_actualizados):
        """Actualiza los datos de un empleado existente"""
        for emp in self.empleados:
            if emp.get('id') == id_empleado:
                emp.update(datos_actualizados)
                break
        
        for emp in self.empleados_ordenados:
            if emp.get('id') == id_empleado:
                emp.update(datos_actualizados)
                break
        
        return True, "Empleado actualizado correctamente"
    
    def eliminar_empleado(self, id_empleado):
        """Elimina un empleado por ID"""
        self.empleados = [emp for emp in self.empleados if emp.get('id') != id_empleado]
        self.empleados_ordenados = [emp for emp in self.empleados_ordenados if emp.get('id') != id_empleado]
        return True, "Empleado eliminado correctamente"
    
    def ordenar_por_campo(self, campo):
        """Ordena empleados por un campo específico usando Merge Sort"""
        if not self.empleados:
            return False, "No hay empleados cargados"
        
        try:
            # Ordenar considerando mayúsculas/minúsculas
            self.empleados_ordenados = merge_sort(self.empleados, key=lambda emp: str(emp.get(campo, '')).lower())
            return True, f"Empleados ordenados por {campo} usando Merge Sort O(n log n)"
        except Exception as e:
            return False, f"Error al ordenar: {str(e)}"
    
    def buscar_por_nombre(self, valor_busqueda):
        """Busca un empleado por nombre usando Binary Search (case-insensitive)"""
        if not self.empleados_ordenados:
            return None, "Primero ordena los empleados por nombre"
        
        valor_busqueda = valor_busqueda.strip().lower()
        if not valor_busqueda:
            return None, "Ingresa un valor para buscar"
        
        # Crear lista de nombres en minúsculas para la búsqueda
        nombres_lower = [emp.get('nombre', '').lower() for emp in self.empleados_ordenados]
        
        # Buscar usando binary search
        indice = binary_search(nombres_lower, valor_busqueda)
        
        if indice != -1:
            empleado_encontrado = self.empleados_ordenados[indice]
            # Mensaje con el nombre original (con mayúsculas correctas)
            nombre_original = empleado_encontrado.get('nombre', '')
            return empleado_encontrado, None
        else:
            # Intentar búsqueda parcial (por si escribió solo parte del nombre)
            for idx, nombre_lower in enumerate(nombres_lower):
                if valor_busqueda in nombre_lower:
                    empleado_encontrado = self.empleados_ordenados[idx]
                    return empleado_encontrado, None
            
            # Si no se encuentra ni exacto ni parcial
            return None, f"No se encontró empleado con nombre: {valor_busqueda.title()}"
    
    def buscar_por_id(self, id_empleado):
        """Busca un empleado por ID (case-insensitive)"""
        empleados_list = self.empleados_ordenados if self.empleados_ordenados else self.empleados
        
        # Normalizar el ID de búsqueda
        id_busqueda = str(id_empleado).strip().upper()
        
        for emp in empleados_list:
            id_emp = str(emp.get('id', '')).strip().upper()
            if id_emp == id_busqueda:
                return emp, None
        
        return None, f"No se encontró empleado con ID: {id_empleado}"
    
    def seleccionar_empleado(self, empleado):
        """Selecciona un empleado para trabajar con él"""
        self.empleado_seleccionado = empleado
        return True
    
    def obtener_empleado_seleccionado(self):
        """Retorna el empleado actualmente seleccionado"""
        return self.empleado_seleccionado
    
    def obtener_empleados(self):
        """Retorna los empleados ordenados si existen, sino los originales"""
        return self.empleados_ordenados if self.empleados_ordenados else self.empleados
    
    def obtener_cantidad_empleados(self):
        """Retorna la cantidad total de empleados"""
        return len(self.empleados)
    
    def obtener_lista_ids(self):
        """Retorna una lista de todos los IDs de empleados"""
        empleados_list = self.empleados_ordenados if self.empleados_ordenados else self.empleados
        return [emp.get('id', '') for emp in empleados_list]
    
    def obtener_lista_nombres(self):
        """Retorna una lista de todos los nombres completos de empleados"""
        empleados_list = self.empleados_ordenados if self.empleados_ordenados else self.empleados
        return [f"{emp.get('nombre', '')} {emp.get('apellido', '')}" for emp in empleados_list]