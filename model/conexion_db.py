import sqlite3
import os

class conexionDB:
    def __init__(self, base_datos=None):
        # Puedes pasar la ruta como parámetro, o usar esta por defecto
        db_folder = os.path.join(
            os.path.expanduser("~"),
            "OneDrive", "Escritorio", "codes", "LabChem", "dabagui_two", "databaGUI", "database", 
        ) # Ubicarse en la carpeta donde se guardará la base de datos
        if not os.path.exists(db_folder):
            os.makedirs(db_folder) # Crear carpeta si no existe
        self.base_datos = base_datos or os.path.join(db_folder, "pumadb.db")
        self.conexion = None
        self.cursor = None

# ------------------------------
#   Entrar a la base de datos
# ------------------------------
    def __enter__(self):
        self.conexion = sqlite3.connect(self.base_datos) # Conexión a la base de datos
        self.cursor = self.conexion.cursor() # Cursor para ejecutar comandos SQL
        return self
# ------------------------------
#   Salir de la base de datos
# ------------------------------

    def __exit__(self, exc_type, exc_value, traceback): # Cierra la conexión al salir del bloque with
        if self.conexion:
            self.conexion.commit() # Guarda los cambios
            self.conexion.close() # Cierra la conexión