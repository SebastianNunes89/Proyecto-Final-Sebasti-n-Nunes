class Departamento:
    def __init__(self, departmentId, displayName):
        self.departmentId = departmentId
        self.displayName= displayName
    def show(self):
        print(" ")
        print(f"Id del departamento: {self.departmentId}")
        print(f"Nombre del departamento: {self.displayName}")
        print(" ")

