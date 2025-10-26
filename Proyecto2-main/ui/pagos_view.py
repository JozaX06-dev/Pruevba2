import customtkinter as ctk
from tkinter import messagebox

class PagosView:
    """Vista para el Procesamiento de Pagos"""
    
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        self.empleados_seleccionados = []
    
    def render(self):
        self.create_header()
        
        content_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        self.create_filter_panel(content_frame)
        self.create_content_panel(content_frame)
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(header_frame, text="Procesamiento de Pagos", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text="Gestión y procesamiento de pagos de nómina", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
    
    def create_filter_panel(self, parent):
        filter_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        filter_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        ctk.CTkLabel(filter_frame, text="Filtrar por:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=20, sticky="w")
        
        self.tipo_pago_var = ctk.StringVar(value="Todos")
        tipo_menu = ctk.CTkOptionMenu(
            filter_frame, 
            values=["Todos", "Semanal", "Quincenal", "Mensual"],
            variable=self.tipo_pago_var,
            command=lambda x: self.actualizar_lista()
        )
        tipo_menu.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        # Botón para seleccionar todos
        ctk.CTkButton(
            filter_frame,
            text="✓ Seleccionar Todos",
            command=self.seleccionar_todos,
            fg_color="#2fa572",
            hover_color="#25824f",
            width=120
        ).grid(row=0, column=3, padx=10, pady=20)
        
        ctk.CTkButton(
            filter_frame,
            text="💵 Procesar Seleccionados",
            command=self.procesar_pagos,
            fg_color="#3b8ed0",
            hover_color="#2d6fa3",
            width=150
        ).grid(row=0, column=4, padx=10, pady=20)
    
    def create_content_panel(self, parent):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo - Lista de empleados
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Empleados Disponibles", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.empleados_frame = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b")
        self.empleados_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Panel derecho - Resumen
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Resumen de Pagos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.resumen_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b")
        self.resumen_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de empleados"""
        # Limpiar frame
        for widget in self.empleados_frame.winfo_children():
            widget.destroy()
        
        empleados = self.data_manager.obtener_empleados()
        
        if not empleados:
            ctk.CTkLabel(
                self.empleados_frame, 
                text="No hay empleados cargados\n\nCarga un archivo CSV primero",
                text_color="gray",
                font=ctk.CTkFont(size=14)
            ).pack(pady=40)
            self.actualizar_resumen()
            return
        
        # Mostrar empleados
        for empleado in empleados:
            emp_id = empleado.get('id', '')
            nombre = empleado.get('nombre', '')
            apellido = empleado.get('apellido', '')
            # Simular un salario (puedes obtenerlo del CSV si existe)
            salario = empleado.get('salario', '2500.00')
            
            emp_frame = ctk.CTkFrame(self.empleados_frame, fg_color="#1a1a1a")
            emp_frame.pack(fill="x", pady=8, padx=5)
            
            # Checkbox para selección
            var = ctk.BooleanVar(value=emp_id in self.empleados_seleccionados)
            
            def toggle_selection(emp_id=emp_id, var=var):
                if var.get():
                    if emp_id not in self.empleados_seleccionados:
                        self.empleados_seleccionados.append(emp_id)
                else:
                    if emp_id in self.empleados_seleccionados:
                        self.empleados_seleccionados.remove(emp_id)
                self.actualizar_resumen()
            
            checkbox = ctk.CTkCheckBox(
                emp_frame,
                text="",
                variable=var,
                command=toggle_selection,
                width=30
            )
            checkbox.pack(side="left", padx=10, pady=10)
            
            # Información del empleado
            info_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            nombre_completo = f"{nombre} {apellido} ({emp_id})"
            ctk.CTkLabel(info_frame, text=nombre_completo, font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"Salario: ${float(salario):,.2f}", text_color="gray", anchor="w").pack(fill="x")
        
        self.actualizar_resumen()
    
    def actualizar_resumen(self):
        """Actualiza el resumen de pagos"""
        # Limpiar frame
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
        
        empleados = self.data_manager.obtener_empleados()
        
        # Calcular totales
        cantidad_seleccionados = len(self.empleados_seleccionados)
        total_a_pagar = 0.0
        
        for emp_id in self.empleados_seleccionados:
            empleado, _ = self.data_manager.buscar_por_id(emp_id)
            if empleado:
                salario = float(empleado.get('salario', '2500.00'))
                total_a_pagar += salario
        
        # Mostrar estadísticas
        stats_data = [
            ("Empleados Seleccionados", str(cantidad_seleccionados), "#3b8ed0"),
            ("Total a Pagar", f"${total_a_pagar:,.2f}", "#2fa572"),
            ("Total Empleados", str(len(empleados) if empleados else 0), "gray")
        ]
        
        for label, value, color in stats_data:
            stat_frame = ctk.CTkFrame(self.resumen_frame, fg_color="#1a1a1a")
            stat_frame.pack(fill="x", pady=10, padx=10)
            
            ctk.CTkLabel(stat_frame, text=label, text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=(15, 2), padx=15, anchor="w")
            ctk.CTkLabel(stat_frame, text=value, text_color=color, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(2, 15), padx=15, anchor="w")
        
        # Lista de seleccionados
        if self.empleados_seleccionados:
            ctk.CTkLabel(
                self.resumen_frame,
                text="Empleados a Procesar:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="lightgray"
            ).pack(pady=(20, 10), padx=10, anchor="w")
            
            lista_frame = ctk.CTkScrollableFrame(self.resumen_frame, fg_color="#1a1a1a", height=200)
            lista_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            for emp_id in self.empleados_seleccionados:
                empleado, _ = self.data_manager.buscar_por_id(emp_id)
                if empleado:
                    nombre = f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}"
                    salario = float(empleado.get('salario', '2500.00'))
                    
                    item_text = f"• {nombre}: ${salario:,.2f}"
                    ctk.CTkLabel(lista_frame, text=item_text, text_color="lightgray", anchor="w", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=3)
    
    def seleccionar_todos(self):
        """Selecciona todos los empleados"""
        empleados = self.data_manager.obtener_empleados()
        self.empleados_seleccionados = [emp.get('id', '') for emp in empleados]
        self.actualizar_lista()
        messagebox.showinfo("Selección", f"Se seleccionaron {len(self.empleados_seleccionados)} empleados")
    
    def procesar_pagos(self):
        """Procesa los pagos de los empleados seleccionados"""
        if not self.empleados_seleccionados:
            messagebox.showwarning("Advertencia", "No hay empleados seleccionados para procesar")
            return
        
        cantidad = len(self.empleados_seleccionados)
        total = 0.0
        
        detalles = "Empleados procesados:\n\n"
        for emp_id in self.empleados_seleccionados:
            empleado, _ = self.data_manager.buscar_por_id(emp_id)
            if empleado:
                nombre = f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}"
                salario = float(empleado.get('salario', '2500.00'))
                total += salario
                detalles += f"• {nombre}: ${salario:,.2f}\n"
        
        detalles += f"\n━━━━━━━━━━━━━━━\nTotal: ${total:,.2f}"
        
        respuesta = messagebox.askyesno(
            "Confirmar Procesamiento",
            f"¿Procesar pagos para {cantidad} empleados?\n\nTotal: ${total:,.2f}"
        )
        
        if respuesta:
            messagebox.showinfo(
                "Pagos Procesados",
                f"✓ Se procesaron {cantidad} pagos exitosamente\n\n{detalles}"
            )
            # Limpiar selección
            self.empleados_seleccionados.clear()
            self.actualizar_lista()