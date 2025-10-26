class Pila_Contrato:
    def __init__(self):
        self.pila = []

    def apilar(self, cheque):
        self.pila.append(cheque)

    def desapilar(self):
        if not self.esta_vacia():
            return self.pila.pop()
        return None
    
    def esta_vacia(self):
        cant = 0
        for _ in self.pila:
            cant += 1
        return cant == 0
    
    def tamaño(self):
        cant = 0
        for _ in self.pila:
            cant += 1
        return cant
    
    def ver_tope(self):
        if not self.esta_vacia():
            return self.pila[-1]
        return None
    
    def mostrar_pila(self):
        contenido = []
        i = self.tamaño() - 1
        while i >= 0:
            cheque = self.pila[i]
            emp = cheque.empleado
            contenido.append(f"Empleado: {emp.nombre} | Puesto: {emp.puesto} | Salario: ₡{emp.salario}")
            i -= 1
        return contenido