import customtkinter as ctk
from tkinter import messagebox

class ListaView:
    
    def __init__(self, parent, lista_impresion, data_manager, main_window):
        self.parent = parent
        self.lista_impresion = lista_impresion
        self.data_manager = data_manager
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
        
        title = ctk.CTkLabel(header_frame, text="Lista/Tupla: Imprimir Cheques", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text="Gestión de lista de cheques listos para impresión", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"✓ Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#2fa572"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar Cheque a Lista", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
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
        
        ctk.CTkLabel(left_panel, text="Monto del Cheque:").pack(pady=(10, 5), padx=20, anchor="w")
        monto_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 3500.00")
        monto_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Concepto:").pack(pady=(10, 5), padx=20, anchor="w")
        concepto_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: Pago de nómina quincenal")
        concepto_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Fecha:").pack(pady=(10, 5), padx=20, anchor="w")
        fecha_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 2025-10-22")
        fecha_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        def add():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = empleado_menu.get()
            monto = monto_entry.get()
            concepto = concepto_entry.get()
            fecha = fecha_entry.get()
            
            if seleccion and monto and "No hay empleados" not in seleccion:
                try:
                    float(monto)
                    id_emp = seleccion.split(" - ")[-1]
                    nombre_emp = seleccion.split(" - ")[0]
                    
                    cheque = (id_emp, nombre_emp, monto, concepto if concepto else "Pago de nómina", fecha if fecha else "Pendiente")
                    self.lista_impresion.append(cheque)
                    self.update_list_display()
                    
                    self.main_window.guardar_estado_completo()
                    
                    monto_entry.delete(0, 'end')
                    concepto_entry.delete(0, 'end')
                    fecha_entry.delete(0, 'end')
                    messagebox.showinfo("Éxito", f"Cheque agregado a la lista para {nombre_emp}")
                except ValueError:
                    messagebox.showerror("Error", "El monto debe ser un número válido")
            else:
                messagebox.showwarning("Advertencia", "Completa al menos el empleado y el monto")
        
        def print_all():
            if self.lista_impresion:
                cantidad = len(self.lista_impresion)
                total = sum(float(cheque[2]) for cheque in self.lista_impresion)
                messagebox.showinfo(
                    "Imprimir Todos los Cheques", 
                    f"Se imprimirían {cantidad} cheques\n\nTotal: ${total:,.2f}\n\n¡Proceso de impresión iniciado!"
                )
            else:
                messagebox.showinfo("Lista Vacía", "No hay cheques para imprimir")
        
        def clear():
            if self.lista_impresion:
                respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres limpiar toda la lista?")
                if respuesta:
                    self.lista_impresion.clear()
                    self.update_list_display()
                    
                    self.main_window.guardar_estado_completo()
                    
                    messagebox.showinfo("Lista Limpiada", "Todos los cheques fueron removidos")
            else:
                messagebox.showinfo("Lista Vacía", "La lista ya está vacía")
        
        ctk.CTkButton(left_panel, text="➕ Agregar a Lista", command=add, fg_color="#2fa572", hover_color="#25824f").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🖨️ Imprimir Todos", command=print_all, fg_color="#3b8ed0", hover_color="#2d6fa3").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Limpiar Lista", command=clear, fg_color="#6b7280", hover_color="#4b5563").pack(pady=5, padx=20, fill="x")
        
        stats_frame = ctk.CTkFrame(left_panel, fg_color="#2b2b2b")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.stats_label.pack(pady=15)
        
        self.update_stats()
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Lista de Cheques", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text="Cheques listos para impresión\nLos elementos se mantienen en orden de inserción",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.list_display = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.list_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_list_display()
    
    def update_stats(self):
        if self.lista_impresion:
            cantidad = len(self.lista_impresion)
            total = sum(float(cheque[2]) for cheque in self.lista_impresion)
            texto = f"📊 Estadísticas\n\nCheques en lista: {cantidad}\nMonto total: ${total:,.2f}"
        else:
            texto = "📊 Estadísticas\n\nNo hay cheques en la lista"
        
        self.stats_label.configure(text=texto)
    
    def update_list_display(self):
        for widget in self.list_display.winfo_children():
            widget.destroy()
        
        if not self.lista_impresion:
            ctk.CTkLabel(self.list_display, text="No hay cheques en la lista\n\nAgrega cheques para comenzar", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            for idx, (id_emp, nombre, monto, concepto, fecha) in enumerate(self.lista_impresion, 1):
                cheque_frame = ctk.CTkFrame(self.list_display, fg_color="#1a1a1a", border_width=2, border_color="#2fa572")
                cheque_frame.pack(fill="x", pady=10, padx=5)
                
                header_frame = ctk.CTkFrame(cheque_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=15, pady=(15, 5))
                
                ctk.CTkLabel(header_frame, text=f"📄 Cheque #{idx}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2fa572").pack(side="left")
                
                info_text = f"👤 Empleado: {nombre}\n🆔 ID: {id_emp}\n💰 Monto: ${float(monto):,.2f}\n📝 Concepto: {concepto}\n📅 Fecha: {fecha}"
                ctk.CTkLabel(cheque_frame, text=info_text, text_color="lightgray", justify="left", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=15, pady=(5, 10))
                
                def eliminar_cheque(index=idx-1):
                    respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar el cheque #{index+1}?")
                    if respuesta:
                        self.lista_impresion.pop(index)
                        self.update_list_display()
                        
                        self.main_window.guardar_estado_completo()
                
                ctk.CTkButton(
                    cheque_frame, 
                    text="🗑️ Eliminar", 
                    command=eliminar_cheque,
                    width=100,
                    height=25,
                    fg_color="#dc2626",
                    hover_color="#b91c1c",
                    font=ctk.CTkFont(size=10)
                ).pack(padx=15, pady=(0, 10), anchor="e")
        
        self.update_stats()