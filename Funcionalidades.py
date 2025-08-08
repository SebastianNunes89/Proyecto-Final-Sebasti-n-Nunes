import requests
import json
from PIL import Image
from Departamento import Departamento
from Obra import Obra
import io
import time

class Funcionalidades:
    """
    Clase principal de la aplicación para interactuar con la API de The Metropolitan Museum of Art.
    """
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/"
    NACIONALIDADES_URL = "https://drive.google.com/uc?export=download&id=1tJEU6_VEeO6xFH8fssSfkw4M8MaN6U5A" 

    def __init__(self):
        """
        Inicializa la aplicación con los datos de departamentos.
        """
        self.departamentos = self.load_departamentos()
        self.nacionalidades = self.load_nacionalidades()

    def load_departamentos(self):
        
        """
        Carga la lista de departamentos.
        
        """
        while True:
            try:
                
                departamento_url = f"{self.BASE_URL}departments"
                departamento_url = requests.get(departamento_url)
                departamentos = departamento_url.json()
                return [Departamento(d["departmentId"], d["displayName"]) for d in departamentos["departments"]]
                
            
            except requests.exceptions.RequestException:
                
                print("Error al cargar los departamentos, intentando nuevamente...")
                time.sleep(5)  
                continue
            
    
    
    def load_nacionalidades(self):
        """
        Descarga y carga la lista de nacionalidades desde una URL.
        
        """
        while True:
            try:
                
                nacionalidades = requests.get(self.NACIONALIDADES_URL)
                nacionalidades.raise_for_status() 
                
                contenido = nacionalidades.text
                nacionalidades_sucias = contenido.splitlines()
                nacionalidades_limpias = [nacionalidad.strip() for nacionalidad in nacionalidades_sucias]
                return nacionalidades_limpias 
            
            except requests.exceptions.RequestException as e:
                
                print("Error al cargar las nacionalidades, intentando nuevamente...")
                time.sleep(5)  
                continue

    def mostrar_obras_paginadas(self, lista_ids):
        """
        Muestra una lista de obras de forma paginada y permite ver sus detalles.
        Args:
        lista_ids (list): Una lista de identificadores de objetos (IDs) de obras
        que se obtienen de la API. Se espera que sean enteros.
        
        """
        if not lista_ids:
            
            print("No se encontraron obras para la búsqueda.")
            return

        obras_por_pagina = 10
        total_obras = len(lista_ids)
        pagina_actual = 0
        
        while True:
            
            inicio = pagina_actual * obras_por_pagina
            fin = min(inicio + obras_por_pagina, total_obras)
            
            if inicio >= total_obras:
                
                print("No hay más obras para mostrar.")
                break

            print("\n--- Mostrando obras ---")
            print(f"Página {pagina_actual + 1} de { (total_obras // obras_por_pagina) + 1}")
            obras_cargadas = []

            for i in lista_ids[inicio:fin]:
                url_obra = f"{self.BASE_URL}/objects/{i}"
                reintentos = 2
                obra_lista = False 
                
                while reintentos > 0 and not obra_lista:
                    
                    try:
                        response_obra = requests.get(url_obra)
                        response_obra.raise_for_status()
                        data_obra = response_obra.json()
                        
                        obra = Obra(
                        titulo=data_obra.get("title"),
                        departamento=data_obra.get("department"),
                        nombre_artista=data_obra.get("artistDisplayName"),
                        nacionalidad_artista=data_obra.get("artistNationality", ""),
                        fecha_nacimiento=data_obra.get("artistBeginDate", ""),
                        fecha_muerte=data_obra.get("artistEndDate", ""),
                        tipo=data_obra.get("classification", ""),
                        ano_creacion=data_obra.get("objectDate", ""),
                        imagen_obra=data_obra.get("primaryImage", ""),
                        id=data_obra.get("objectID"))
                        obras_cargadas.append(obra)
                        obra_lista = True
                        
                        if obra.nombre_artista == "":
                            
                            print(f" {obra.titulo} (Autor desconocido) - ID: {obra.id}")

                        
                        else:
                            print(f" {obra.titulo} ({obra.nombre_artista}) - ID: {obra.id}")


                    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                        
                        reintentos -= 1
                        if reintentos > 0:
                            print(f"Error al obtener los detalles de la obra con ID {i}: {e}. Reintentando en 3 segundos...")
                            time.sleep(3) 
                        else:
                            print(f"Error persistente al obtener la obra con ID {i} después de varios intentos. Saltando esta obra.")
            
            print("")
            print("Presiona 'Enter' para ver la siguiente página, 'r' para reiniciar la página actual o 's' para salir. Para ver los detalles de una obra, introduce su ID:  >>> ")
            opcion = input(">>> ").strip()

            if opcion.lower() == 's':
                
                break
            
            if opcion.lower() == 'r':
                
                continue
            
            elif opcion.isdigit():
                
                obra_encontrada = None 
                
                for obra in obras_cargadas:
                    if obra.id == int(opcion):
                        
                        obra_encontrada = obra
                        break 
                
                if obra_encontrada:
                    
                    print("\n--- Mostrando detalles de la obra seleccionada ---")
                    obra_encontrada.show()
                    
                    if obra_encontrada.imagen_obra:
                        
                        ver_imagen = input("¿Desea ver la imagen de la obra? (s/n): ").strip().lower()
                        if ver_imagen == 's':
                            
                            print("Descargando y mostrando la imagen...")
                            self.guardar_y_mostrar_imagen(obra_encontrada.imagen_obra, f"obra_{obra_encontrada.id}")
                    else:
                        
                        print("No hay una imagen disponible para esta obra.")

                    print("-" * 110)
                else:
                    
                    print(f"El ID {opcion} no se encuentra en las obras de esta página.")
                
                input("\nOprime enter para regresar a la página actual: ")
                
                continue
            
            else:
                
                pagina_actual += 1
                

    def guardar_y_mostrar_imagen(self, url, nombre_archivo):
        """
        Descarga una imagen desde una URL y la muestra.
         Argumentos:
        url (str): La URL de la imagen a descargar.
        nombre_archivo (str): El nombre con el que se mostrará la imagen.
        
        """
        try:
            
            datos_imagen = requests.get(url, stream=True)
            datos_imagen.raise_for_status()
            
            imagen = Image.open(io.BytesIO(datos_imagen.content))
            imagen.show(title=nombre_archivo)
            
        except requests.exceptions.RequestException as e:
            
            print(f"Error al descargar la imagen: {e}")
            
        except Exception as e:
            
            print(f"Error al procesar la imagen: {e}")
            
