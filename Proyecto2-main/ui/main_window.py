import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from core.data_manager import DataManager
from ui.dashboard_view import DashboardView
from ui.empleados_view import EmpleadosView
from ui.cola_view import ColaView
from ui.pila_view import PilaView
from ui.diccionario_view import DiccionarioView
from ui.lista_view import ListaView
from ui.pagos_view import PagosView
from GestionArchivos import GestionArchivos

# Importar clases reales
from Cola_cheques import ColaCheques
from Pila_horas import Pila_Horas
from Pila_contrato import Pila_Contrato
from Empresa import Empresa
from Empleado import Empleado

class PayrollSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Nómina - Visualización de Estructuras de Datos")
        self.geometry("1400x850")
        
        self.data_manager = DataManager()
        
        # Usar clases reales en lugar de listas simples
        self.cola_cheques = ColaCheques()
        self.pila_horas = Pila_Horas()
        self.pila_contratos = Pila_Contrato()
        self.diccionario_calculos = {}
        self.lista_impresion = []
        self.empresa = Empresa("Mi Empresa")
        
        self.auto_load_csv()
        self.cargar_estado_completo()
        
        self.create_layout()
    
    def guardar_estado_completo(self):
        try:
            # Convertir estructuras reales a formato serializable
            cola_lista = list(self.cola_cheques.cola)
            pila_horas_lista = self.pila_horas.pila.copy()
            pila_contratos_lista = self.pila_contratos.pila.copy()
            
            GestionArchivos.guardar_todos_los_datos(
                cola_lista,
                pila_horas_lista,
                pila_contratos_lista,
                self.diccionario_calculos,
                self.lista_impresion
            )
        except Exception as e:
            print(f"Error al guardar estado: {e}")
    
    def cargar_estado_completo(self):
        try:
            if GestionArchivos.existe_archivo(GestionArchivos.Cola_Cheques_csv):
                cola, pila_h, pila_c, dicc, lista = GestionArchivos.cargar_todos_los_datos()
                
                # Restaurar en estructuras reales
                self.cola_cheques = ColaCheques()
                for item in cola:
                    self.cola_cheques.encolar(item)
                
                self.pila_horas.pila = pila_h
                self.pila_contratos.pila = pila_c
                self.diccionario_calculos = dicc
                self.lista_impresion = lista
                print("Datos cargados correctamente")
            else:
                print("No hay datos previos, iniciando con estructuras vacías")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def auto_load_csv(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        
        posibles_archivos = [
            os.path.join(directorio_actual, 'empleados.csv'),
            'empleados.csv',
            os.path.join(directorio_actual, '..', 'empleados.csv'),
            'data/empleados.csv',
            'datos/empleados.csv',
            'ui/empleados.csv',
        ]
        
        print(f"Buscando CSV en directorio: {directorio_actual}")
        
        for archivo in posibles_archivos:
            archivo_normalizado = os.path.normpath(archivo)
            print(f"Intentando: {archivo_normalizado}")
            
            if os.path.exists(archivo_normalizado):
                exito, mensaje = self.data_manager.cargar_csv(archivo_normalizado)
                if exito:
                    # Cargar empleados en la empresa también
                    self.cargar_empleados_en_empresa()
                    print(f"{mensaje}")
                    print(f"CSV cargado desde: {archivo_normalizado}")
                    return
        
        print("No se encontró archivo CSV para cargar automáticamente")
    
    def cargar_empleados_en_empresa(self):
        """Carga empleados del DataManager a la clase Empresa"""
        empleados_data = self.data_manager.obtener_empleados()
        self.empresa.empleados = []
        
        for emp_dict in empleados_data:
            empleado = Empleado(
                id=emp_dict.get('id', ''),
                nombre=emp_dict.get('nombre', ''),
                apellido=emp_dict.get('apellido', ''),
                departamento=emp_dict.get('departamento', ''),
                puesto=emp_dict.get('puesto', ''),
                salario_base=float(emp_dict.get('salario', 0.0)),
                tipo_contrato=emp_dict.get('tipo_pago', 'Quincenal')
            )
            self.empresa.empleados.append(empleado)
    
    def create_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.show_dashboard()
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        logo_label = ctk.CTkLabel(
            sidebar, 
            text="💼 Sistema de Nómina", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#3b8ed0"
        )
        logo_label.pack(pady=30, padx=20)
        
        self.load_csv_btn = ctk.CTkButton(
            sidebar,
            text="Cargar CSV",
            command=self.load_csv,
            fg_color="#2b2b2b",
            hover_color="#3b3b3b",
            height=35
        )
        self.load_csv_btn.pack(pady=10, padx=20, fill="x")
        
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#3b3b3b")
        separator.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(
            sidebar,
            text="NAVEGACIÓN",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray"
        ).pack(pady=(0, 10), padx=20, anchor="w")
        
        nav_buttons = [
            ("Dashboard", self.show_dashboard, "#3b8ed0"),
            ("Empleados", self.show_empleados, "#2fa572"),
            ("Cola: Calcular Neto", self.show_cola_neto, "#2fa572"),
            ("Pila: Neto por Horas", self.show_pila_horas, "#d97706"),
            ("Pila: Neto Contrato", self.show_pila_contratos, "#d97706"),
            ("Diccionario: Cálculos", self.show_diccionario, "#dc2626"),
            ("Lista: Imprimir Cheques", self.show_lista_cheques, "#2fa572"),
            ("Procesar Pagos", self.show_procesar_pagos, "#6b7280")
        ]
        
        for text, command, color in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color="#2b2b2b",
                anchor="w",
                height=40,
                text_color=color
            )
            btn.pack(pady=5, padx=20, fill="x")
        
        separator2 = ctk.CTkFrame(sidebar, height=2, fg_color="#3b3b3b")
        separator2.pack(side="bottom", pady=20, padx=20, fill="x")
        
        info_label = ctk.CTkLabel(
            sidebar,
            text="v1.0 | Estructuras de Datos",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        info_label.pack(side="bottom", pady=10)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def load_csv(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            exito, mensaje = self.data_manager.cargar_csv(filename)
            if exito:
                self.cargar_empleados_en_empresa()
                messagebox.showinfo("Éxito", mensaje)
                self.show_dashboard()
            else:
                messagebox.showerror("Error", mensaje)
    
    def show_dashboard(self):
        self.clear_main_frame()
        view = DashboardView(
            self.main_frame, 
            self.data_manager, 
            self.cola_cheques.tamaño(),
            self.pila_horas.tamaño(), 
            len(self.diccionario_calculos)
        )
        view.render()
    
    def show_empleados(self):
        self.clear_main_frame()
        view = EmpleadosView(self.main_frame, self.data_manager)
        view.render()
    
    def show_cola_neto(self):
        self.clear_main_frame()
        view = ColaView(self.main_frame, self.cola_cheques, self.data_manager, self.empresa, self)
        view.render()
    
    def show_pila_horas(self):
        self.clear_main_frame()
        view = PilaView(
            self.main_frame, 
            self.pila_horas, 
            "Neto por Horas", 
            "Horas trabajadas",
            self.data_manager,
            self.empresa,
            self
        )
        view.render()
    
    def show_pila_contratos(self):
        self.clear_main_frame()
        view = PilaView(
            self.main_frame, 
            self.pila_contratos, 
            "Neto Contrato", 
            "Valor del contrato",
            self.data_manager,
            self.empresa,
            self
        )
        view.render()
    
    def show_diccionario(self):
        self.clear_main_frame()
        view = DiccionarioView(self.main_frame, self.diccionario_calculos, self.data_manager, self)
        view.render()
    
    def show_lista_cheques(self):
        self.clear_main_frame()
        view = ListaView(self.main_frame, self.lista_impresion, self.data_manager, self)
        view.render()
    
    def show_procesar_pagos(self):
        self.clear_main_frame()
        view = PagosView(self.main_frame, self.data_manager)
        view.render()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = PayrollSystem()
    app.mainloop()