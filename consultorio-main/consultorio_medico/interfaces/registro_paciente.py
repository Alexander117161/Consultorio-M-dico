import customtkinter as ctk
from tkinter import messagebox
import json
import csv
import os
import re
from utils.validaciones import comunidad_es_valida


def validar_formato_curp(curp):
    patron = r'^[A-Z]{4}\d{6}[HM]{1}[A-Z]{2}[A-Z]{3}[0-9A-Z]{2}$'
    return re.match(patron, curp) is not None

class RegistroPaciente(ctk.CTkFrame):

    def __init__(self, master, controller, usuario):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.usuario = usuario

        ctk.CTkLabel(self, text="Registro de Pacientes", font=("Arial", 22)).pack(pady=20)

        self.entry_curp = ctk.CTkEntry(self, placeholder_text="CURP", width=300)
        self.entry_curp.pack(pady=5)

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre/nombres", width=300)
        self.entry_nombre.pack(pady=5)

        self.entry_apellidop = ctk.CTkEntry(self, placeholder_text="Apellido paterno", width=300)
        self.entry_apellidop.pack(pady=5)

        self.entry_apellidom = ctk.CTkEntry(self, placeholder_text="Apellido materno", width=300)
        self.entry_apellidom.pack(pady=5)

        self.entry_edad = ctk.CTkEntry(self, placeholder_text="Edad", width=300)
        self.entry_edad.pack(pady=5)

        self.label_sexo = ctk.CTkLabel(self, text="Sexo:")
        self.label_sexo.pack(pady=(10, 0))

        self.combo_sexo = ctk.CTkComboBox(self, values=["FEMENINO", "MASCULINO"])
        self.combo_sexo.pack(pady=(0, 10))

        self.entry_comunidad = ctk.CTkEntry(self, placeholder_text="Comunidad", width=300)
        self.entry_comunidad.pack(pady=5)

        ctk.CTkButton(self, text="Registrar", command=self.registrar_paciente).pack(pady=20)

        self.boton_regresar = ctk.CTkButton(self, text="Regresar", command=self.volver_menu_principal)
        self.boton_regresar.pack(pady=(10, 20))

    def registrar_paciente(self):

        curp = self.entry_curp.get().strip().upper()
        if not validar_formato_curp(curp):
            messagebox.showerror("CURP inválido", "El CURP ingresado no tiene un formato válido.")
            return

        nombre = self.entry_nombre.get().strip().upper()
        apellidop = self.entry_apellidop.get().strip().upper()
        apellidom = self.entry_apellidom.get().strip().upper()
        edad = self.entry_edad.get().strip()
        sexo = self.combo_sexo.get().strip().upper()

        comunidad = self.entry_comunidad.get().strip().upper()
        if not comunidad_es_valida(comunidad):
            messagebox.showerror("Error", "La entidad ingresada no es una comunidad válida de Puebla.")
            return

        if not all([curp, nombre, apellidop, apellidom, edad, sexo, comunidad]):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        if not edad.isdigit():
            messagebox.showerror("Edad inválida", "La edad debe ser un número.")
            return

        # RUTA ABSOLUTA SEGURA
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        carpeta_datos = os.path.join(base_dir, "base_datos")
        archivo = os.path.join(carpeta_datos, "pacientes.csv")

        # Crear carpeta si no existe
        os.makedirs(carpeta_datos, exist_ok=True)

        paciente_existente = False

        # Verifica si ya existe ese CURP
        if os.path.exists(archivo):
            with open(archivo, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == curp:
                        paciente_existente = True
                        break

        if paciente_existente:
            messagebox.showerror("CURP duplicado", "Este paciente ya está registrado.")
            return

        # Escribir nuevo paciente
        with open(archivo, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([curp, nombre, apellidop, apellidom, edad, sexo, comunidad])

        messagebox.showinfo("Registro exitoso", f"Paciente {nombre} registrado correctamente.")
        self.entry_curp.delete(0, 'end')
        self.entry_nombre.delete(0, 'end')
        self.entry_apellidop.delete(0, 'end')
        self.entry_apellidom.delete(0, 'end')
        self.entry_edad.delete(0, 'end')
        self.entry_comunidad.delete(0, 'end')

    def volver_menu_principal(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        login = MenuPrincipal(self.master, self.controller, self.usuario)
        login.pack(fill="both", expand=True)
