import customtkinter as ctk
from tkinter import messagebox

class EmpleadosView:
    """Vista para la gestión de empleados con Merge Sort y Binary Search"""
    
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        self.empleado_seleccionado = None
    
    def render(self):
        """Renderiza la vista de empleados"""
        self.create_header()
        self.create_search_and_sort_controls()
        self.create_table()
    
    def create_header(self):
        """Crea el encabezado de la vista"""
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Gestión de Empleados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(anchor="w")
        
        # Mostrar empleado seleccionado
        empleado_actual = self.data_manager.obtener_empleado_seleccionado()
        if empleado_actual:
            texto_seleccion = f"✓ Empleado Seleccionado: {empleado_actual.get('nombre', '')} {empleado_actual.get('apellido', '')} (ID: {empleado_actual.get('id', '')})"
            color = "#2fa572"
        else:
            texto_seleccion = "⚠ No hay empleado seleccionado - Haz clic en 'Seleccionar' para elegir uno"
            color = "gray"
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=texto_seleccion,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
    
    def create_search_and_sort_controls(self):
        """Crea los controles de búsqueda y ordenamiento"""
        # Frame de búsqueda
        search_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=20)
        search_frame.grid_columnconfigure(1, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar empleado (Nombre/Apellido/ID)...",
            height=40
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Buscar (Binary Search)",
            command=self.buscar,
            width=200,
            fg_color="#3b8ed0",
            hover_color="#2d6fa3",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=1, padx=5)
        
        # Frame de botones de ordenamiento
        sort_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        sort_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        sort_frame.grid_columnconfigure(5, weight=1)
        
        ctk.CTkLabel(sort_frame, text="Ordenar por:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=(0, 10)
        )
        
        sort_buttons = [
            ("Nombre", 'nombre'),
            ("Apellido", 'apellido'),
            ("ID", 'id')
        ]
        
        for i, (text, campo) in enumerate(sort_buttons):
            ctk.CTkButton(
                sort_frame,
                text=text,
                command=lambda c=campo: self.ordenar(c),
                width=100,
                fg_color="#2fa572",
                hover_color="#25824f",
                font=ctk.CTkFont(size=12)
            ).grid(row=0, column=i+1, padx=5)
        
        ctk.CTkButton(
            sort_frame,
            text="💾 Guardar CSV",
            command=self.guardar_csv,
            width=120,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=4, padx=5, sticky="e")
    
    def create_table(self):
        """Crea la tabla de empleados"""
        table_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        table_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        scrollable = ctk.CTkScrollableFrame(table_frame, fg_color="#2b2b2b")
        scrollable.grid(row=0, column=0, sticky="nsew")
        
        empleados = self.data_manager.obtener_empleados()
        
        if empleados:
            # Crear encabezados
            headers = list(empleados[0].keys()) + ["ACCIONES"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    scrollable,
                    text=header.upper(),
                    font=ctk.CTkFont(weight="bold"),
                    fg_color="#1a1a1a",
                    corner_radius=5
                )
                label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            # Crear filas de empleados
            empleado_actual = self.data_manager.obtener_empleado_seleccionado()
            id_seleccionado = empleado_actual.get('id') if empleado_actual else None
            
            for row_idx, empleado in enumerate(empleados, 1):
                es_seleccionado = empleado.get('id') == id_seleccionado
                bg_color = "#2d5016" if es_seleccionado else ("#2b2b2b" if row_idx % 2 == 0 else "#1a1a1a")
                
                # Mostrar datos del empleado
                for col_idx, value in enumerate(empleado.values()):
                    label = ctk.CTkLabel(
                        scrollable,
                        text=str(value),
                        fg_color=bg_color,
                        text_color="#2fa572" if es_seleccionado else "white"
                    )
                    label.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                
                # Botón de selección/deselección
                if es_seleccionado:
                    btn_text = "✓ SELECCIONADO (Click para deseleccionar)"
                    btn_color = "#2fa572"
                    btn_hover = "#25824f"
                else:
                    btn_text = "Seleccionar"
                    btn_color = "#3b8ed0"
                    btn_hover = "#2d6fa3"
                
                select_btn = ctk.CTkButton(
                    scrollable,
                    text=btn_text,
                    command=lambda emp=empleado, sel=es_seleccionado: self.toggle_seleccion(emp, sel),
                    width=250 if es_seleccionado else 120,
                    height=30,
                    fg_color=btn_color,
                    hover_color=btn_hover,
                    font=ctk.CTkFont(size=11, weight="bold" if es_seleccionado else "normal")
                )
                select_btn.grid(row=row_idx, column=len(headers)-1, padx=5, pady=5)
        else:
            no_data = ctk.CTkLabel(
                scrollable,
                text="No hay empleados cargados. Por favor, carga un archivo CSV.",
                text_color="gray"
            )
            no_data.pack(pady=50)
    
    def toggle_seleccion(self, empleado, esta_seleccionado):
        """Selecciona o deselecciona un empleado según su estado actual"""
        if esta_seleccionado:
            # Deseleccionar
            self.data_manager.seleccionar_empleado(None)
            messagebox.showinfo(
                "Empleado Deseleccionado", 
                f"Se ha deseleccionado a:\n\n{empleado.get('nombre', '')} {empleado.get('apellido', '')}\n\nAhora puedes seleccionar otro empleado o trabajar sin selección."
            )
        else:
            # Seleccionar
            self.data_manager.seleccionar_empleado(empleado)
            messagebox.showinfo(
                "Empleado Seleccionado", 
                f"Has seleccionado a:\n\n{empleado.get('nombre', '')} {empleado.get('apellido', '')}\nID: {empleado.get('id', '')}\n\nAhora puedes usar este empleado en Cola, Pila, Lista y Diccionario.\n\nPara deseleccionar, haz clic nuevamente en el botón."
            )
        
        self.render()  # Refrescar vista
    
    def ordenar(self, campo):
        """Ordena empleados por el campo especificado usando Merge Sort"""
        exito, mensaje = self.data_manager.ordenar_por_campo(campo)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.render()
        else:
            messagebox.showwarning("Advertencia", mensaje)
    
    def buscar(self):
        """Busca un empleado usando Binary Search"""
        valor_busqueda = self.search_entry.get()
        empleado, error = self.data_manager.buscar_por_nombre(valor_busqueda)
        
        if error:
            messagebox.showwarning("Advertencia", error)
        else:
            resultado = f"Empleado encontrado:\n\n"
            for key, value in empleado.items():
                resultado += f"{key.upper()}: {value}\n"
            messagebox.showinfo("Resultado de Búsqueda", resultado)
    
    def guardar_csv(self):
        """Guarda los cambios en el archivo CSV"""
        exito, mensaje = self.data_manager.guardar_csv()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)