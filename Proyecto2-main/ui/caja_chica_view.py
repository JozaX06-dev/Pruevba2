import customtkinter as ctk
from tkinter import messagebox

class CajaChicaView:
    """Vista para la gestión de Caja Chica"""
    
    def __init__(self, parent, balance, movimientos):
        self.parent = parent
        self.balance = balance
        self.movimientos = movimientos
    
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
        
        title = ctk.CTkLabel(header_frame, text="Gestión de Caja Chica", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        balance_frame = ctk.CTkFrame(left_panel, fg_color="#2b2b2b")
        balance_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(balance_frame, text="Balance Actual", font=ctk.CTkFont(size=14), text_color="gray").pack(pady=(15, 5))
        
        self.balance_label = ctk.CTkLabel(balance_frame, text=f"${self.balance:,.2f}", font=ctk.CTkFont(size=32, weight="bold"), text_color="#2fa572")
        self.balance_label.pack(pady=(5, 15))
        
        ctk.CTkLabel(left_panel, text="Recargar Caja:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10), padx=20, anchor="w")
        
        recarga_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 1000.00")
        recarga_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        def recargar():
            try:
                monto = float(recarga_entry.get())
                self.balance += monto
                self.balance_label.configure(text=f"${self.balance:,.2f}")
                self.movimientos.append(f"Recarga: +${monto:.2f}")
                recarga_entry.delete(0, 'end')
                messagebox.showinfo("Éxito", f"Se recargaron ${monto:.2f}")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")
        
        ctk.CTkButton(left_panel, text="💰 Recargar Caja Chica", command=recargar, fg_color="#2fa572", hover_color="#25824f", height=40).pack(pady=10, padx=20, fill="x")
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Últimos Movimientos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.historial_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.historial_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_historial()
    
    def update_historial(self):
        for widget in self.historial_frame.winfo_children():
            widget.destroy()
        
        if not self.movimientos:
            ctk.CTkLabel(self.historial_frame, text="No hay movimientos", text_color="gray").pack(pady=10)
        else:
            for mov in reversed(self.movimientos[-10:]):
                mov_frame = ctk.CTkFrame(self.historial_frame, fg_color="#2b2b2b")
                mov_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(mov_frame, text=mov, text_color="lightgray").pack(side="left", padx=10, pady=8)