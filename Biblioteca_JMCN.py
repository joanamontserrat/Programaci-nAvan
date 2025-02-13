from datetime import datetime, timedelta

class Recurso:
    def __init__(self, titulo, disponible=True):
        self.titulo = titulo
        self.disponible = disponible

    def marcar_prestado(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def marcar_devuelto(self):
        self.disponible = True

class Libro(Recurso):
    def __init__(self, titulo, autor, genero):
        super().__init__(titulo)
        self.autor = autor
        self.genero = genero

class Revista(Recurso):
    def __init__(self, titulo, edicion, frecuencia):
        super().__init__(titulo)
        self.edicion = edicion
        self.frecuencia = frecuencia

class RecursoDigital(Recurso):
    def __init__(self, titulo, tipo_archivo, url):
        super().__init__(titulo)
        self.tipo_archivo = tipo_archivo
        self.url = url

class Individuo:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

class Lector(Individuo):
    def __init__(self, nombre, email):
        super().__init__(nombre, email)
        self.recursos_prestados = []
        self.multa_acumulada = 0

    def buscar_en_catalogo(self, catalogo):
        catalogo.listar_recursos()

    def solicitar_recurso(self, recurso, bibliotecario):
        bibliotecario.gestionar_prestamo(self, recurso)

    def devolver_recurso(self, recurso, bibliotecario):
        bibliotecario.gestionar_devolucion(self, recurso)

class Encargado(Individuo):
    def __init__(self, nombre, email, biblioteca):
        super().__init__(nombre, email)
        self.biblioteca = biblioteca

    def agregar_recurso(self, recurso):
        self.biblioteca.anadir_recurso(recurso)

    def gestionar_prestamo(self, lector, recurso):
        if recurso.marcar_prestado():
            lector.recursos_prestados.append(recurso)
            print(f"{lector.nombre} ha tomado prestado: {recurso.titulo}")
        else:
            print(f"El recurso '{recurso.titulo}' no está disponible.")

    def gestionar_devolucion(self, lector, recurso):
        if recurso in lector.recursos_prestados:
            lector.recursos_prestados.remove(recurso)
            recurso.marcar_devuelto()
            print(f"{lector.nombre} ha devuelto: {recurso.titulo}")
        else:
            print(f"El lector no tiene este recurso en su lista de préstamos.")

class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.recursos = []

    def anadir_recurso(self, recurso):
        self.recursos.append(recurso)

    def transferir_recurso(self, recurso, otra_biblioteca):
        if recurso in self.recursos:
            self.recursos.remove(recurso)
            otra_biblioteca.anadir_recurso(recurso)
            print(f"'{recurso.titulo}' ha sido transferido a {otra_biblioteca.nombre}.")

class RegistroMultas:
    def __init__(self, lector, dias_retraso):
        self.lector = lector
        self.dias_retraso = dias_retraso
        self.multa = dias_retraso * 5
        lector.multa_acumulada += self.multa

    def mostrar_multa(self):
        print(f"{self.lector.nombre} tiene una multa de ${self.multa} por {self.dias_retraso} días de retraso.")

class Catalogo:
    def __init__(self):
        self.recursos_disponibles = []

    def incluir_recurso(self, recurso):
        self.recursos_disponibles.append(recurso)

    def buscar_por_titulo(self, titulo):
        return [r for r in self.recursos_disponibles if titulo.lower() in r.titulo.lower()]

    def listar_recursos(self):
        for recurso in self.recursos_disponibles:
            estado = "Disponible" if recurso.disponible else "Prestado"
            print(f"{recurso.titulo} - {estado}")

#Uso
biblioteca_central = Biblioteca("Central Universitaria")
biblioteca_computacion = Biblioteca("Facultad de Computacion")

encargado = Encargado("Rogelio Lopez", "ro.lopez@alm.bua.mx", biblioteca_central)
lector = Lector("Montserrat Carmona", "cn202466401@alm.buap.mx")

libro = Libro("Programacion General", "Resnick & Halliday", "Computacion")
revista = Revista("National Geographic", "Febrero 2025", "Mensual")
recurso_digital = RecursoDigital("Manual de Python", "PDF", "https://uni.edu/python.pdf")

encargado.agregar_recurso(libro)
encargado.agregar_recurso(revista)
lector.solicitar_recurso(libro, encargado)
lector.devolver_recurso(libro, encargado)

registro_multa = RegistroMultas(lector, 3)
registro_multa.mostrar_multa()

biblioteca_central.transferir_recurso(libro, biblioteca_computacion)
