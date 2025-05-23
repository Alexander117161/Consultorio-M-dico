import customtkinter as ctk
from tkinter import messagebox
import csv
import os
from datetime import datetime

# RUTAS ABSOLUTAS desde el archivo actual
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACIENTES_FILE = os.path.join(BASE_DIR, "base_datos", "pacientes.csv")
CITAS_FILE = os.path.join(BASE_DIR, "base_datos", "citas.csv")
ATENCIONES_FILE = os.path.join(BASE_DIR, "base_datos", "atenciones.csv")

class ModuloAtencionMedica(ctk.CTkFrame):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent)
        self.controller = controller
        self.master = parent
        self.usuario = usuario

        ctk.CTkLabel(self, text="Módulo de Atención Médica", font=("Arial", 22)).pack(pady=20)

        self.entry_curp = ctk.CTkEntry(self, placeholder_text="Ingresa CURP del paciente")
        self.entry_curp.pack(pady=10)

        ctk.CTkButton(self, text="Buscar cita del día", command=self.buscar_cita).pack(pady=5)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(pady=10, padx=10, fill="x")

        self.text_sintomas = ctk.CTkEntry(self, placeholder_text="Síntomas")
        self.text_diagnostico = ctk.CTkEntry(self, placeholder_text="Diagnóstico")
        self.text_tratamiento = ctk.CTkEntry(self, placeholder_text="Tratamiento")
        self.text_peso = ctk.CTkEntry(self, placeholder_text="Peso (kg)")
        self.text_talla = ctk.CTkEntry(self, placeholder_text="Talla (cm)")

        self.boton_guardar = ctk.CTkButton(self, text="Guardar atención", command=self.guardar_atencion, state="disabled")
        self.boton_guardar.pack(pady=15)

        ctk.CTkButton(self, text="Volver al menú", command=self.volver_al_menu).pack(pady=10)

        self.cita_encontrada = None

    def buscar_cita(self):
        curp = self.entry_curp.get().strip().upper()
        hoy = datetime.now().strftime("%Y-%m-%d")

        with open(CITAS_FILE, "r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if fila['CURP'].strip().upper() == curp and fila['Fecha'] == hoy:
                    self.cita_encontrada = fila
                    self.mostrar_info_paciente(fila)
                    return

        messagebox.showinfo("Sin cita", "No se encontró una cita para hoy con ese CURP.")

    def mostrar_info_paciente(self, cita):
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        nombre_completo = f"{cita['Nombre']} {cita.get('Apellidop', '')} {cita.get('Apellidom', '')}"
        info = f"Paciente: {nombre_completo}\nSexo: {cita['Sexo']}\nEdad: {cita['Edad']}\nHora: {cita['Hora']}"
        ctk.CTkLabel(self.info_frame, text=info, justify="left").pack(padx=10, pady=5)

        self.text_sintomas.pack(pady=5)
        self.text_diagnostico.pack(pady=5)
        self.text_tratamiento.pack(pady=5)
        self.text_peso.pack(pady=5)
        self.text_talla.pack(pady=5)
        self.boton_guardar.configure(state="normal")

    def guardar_atencion(self):
        if not self.cita_encontrada:
            return

        sintomas = self.text_sintomas.get().strip()
        diagnostico = self.text_diagnostico.get().strip()
        tratamiento = self.text_tratamiento.get().strip()
        peso = self.text_peso.get().strip()
        talla = self.text_talla.get().strip()

        if not (sintomas and diagnostico and tratamiento and peso and talla):
            messagebox.showerror("Campos incompletos", "Por favor llena todos los campos.")
            return

        nombre_completo = f"{self.cita_encontrada['Nombre']} {self.cita_encontrada.get('Apellidop', '')} {self.cita_encontrada.get('Apellidom', '')}"

        registro = {
            "CURP": self.cita_encontrada['CURP'],
            "Nombre": nombre_completo,
            "Sexo": self.cita_encontrada['Sexo'],
            "Edad": self.cita_encontrada['Edad'],
            "Fecha": self.cita_encontrada['Fecha'],
            "Hora": self.cita_encontrada['Hora'],
            "Peso": peso,
            "Talla": talla,
            "Síntomas": sintomas,
            "Diagnóstico": diagnostico,
            "Tratamiento": tratamiento,
            "Registrado_por": self.usuario
        }

        archivo_existe = os.path.exists(ATENCIONES_FILE)

        with open(ATENCIONES_FILE, "a", newline="", encoding="utf-8") as archivo:
            fieldnames = list(registro.keys())
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            if not archivo_existe:
                writer.writeheader()
            writer.writerow(registro)

        messagebox.showinfo("Guardado", "Atención registrada correctamente.")
        self.text_sintomas.delete(0, 'end')
        self.text_diagnostico.delete(0, 'end')
        self.text_tratamiento.delete(0, 'end')
        self.text_peso.delete(0, 'end')
        self.text_talla.delete(0, 'end')
        self.boton_guardar.configure(state="disabled")

    def volver_al_menu(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)
