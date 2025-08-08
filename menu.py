from Funcionalidades import Funcionalidades
import requests
import json

class Menu:
    """
    Clase que maneja la interfaz de menú de la aplicación MetroArt.
    """
    
    def __init__(self):
        
        self.funcionalidades = Funcionalidades() 
    
    def mostrar_menu(self):
        """
        Muestra las opciones del menú principal.
        
        """
        print(" ")
        print("-" * 40)
        print("     Bienvenido a MetroArt")
        print(" ")
        print("       ¿Qué deseas hacer?")
        print(" ")
        print(" 1) Ver lista de obras por Departamento.")
        print(" 2) Ver lista de obras por Nacionalidad.")
        print(" 3) Ver lista de obras por nombre del autor.")
        print(" s) Salir")
        print(" ")

    def manejar_opcion(self, num):
        """
        Maneja la opción seleccionada por el usuario.
        '
        """
        if num == "1":
            
            for d in self.funcionalidades.departamentos:
                print(" ")
                d.show()
            
            while True:
                
                print(" ")
                print("Elige un ID para visualizar obras  o coloca 's' para salir: ")
                id_departamento = input(" --> ").strip()
                
                if id_departamento.lower() == 's':
                    break
                
                try:
                    
                    id_departamento = int(id_departamento)
                    
                except ValueError:
                    
                    print("Argumento inválido, debes ingresar un número para el ID.")
                    continue
                
                departamento_encontrado = None
                for d in self.funcionalidades.departamentos:
                    if id_departamento == d.departmentId:
                        departamento_encontrado = d.displayName
                        break
                
                if departamento_encontrado:
                    
                    print(" ")
                    print(f"Buscando obras para el departamento: {departamento_encontrado}")
                    
                    try:
                        
                        url_search = f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={id_departamento}"
                        response_search = requests.get(url_search)
                        response_search.raise_for_status()
                        data = response_search.json()
                        
                        if data.get("objectIDs"):
                            
                            self.funcionalidades.mostrar_obras_paginadas(data["objectIDs"])
                            
                        else:
                            
                            print(f"No se encontraron obras para el departamento: {departamento_encontrado}")
                            
                    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                        
                        print(f"Error al conectar con la API o al procesar la respuesta: {e}")
                    
                    break
                
                else:
            
                    print("ID de departamento no válido. Inténtalo de nuevo.")
                
                    
        elif num == "2":
            
            while True:
                print("Nacionalidades presentes en el museo:")
                print(" ")
                for n in self.funcionalidades.nacionalidades:
                    print(f" - {n}")
                    
                print("")
                print("Introduce una nacionalidad o coloca 's' para salir:")
                nacionalidad = input( "-->  ").strip().capitalize()
                print("")        
                
                if nacionalidad.lower() == 's':
                    break
                    
                if nacionalidad:
                    
                    print(f"Buscando obras por nacionalidad: {nacionalidad}")
                    
                    try:
                        
                        url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={nacionalidad}"
                        informacion_url = requests.get(url)
                        informacion_url.raise_for_status()
                        data = informacion_url.json()
                        
                        if data.get("objectIDs"):
                            
                            nacionalidades_filtradas = []
                            
                            for i in data["objectIDs"]:
                                
                                try:
                                    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}"
                                    informacion_url = requests.get(url)
                                    informacion_url.raise_for_status()
                                    data = informacion_url.json()
                                    
                                    if data.get("artistNationality").lower() == nacionalidad.lower():
                                        nacionalidades_filtradas.append(i)
                                
                                except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                                    
                                    continue
                                
                            self.funcionalidades.mostrar_obras_paginadas(nacionalidades_filtradas)
                            
                        else:
                            
                            print(f"No se encontraron obras para la nacionalidad: {nacionalidad}")
                            
                    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                        
                        print(f"Error al conectar con la API o al procesar la respuesta: {e}")
                    
                    break
                
                else:
                    
                    print("Por favor, introduce una nacionalidad para buscar.")
                    continue
            
        elif num == "3":
            
            while True:
                
                print(" ")
                print("Introduce el nombre del autor o 's' para salir: ")
                nombre_autor = input("--> ").strip()
                
                if nombre_autor.lower() == 's':
                    break
                
                if nombre_autor:
                    
                    print(f"Buscando obras por autor: {nombre_autor}")
                    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={nombre_autor}"
                    
                    try:
                        
                        informacion_url = requests.get(url)
                        informacion_url.raise_for_status()
                        data = informacion_url.json()
                        
                        if data.get("objectIDs"):
                            
                            autores_filtrados = []
                            
                            for i in data["objectIDs"]:
                                
                                try:
                                    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}"
                                    informacion_url = requests.get(url)
                                    informacion_url.raise_for_status()
                                    data = informacion_url.json()
                                    
                                    if data.get("artistDisplayName").lower() == nombre_autor.lower():
                                        autores_filtrados.append(i)
                                
                                except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                                    
                                    continue
                                
                            self.funcionalidades.mostrar_obras_paginadas(autores_filtrados)
                            
                        else:
                            print(f"No se encontraron obras para el autor: {nombre_autor}")
                            
                    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                        
                        print(f"Error al conectar con la API o al procesar la respuesta: {e}")
                    
                    break
                
                else:
                    print("Por favor, introduce un nombre para buscar.")
                    continue
        
        elif num.lower() == "s":
            
            print("Saliendo de la aplicación.")
            return False
        
        else:
            
            print(" ")
            print("Argumento inválido. Por favor, elige una de las opciones.")
            print(" ")
        
        return True

    def run(self):
        """
        Ejecuta el bucle principal del menú.
        
        """
        while True:
            
            self.mostrar_menu()
            opcion = input(" ---> ").strip()
            if not self.manejar_opcion(opcion):
                break
            
