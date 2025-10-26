import customtkinter as ctk
from tkinter import messagebox
from Cheque import Cheque
from datetime import datetime

class PilaView:
    
    def __init__(self, parent, pila, titulo, label_text, data_manager, empresa, main_window):
        self.parent = parent
        self.pila = pila
        self.titulo = titulo
        self.label_text = label_text
        self.data_manager = data_manager
        self.empresa = empresa
        self.main_window = main_window
    
    def render(self):
        self.create_header()
        
        content_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(header_frame, text=f"Pila: {self.titulo}", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text=f"Visualización de la pila para cálculo de {self.titulo.lower()} (LIFO)", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"✓ Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#d97706"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar a la Pila", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="Seleccionar Empleado:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        
        empleados = self.data_manager.obtener_empleados()
        if empleados:
            opciones_empleados = [f"{emp.get('nombre', '')} {emp.get('apellido', '')} - {emp.get('id', '')}" for emp in empleados]
            empleado_menu = ctk.CTkOptionMenu(left_panel, values=opciones_empleados)
            empleado_menu.pack(pady=(0, 10), padx=20, fill="x")
            
            empleado_actual = self.data_manager.obtener_empleado_seleccionado()
            if empleado_actual:
                texto_actual = f"{empleado_actual.get('nombre', '')} {empleado_actual.get('apellido', '')} - {empleado_actual.get('id', '')}"
                if texto_actual in opciones_empleados:
                    empleado_menu.set(texto_actual)
        else:
            empleado_menu = ctk.CTkOptionMenu(left_panel, values=["No hay empleados"])
            empleado_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text=f"{self.label_text}:").pack(pady=(10, 5), padx=20, anchor="w")
        valor_entry = ctk.CTkEntry(left_panel, placeholder_text=f"Ej: {self.get_placeholder()}")
        valor_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Pila Actual (LIFO):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.stack_display = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b", height=200)
        self.stack_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def push():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = empleado_menu.get()
            valor = valor_entry.get()

            if seleccion and valor and "No hay empleados" not in seleccion:
                try:
                    id_emp = seleccion.split(" - ")[-1]
                    
                    # Buscar empleado en empresa
                    empleado_obj = None
                    for emp in self.empresa.empleados:
                        if emp.id == id_emp:
                            empleado_obj = emp
                            break
                    
                    if empleado_obj:
                        fecha_actual = datetime.now().strftime("%Y-%m-%d")
                        
                        # Determinar si es por horas o por contrato
                        if "Horas" in self.titulo:
                            # Usar calculadora de horas
                            from CalculosPILAS.ObtenerNetoXHoras import obtenerNetoXHoras
                            calculadora = obtenerNetoXHoras()
                            
                            horas = float(valor)
                            tarifa = float(empleado_obj.salario_base)
                            resultado = calculadora.calcular_y_guardar(empleado_obj, horas, tarifa)
                            
                            cheque = Cheque(
                                empleado=empleado_obj,
                                tipo="Pago por Horas",
                                monto=resultado.get("neto", 0.0),
                                fecha_emision=fecha_actual,
                                fecha_cobro=fecha_actual
                            )
                            self.pila.apilar(cheque)
                            
                        else:
                            # Usar calculadora de contrato
                            from CalculosPILAS.CalcularNetoXContrato import calcularNetoXContrato
                            calculadora = calcularNetoXContrato()
                            
                            resultado = calculadora.calcular_y_guardar(empleado_obj, None, None)
                            
                            cheque = Cheque(
                                empleado=empleado_obj,
                                tipo="Pago Contrato",
                                monto=resultado.get("neto", 0.0),
                                fecha_emision=fecha_actual,
                                fecha_cobro=fecha_actual
                            )
                            self.pila.apilar(cheque)
                        
                        self.update_stack_display()
                        self.main_window.guardar_estado_completo()
                        
                        valor_entry.delete(0, 'end')
                        messagebox.showinfo("Éxito", f"Cálculo realizado y agregado (PUSH)\nNeto: ${resultado.get('neto', 0.0):.2f}")
                    else:
                        messagebox.showerror("Error", "No se encontró el empleado")
                        
                except ValueError:
                    messagebox.showerror("Error", "El valor debe ser un número válido")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
        
        def pop():
            if not self.pila.esta_vacia():
                procesado = self.pila.desapilar()
                self.update_stack_display()
                
                self.main_window.guardar_estado_completo()
                
                messagebox.showinfo("Procesado", f"Elemento procesado (POP):\n{procesado.empleado.nombre}\nMonto: ${procesado.monto:.2f}")
            else:
                messagebox.showinfo("Pila Vacía", "No hay elementos en la pila")
        
        def peek():
            if not self.pila.esta_vacia():
                ultimo = self.pila.ver_tope()
                messagebox.showinfo("PEEK", f"Elemento en el tope:\n{ultimo.empleado.nombre}\nMonto: ${ultimo.monto:.2f}")
            else:
                messagebox.showinfo("Pila Vacía", "No hay elementos en la pila")
        
        def clear_stack():
            while not self.pila.esta_vacia():
                self.pila.desapilar()
            self.update_stack_display()
            
            self.main_window.guardar_estado_completo()
            
            messagebox.showinfo("Pila Limpiada", "Todos los elementos fueron removidos")
        
        ctk.CTkButton(left_panel, text="⬆️ PUSH (Agregar al tope)", command=push, fg_color="#d97706", hover_color="#b45309").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="⬇️ POP (Remover del tope)", command=pop, fg_color="#3b8ed0", hover_color="#2d6fa3").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="👁️ PEEK (Ver tope)", command=peek, fg_color="#2fa572", hover_color="#25824f").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Limpiar Pila", command=clear_stack, fg_color="#6b7280", hover_color="#4b5563").pack(pady=5, padx=20, fill="x")
        
        self.update_stack_display()
    
    def get_placeholder(self):
        if "Horas" in self.titulo:
            return "40"
        else:
            return "Automático según contrato"
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Pila (LIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text="LIFO: Last In, First Out\nEl último elemento agregado será el primero en procesarse",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.display_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_display()
    
    def update_stack_display(self):
        for widget in self.stack_display.winfo_children():
            widget.destroy()
        
        if self.pila.esta_vacia():
            ctk.CTkLabel(self.stack_display, text="Pila vacía", text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=10)
        else:
            contenido = self.pila.mostrar_pila()
            for idx, texto in enumerate(contenido[:5]):
                color = "#d97706" if idx == 0 else "gray"
                peso = "bold" if idx == 0 else "normal"
                ctk.CTkLabel(self.stack_display, text=texto, text_color=color, font=ctk.CTkFont(size=10, weight=peso)).pack(anchor="w", padx=5, pady=2)
            
            if len(contenido) > 5:
                ctk.CTkLabel(self.stack_display, text=f"... {len(contenido) - 5} elementos abajo", text_color="gray", font=ctk.CTkFont(size=9)).pack(anchor="w", padx=5, pady=2)
        if hasattr(self, 'display_frame'):
            self.update_display()
    
    def update_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if self.pila.esta_vacia():
            ctk.CTkLabel(self.display_frame, text="Pila vacía\n\nAgrega elementos para comenzar", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            contenido = self.pila.mostrar_pila()
            for idx, texto in enumerate(contenido):
                item_frame = ctk.CTkFrame(self.display_frame, fg_color="#1a1a1a", border_width=2, border_color="#d97706" if idx == 0 else "#3b3b3b")
                item_frame.pack(fill="x", pady=8, padx=5)
                
                position_text = "🔝 TOPE DE LA PILA" if idx == 0 else f"Posición #{self.pila.tamaño() - idx}"
                position_color = "#d97706" if idx == 0 else "gray"
                
                header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                
                ctk.CTkLabel(header_frame, text=position_text, text_color=position_color, font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
                
                ctk.CTkLabel(item_frame, text=texto, text_color="lightgray", justify="left", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=15, pady=(5, 15))