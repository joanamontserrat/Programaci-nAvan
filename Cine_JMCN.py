class Persona:
    registro = []
    
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def guardar(self):
        Persona.registro.append(self)
        print(f"{self.nombre} ha sido añadida al sistema con el correo {self.correo}.")

    def modificar(self, nuevo_nombre, nuevo_correo):
        self.nombre = nuevo_nombre
        self.correo = nuevo_correo
        print(f"Información actualizada: {self.nombre}, {self.correo}")

    @classmethod
    def mostrar_registro(cls):
        print("Listado de personas registradas:")
        for p in cls.registro:
            print(f"Nombre: {p.nombre}, Correo: {p.correo}")


class Usuario(Persona):
    def __init__(self, nombre, correo):
        super().__init__(nombre, correo)
        self.reservas = []

    def hacer_reserva(self, funcion, cantidad_asientos):
        if cantidad_asientos <= funcion.asientos_disponibles:
            funcion.asientos_disponibles -= cantidad_asientos
            self.reservas.append({"funcion": funcion, "asientos": cantidad_asientos})
            print(f"Reserva realizada para '{funcion.pelicula.titulo}' en la sala {funcion.sala.identificador}.")
        else:
            print("No hay suficientes asientos disponibles para esta reserva.")

    def anular_reserva(self, funcion):
        reserva = next((r for r in self.reservas if r["funcion"] == funcion), None)
        if reserva:
            funcion.asientos_disponibles += reserva["asientos"]
            self.reservas.remove(reserva)
            print(f"Reserva para '{funcion.pelicula.titulo}' cancelada.")
        else:
            print("No se encontró una reserva para esta función.")


class Empleado(Persona):
    def __init__(self, nombre, correo, rol):
        super().__init__(nombre, correo)
        self.rol = rol

    def programar_funcion(self, funcion):
        print(f"Función programada: '{funcion.pelicula.titulo}' a las {funcion.hora} en {funcion.sala.identificador}.")

    def ajustar_promocion(self, promocion, nuevo_descuento, nuevas_condiciones):
        promocion.descuento = nuevo_descuento
        promocion.condiciones = nuevas_condiciones
        print(f"Promoción actualizada: {nuevo_descuento}% de descuento. {nuevas_condiciones}")


class Espacio:
    def __init__(self, capacidad, identificador):
        self.capacidad = capacidad
        self.identificador = identificador

    def detalles(self):
        print(f"Espacio ID: {self.identificador}, Capacidad: {self.capacidad}")


class Sala(Espacio):
    def __init__(self, capacidad, identificador, tipo):
        super().__init__(capacidad, identificador)
        self.tipo = tipo
        self.esta_disponible = True

    def verificar_disponibilidad(self):
        print("Sala disponible" if self.esta_disponible else "Sala ocupada")


class Pelicula:
    def __init__(self, titulo, genero, duracion):
        self.titulo = titulo
        self.genero = genero
        self.duracion = duracion


class Funcion:
    def __init__(self, pelicula, sala, hora, asientos_disponibles=None):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora
        self.asientos_disponibles = asientos_disponibles or sala.capacidad


class Promocion:
    def __init__(self, descuento, condiciones):
        self.descuento = descuento
        self.condiciones = condiciones

    def mostrar(self):
        print(f"Promoción: {self.descuento}% de descuento. {self.condiciones}")


#Uso
pelicula1 = Pelicula("Percy Jackson", "Ciencia Ficción", 136)
pelicula2 = Pelicula("De todos los chicos de los que me enamore", "Drama/Romance", 195)

sala1 = Sala(100, "Sala 4", "4D")
sala2 = Sala(50, "Sala 5", "VIP")

funcion1 = Funcion(pelicula1, sala1, "18:00")
funcion2 = Funcion(pelicula2, sala2, "20:00")

usuario1 = Usuario("Montserrat Carmona", "joanamontse11@gmail.com")
empleado1 = Empleado("Rosa Gonazalez", "rosa.gonzalez@gmail.com", "Gerente")

usuario1.guardar()
empleado1.guardar()

usuario1.hacer_reserva(funcion1, 3)
usuario1.anular_reserva(funcion1)

promocion1 = Promocion(20, "Válido de lunes a sabado.")
promocion1.mostrar()
empleado1.ajustar_promocion(promocion1, 30, "Válido antes de las 4 PM.")

Persona.mostrar_registro()
