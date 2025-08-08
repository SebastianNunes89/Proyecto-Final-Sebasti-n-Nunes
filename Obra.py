class Obra:
    def __init__(self, titulo, departamento, nombre_artista, nacionalidad_artista, fecha_nacimiento, fecha_muerte, tipo, ano_creacion, imagen_obra, id):
        self.titulo = titulo
        self.departamento = departamento
        self.nombre_artista = nombre_artista
        self.nacionalidad_artista = nacionalidad_artista
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_muerte = fecha_muerte
        self.tipo = tipo
        self.ano_creacion = ano_creacion
        self.imagen_obra = imagen_obra
        self.id = id
        
    def show(self):
        print(f"El título de la obra es: {self.titulo}")
        if self.nombre_artista == "":
            print(" Artista desconocido")
        else:
            print(f"El artista de la obra es: {self.nombre_artista}")
            print(f"La nacionalidad del artista es: {self.nacionalidad_artista}")
            if self.fecha_nacimiento and self.fecha_muerte:
                print(f"{self.nombre_artista} nació en el año {self.fecha_nacimiento}, falleció en el año {self.fecha_muerte}")
        if self.tipo == "":
            pass
        else:
            print(f"La clasificación de la obra es: {self.tipo}")
        if self.ano_creacion == "":
            pass
        else:
            print(f"El año de creación de la obra es: {self.ano_creacion}")

        
        

       

        
