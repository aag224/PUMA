from tkinter import ttk, messagebox as mb, filedialog
import tkinter as tk
import os
import shutil
from model.control_dao import Control, nuevo, listar, editar, eliminar, busca_password, busca_users, buscar_material
from datetime import datetime
from model.conexion_db import conexionDB 
import subprocess
import pyautogui

class Fr(tk.Frame):
    def __init__(self, master):
        super().__init__(master,bg="white",width=1200, height=480)
        self.pack()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        self.crear_widgets()
        self.usuario_activo = None  # Para rastrear el usuario activo
        self.material_data = None  # Para almacenar el archivo adjunto

    def crear_widgets(self):
        self.clave_var = tk.StringVar()
        self.fecha_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.material_name_var = tk.StringVar()
        self.noCuenta_var = tk.StringVar()
        self.password_var = tk.StringVar() 

        # Entradas
        tk.Label(self, text="No. de cuenta:",bg="white",fg="black",font=("Open Sans",16, 'bold')).place(x=22, y=10)
        tk.Entry(self, textvariable=self.noCuenta_var,font=("Arial", 12), bg="#f0f0f0", fg="#333", relief="sunken", bd=0.5,width=16).place(x=22, y=55)

        tk.Label(self, text="Contraseña:",bg="white",fg="black",font=("Open Sans",16, 'bold')).place(x=22, y=80)
        tk.Entry(self, textvariable=self.password_var, show="*",font=("Arial", 12), bg="#f0f0f0", fg="#333", relief="sunken", bd=0.5,width=16).place(x=22, y=125)
        
        tk.Label(self, text="Clave:",bg="white",fg="black",font=("Open Sans",16, 'bold')).place(x=22, y=150)
        tk.Entry(self, textvariable=self.clave_var,font=("Arial", 12), bg="#f0f0f0", fg="#333", relief="sunken", bd=0.5,width=16).place(x=22, y=195)

        tk.Label(self, text="Fecha:",bg="white",fg="black",font=("Open Sans",16, 'bold')).place(x=22, y=220)
        tk.Entry(self, textvariable=self.fecha_var,font=("Arial", 12), bg="#f0f0f0", fg="#333", relief="sunken", bd=0.5,width=16).place(x=22, y=265)

        tk.Label(self, text="Documento:",bg="white",fg="black",font=("Open Sans",16, 'bold')).place(x=22, y=290)
        doc = tk.Entry(self, textvariable=self.material_name_var,font=("Arial", 12), bg="#f0f0f0", fg="#333", relief="sunken", bd=0.5,width=12).place(x=22, y=335)

        # Tabla(columnas, encabezados, ancho de columnas)
        self.tabla = ttk.Treeview(self, columns=("Cuenta_id", "Clave", "Fecha", "Material"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=20)
        self.tabla.place(x=280, y=10, width=850, height=350)
        self.tabla.bind("<ButtonRelease-1>", self.cargar_datos_tabla)

        # Botones(texto, comando, ancho, fuente, color de texto, color de fondo, cursor, color al hacer clic)
        tk.Button(self, text="Buscar",width=10, command=self.buscar_por_cuenta, font=('Open Sans', 16,'bold'), fg='#FFFFFF', bg="#464646", cursor='hand2',activebackground="#BABABA").place(x=40, y=400)
        tk.Button(self, text="Nuevo", command=self.verificacion_nuevo,width=10, font=('Open Sans', 16,'bold'), fg='#FFFFFF', bg='#1658A2', cursor='hand2',activebackground='#3586DF').place(x=270, y=400)
        tk.Button(self, text="Editar", command=self.verificacion_actualizar,width=10, font=('Open Sans', 16,'bold'), fg='#FFFFFF', bg='#FFCE49', cursor='hand2', activebackground='#35BD6F').place(x=500, y=400)
        tk.Button(self, text="Eliminar", command=self.verificacion_eliminar,width=10, font=('Open Sans', 16,'bold'), fg='#FFFFFF', bg='#BD152E', cursor='hand2',activebackground='#E15370').place(x=960, y=400)
        tk.Button(self, text="Cargar", command=self.cargar_archivo,width=6, height=1, font=('Open Sans', 9), fg="#100E0F", bg="#E7E7E6", cursor='hand2',activebackground='#F3BF7D').place(x=188, y=332)
        tk.Button(self, text="Abrir", command=self.consultar_archivo,width=10, font=('Open Sans', 16,'bold'), fg="#FFFFFF", bg="#35BD6F", cursor='hand2',activebackground="#F2D834").place(x=730, y=400)
        self.actualizar_tabla()

    def verificar_credenciales(self, callback):
        user = f"{self.noCuenta_var.get()}"
        pw = f"{self.password_var.get()}"
        u = busca_users(user)
        p = busca_password(pw)

        if not u or not p:
            mb.showerror("Error", "Usuario o contraseña erróneos")
        elif u[0][1] and p[0][2]:
            self.usuario_activo = u[0][1]  # Guarda el nombre del usuario activo
            self.cuenta_id = u[0][0]  # Guarda el ID del usuario activo
            mb.showinfo("Éxito", f"Bienvenido {self.usuario_activo}")
            callback()

    def verificacion_nuevo(self):
        self.verificar_credenciales(self.guardar_nuevo)

    def verificacion_actualizar(self):
        self.verificar_credenciales(self.actualizar_registro)

    def verificacion_eliminar(self):
        self.verificar_credenciales(self.eliminar_registro)

    def guardar_nuevo(self):
        datos = Control(
            Cuenta_id=self.cuenta_id,
            Clave=self.clave_var.get(),
            Fecha=self.fecha_var.get(),
            Material=self.material_name_var.get() if self.material_data else None,
        )
        if all([datos.Cuenta_id, datos.Clave, datos.Fecha, datos.Material]):
            nuevo(datos)
            self.actualizar_tabla()
            self.material_data = None  # Resetear después de guardar    
        else:
            mb.showwarning("Advertencia", "Faltan datos")
        self.limpiar_campos()

    def actualizar_registro(self):
        if not hasattr(self, 'registro_id'): # Verifica si se ha seleccionado un registro
            mb.showwarning("Advertencia", "Seleccione un registro para editar")
            return

        control = Control(
            Cuenta_id = self.cuenta_id,
            Clave = self.clave_var.get(),
            Fecha = self.fecha_var.get(),
            Material = self.material_data   
        )
        editar(control, self.registro_id)
        self.actualizar_tabla()
        self.limpiar_campos()

    def eliminar_registro(self):
        if not hasattr(self, 'registro_id'):
            mb.showwarning("Advertencia", "Seleccione un registro para eliminar")
            return
        eliminar(self.registro_id)
        self.actualizar_tabla()
        self.limpiar_campos()

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for fila in listar():
            self.tabla.insert('', tk.END, values=fila)

    def cargar_datos_tabla(self, event):
        item = self.tabla.focus()
        valores = self.tabla.item(item, 'values')
        if valores:
            self.registro_id = valores[0]  # Guarda ID
            self.clave_var.set(valores[1]) # 
            self.fecha_var.set(valores[2])
            self.material_name_var.set(valores[3])

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename()
        if archivo:
            try:
                files_folder = os.path.join(os.getcwd(), "files") # Carpeta 'files' en el directorio actual
                if not os.path.exists(files_folder): # Crear carpeta si no existe
                    os.makedirs(files_folder)
                dest_path = os.path.join(files_folder, os.path.basename(archivo)) # Ruta destino
                shutil.copy2(archivo, dest_path) # Copiar archivo
                self.material_data = dest_path  # Guarda la ruta completa en 'files'
                self.material_name_var.set(os.path.basename(archivo))  # Muestra solo el nombre
                mb.showinfo("Archivo cargado", f"Guardado en: {dest_path}")
            except Exception as e:
                self.material_data = None
                mb.showerror("Error", str(e))
    
    def mostrar_registros(self):
        if self.noCuenta_var.get() == "":
            mb.showwarning("Advertencia", "Ingresa el No. de cuenta si deseas ver los registros realizados por esa cuenta!")
            return

    def consultar_archivo(self):
        if not hasattr(self, 'registro_id'):
            mb.showwarning("Advertencia", "Seleccione un registro para consultar")
            return
        item = self.tabla.focus() # Obtiene el item seleccionado
        valores = self.tabla.item(item, 'values')

        if valores and valores[3]: # Verifica que haya un archivo asociado
            nombre_archivo = valores[3]  # Debe ser la ruta completa en 'files'

            carpetas_files = os.path.join(os.getcwd(), "files") # Carpeta 'files' en el directorio actual
            ruta_completa = os.path.join(carpetas_files, nombre_archivo)

            if os.path.exists(ruta_completa):
                try:
                    subprocess.Popen(f'explorer "{ruta_completa}"')  # Abre el archivo con la aplicación predeterminada
                    self.after(2000, lambda: pyautogui.hotkey('alt','tab'))  # Espera a que se abra el archivo
                    pyautogui.hotkey('ctrl','f')  # Abre la función de búsqueda
                    self.after(500, lambda: pyautogui.typewrite(nombre_archivo))  # Escribe el nombre del archivo

                    pyautogui.press('enter')  # Presiona Enter para buscar
                except Exception as e:
                    mb.showerror("Error", f"No se pudo abrir el archivo: {e}")
            else:
                mb.showwarning("Advertencia", "El archivo no existe en la ruta guardada")
        else:
            mb.showwarning("Advertencia", "No hay archivo asociado a este registro")
        self.limpiar_campos()
    
    def buscar_por_cuenta(self):
        nocuenta = self.noCuenta_var.get().strip()
        if not nocuenta:
            mb.showwarning("Advertencia", "Ingrese un No. de cuenta para buscar")
            return
        resultados = buscar_material(nocuenta)
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        if resultados:
            for fila in resultados:
                self.tabla.insert('', tk.END, values=fila)
        else:
            mb.showinfo("Resultados", "No se encontraron registros para este No. de cuenta")


    def limpiar_campos(self): 
        self.clave_var.set("") # Limpia campo clave
        self.fecha_var.set(datetime.now().strftime('%Y-%m-%d')) # Limpia campo fecha
        self.material_name_var.set("") # Limpia campo material
        self.noCuenta_var.set("") # Limpia campo noCuenta
        self.password_var.set("") # Limpia campo password
        self.material_data = None # Limpia variable material_data

def barra_menu(Root):
    barra_menu = tk.Menu(Root)
    Root.config(menu = barra_menu, width=300, height=300)
