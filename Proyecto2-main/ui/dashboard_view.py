import customtkinter as ctk

class DashboardView:
    """Vista del Dashboard con estadísticas generales"""
    
    def __init__(self, parent, data_manager, cola_length, pila_length, dict_length):
        self.parent = parent
        self.data_manager = data_manager
        self.cola_length = cola_length
        self.pila_length = pila_length
        self.dict_length = dict_length
    
    def render(self):
        """Renderiza el dashboard"""
        self.create_header()
        self.create_stats_cards()
        self.create_welcome_message()
    
    def create_header(self):
        """Crea el encabezado"""
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Resumen general del sistema",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(anchor="w")
    
    def create_stats_cards(self):
        """Crea las tarjetas de estadísticas"""
        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="nsew")
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        stats = [
            ("👥 Empleados", str(self.data_manager.obtener_cantidad_empleados()), "#3b8ed0"),
            ("📋 Cola Cheques", str(self.cola_length), "#2fa572"),
            ("📚 Pila Activa", str(self.pila_length), "#d97706"),
            ("📖 Diccionario", str(self.dict_length), "#dc2626")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = self.create_stat_card(cards_frame, label, value, color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
    
    def create_stat_card(self, parent, title, value, color):
        """Crea una tarjeta de estadística individual"""
        card = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        title_label.pack(pady=(20, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(5, 20))
        
        return card
    
    def create_welcome_message(self):
        """Crea el mensaje de bienvenida"""
        viz_frame = ctk.CTkFrame(self.parent, fg_color="#1a1a1a")
        viz_frame.grid(row=2, column=0, sticky="nsew", pady=20)
        viz_frame.grid_rowconfigure(0, weight=1)
        
        info_label = ctk.CTkLabel(
            viz_frame,
            text="Bienvenido al Sistema de Nómina\n\nSelecciona una opción del menú para visualizar las estructuras de datos",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        info_label.pack(expand=True, pady=50)