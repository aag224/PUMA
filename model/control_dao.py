from model.conexion_db import conexionDB
from tkinter import messagebox as mb

# ------------------------------
# Creación de tablas al iniciar
# ------------------------------
def create_tables():
    tablas = {
        "Control": """CREATE TABLE IF NOT EXISTS Control (
            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Cuenta_id" INTEGER,
            "Clave" TEXT NOT NULL COLLATE RTRIM,
            "Fecha" TEXT NOT NULL,
            "Material" TEXT,
            FOREIGN KEY("Cuenta_id") REFERENCES Login("ID"),
            FOREIGN KEY("Clave") REFERENCES Investigacion("Clave")
        )""",

        "Identificacion": """CREATE TABLE IF NOT EXISTS Identificacion (
            "NoCuenta" INTEGER PRIMARY KEY,
            "Correo" TEXT,
            "Numero_Celular" TEXT,
            "Nombre_Completo" TEXT UNIQUE,
            "Posgrado" TEXT
        )""",

        "Investigacion": """CREATE TABLE IF NOT EXISTS Investigacion (
            "Clave" INTEGER PRIMARY KEY,
            "Reaccion" TEXT UNIQUE,
            "Rendimiento" TEXT,
            "Estatus" TEXT NULL
        )""",

        "Login": """CREATE TABLE IF NOT EXISTS Login (
            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "NoCuenta" INTEGER,
            "Password" TEXT,
            FOREIGN KEY("NoCuenta") REFERENCES Identificacion("NoCuenta")
        )"""
    }

    with conexionDB() as db:
        for tabla_sql in tablas.values(): # Los valores del diccionario pasan a formar la base de datos
            db.cursor.execute(tabla_sql)  #  el uso de un ciclo for permite pasar una tabla por una

create_tables()

# ------------------------------
# Modelo de datos Control
# ------------------------------
class Control:
    def __init__(self, Cuenta_id, Clave, Fecha, Material=None):
        self.Cuenta_id = Cuenta_id
        self.Clave = Clave
        self.Fecha = Fecha
        self.Material = Material  # Puede ser None si no se adjunta un archivo

    def __str__(self):
        return f'CONTROL[{self.Clave}, {self.Fecha}, {self.Material}]'

# ------------------------------
# Operaciones CRUD
# ------------------------------
def nuevo(control):
    sql = """
        INSERT INTO Control (Cuenta_id, Clave, Fecha, Material)
        VALUES (?, ?, ?, ?)"""
    try:
        with conexionDB() as db:
            db.cursor.execute(sql, (
                control.Cuenta_id,
                control.Clave,
                control.Fecha,
                control.Material
            ))
        mb.showinfo('Conexión a la base de datos', 'El registro fue exitoso')
    except Exception as e:
        mb.showwarning('Conexión a la base de datos', f'Error de registro: {e}')

def listar():
    sql = """
    SELECT Control.ID, Control.Clave, Control.Fecha, Control.Material, Login.ID
    FROM Control
    INNER JOIN Login ON Control.Cuenta_id = Login.ID
"""
    with conexionDB() as db:
        db.cursor.execute(sql)
        return db.cursor.fetchall()

def editar(control, ID):
    sql = """
        UPDATE Control
        SET Clave = ?, Fecha = ?, Material = ?
        WHERE ID = ?"""
    try:
        with conexionDB() as db:
            db.cursor.execute(sql, (
                control.Clave,
                control.Fecha,
                control.Material,
                ID
            ))
        mb.showinfo('Editar registro', 'Se ha editado el registro')
    except Exception as e:
        mb.showerror('Editar registro', f'No se pudo editar: {e}')

def eliminar(ID):
    sql = 'DELETE FROM Control WHERE ID = ?'
    try:
        with conexionDB() as db:
            db.cursor.execute(sql, (ID,))
        mb.showinfo('Eliminar registro', 'Se ha eliminado el registro')
    except Exception as e:
        mb.showerror('Eliminar registro', f'No se pudo eliminar: {e}')

def busca_users(users):
    sql = 'SELECT * FROM Login WHERE NoCuenta = ?'
    with conexionDB() as db:
        db.cursor.execute(sql, (users,))
        return db.cursor.fetchall()

def busca_password(password):
    sql = 'SELECT * FROM Login WHERE Password = ?'
    with conexionDB() as db:
        db.cursor.execute(sql, (password,))
        return db.cursor.fetchall()
    
def buscar_material(material):
    sql = 'SELECT Material FROM Control WHERE NoCuenta = ?'
    with conexionDB() as db:
        db.cursor.execute(sql, (material,))
        return db.cursor.fetchall()
    
def mostrar_material(control_id):
    sql = 'SELECT * FROM Control WHERE ID = ?'
    with conexionDB() as db:
        db.cursor.execute(sql, (control_id,))
        result = db.cursor
        return result[0] if result else None
