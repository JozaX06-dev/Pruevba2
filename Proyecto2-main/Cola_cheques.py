from collections import deque

class ColaCheques:
    def __init__(self):
        self.cola=deque()

    def encolar(self, cheque):
        self.cola.append(cheque)

    def desencolar(self):
        if not self.esta_vacia():
            return self.cola.popleft()
        return None
    
    #Este método lo hice porque el profe había dicho que no se permite utilizar len o empty
    def esta_vacia(self):
        cant = 0
        for _ in self.cola:
            cant += 1
        return cant == 0
    
    def ver_frente(self):
        if not self.esta_vacia():
            return self.cola[0]
        return None
    
    def tamaño(self):
        cant = 0
        for _ in self.cola:
            cant += 1
        return cant
    
    def mostrar_cola(self):
        contenido = []
        for cheque in self.cola:
            nombre = cheque.empleado.nombre
            tipo = cheque.tipo
            monto = cheque.monto
            contenido.append(f"Empleado: {nombre} | Tipo: {tipo} | Monto: ₡{monto}")
        return contenido
    
    