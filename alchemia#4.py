import tkinter as tk
from tkinter import ttk, messagebox as mb, filedialog
from PIL import Image, ImageTk
from interface.app import Fr, barra_menu

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PUMA")
    Icono = tk.PhotoImage(file='C:\\Users\\alber\\OneDrive\\Escritorio\\codes\\LabChem\\dabagui_two\\databaGUI\\images\\garra.png')
    root.iconphoto(True, Icono)
    root.resizable(1,1) 
    barra_menu(root)
    app = Fr(root)
    root.mainloop()
