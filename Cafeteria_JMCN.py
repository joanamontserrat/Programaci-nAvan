class Persona:
    registros = []

    def __init__(self, nombre, contacto):
        self.nombre = nombre
        self.contacto = contacto

    def agregar_registro(self):
        Persona.registros.append(self)
        print(f"Registro exitoso: {self.nombre}.")

    @classmethod
    def listar_registros(cls):
        print("Listado de personas registradas:")
        for persona in cls.registros:
            print(f"- {persona.nombre}, Contacto: {persona.contacto}")

class Cliente(Persona):
    def __init__(self, nombre, contacto):
        super().__init__(nombre, contacto)
        self.pedidos = []

    def hacer_pedido(self, orden):
        if orden.validar():
            self.pedidos.append(orden)
            orden.confirmar()
        else:
            print("El pedido no puede procesarse por falta de inventario.")

    def historial_pedidos(self):
        print(f"Historial de {self.nombre}:")
        for orden in self.pedidos:
            print(f"- Productos: {orden.productos}, Estado: {orden.estado}, Total: ${orden.total}")

class Empleado(Persona):
    def __init__(self, nombre, contacto, posicion):
        super().__init__(nombre, contacto)
        self.posicion = posicion

    def modificar_inventario(self, inventario, item, cantidad):
        inventario.actualizar(item, cantidad)

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Bebida(Producto):
    def __init__(self, nombre, precio, tamano, tipo, opciones=None):
        super().__init__(nombre, precio)
        self.tamano = tamano
        self.tipo = tipo
        self.opciones = opciones if opciones else []

class Postre(Producto):
    def __init__(self, nombre, precio, es_vegano=False, sin_gluten=False):
        super().__init__(nombre, precio)
        self.es_vegano = es_vegano
        self.sin_gluten = sin_gluten

class Inventario:
    def __init__(self):
        self.stock = {}

    def actualizar(self, item, cantidad):
        self.stock[item] = self.stock.get(item, 0) + cantidad
        print(f"Inventario actualizado: {item} -> {self.stock[item]} unidades.")

    def verificar_disponibilidad(self, requerimientos):
        return all(self.stock.get(item, 0) >= cantidad for item, cantidad in requerimientos.items())

    def consumir(self, requerimientos):
        if self.verificar_disponibilidad(requerimientos):
            for item, cantidad in requerimientos.items():
                self.stock[item] -= cantidad
            return True
        return False

class Pedido:
    def __init__(self, cliente, productos, inventario):
        self.cliente = cliente
        self.productos = productos
        self.estado = "Pendiente"
        self.total = sum(p.precio for p in productos)
        self.inventario = inventario

    def validar(self):
        requerimientos = {}
        return self.inventario.verificar_disponibilidad(requerimientos)

    def confirmar(self):
        if self.inventario.consumir({}):
            self.estado = "En preparación"
            print(f"Pedido confirmado. Total: ${self.total}.")
        else:
            print("No se puede procesar el pedido por falta de inventario.")

class Promocion:
    def __init__(self, descripcion, descuento):
        self.descripcion = descripcion
        self.descuento = descuento

    def aplicar(self, pedido):
        pedido.total *= (1 - self.descuento / 100)
        print(f"Promoción aplicada: {self.descripcion}. Total final: ${pedido.total}.")

#Uso
almacen = Inventario()
almacen.actualizar("Café", 15)
almacen.actualizar("Leche", 10)

cliente = Cliente("Montserrat Carmona", "joanamontse11@gmail.com")
cliente.agregar_registro()

empleado = Empleado("Gloria Ortega", "ortega.gloria@gmail.com", "Barista")
empleado.agregar_registro()

cafe = Bebida("Café Americano", 2.5, "Mediano", "Caliente", ["Sin azúcar"])
pastel = Postre("Cheesecake", 3.5, sin_gluten=True)

orden = Pedido(cliente, [cafe, pastel], almacen)
cliente.hacer_pedido(orden)

promo = Promocion("Descuento del 15%", 15)
promo.aplicar(orden)

cliente.historial_pedidos()
Persona.listar_registros()
