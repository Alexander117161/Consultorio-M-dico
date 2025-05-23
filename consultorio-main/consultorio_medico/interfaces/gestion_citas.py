import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
import csv
import os
from datetime import datetime

CITAS_FILE = "base_datos/citas.csv"
PACIENTES_FILE = "base_datos/pacientes.csv"

class AgendarCita(ctk.CTkFrame):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent)
        self.controller = controller
        self.master = parent
        self.usuario = usuario
        self.horario_seleccionado = None
        self.fecha_seleccionada = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text=f"HOLA {self.usuario.upper()}", font=("Arial", 22)).grid(row=0, column=0, columnspan=2, pady=20)

        self.frame_izquierdo = ctk.CTkFrame(self)
        self.frame_izquierdo.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        ctk.CTkLabel(self.frame_izquierdo, text="Seleccione un día", font=("Arial", 18, "bold")).pack(pady=10)

        self.calendario = Calendar(self.frame_izquierdo, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendario.pack(pady=10)

        ctk.CTkButton(self.frame_izquierdo, text="Ver horarios disponibles", command=self.mostrar_horarios).pack(pady=10)

        self.frame_horarios = ctk.CTkFrame(self.frame_izquierdo)
        self.frame_horarios.pack(pady=10)

        self.frame_derecho = ctk.CTkFrame(self)
        self.frame_derecho.grid(row=1, column=1, padx=20, pady=10, sticky="n")

        ctk.CTkLabel(self.frame_derecho, text="Confirmar Cita", font=("Arial", 18, "bold")).pack(pady=10)

        self.label_cita = ctk.CTkLabel(self.frame_derecho, text="Selecciona un horario", font=("Arial", 14))
        self.label_cita.pack(pady=5)

        self.entry_curp = ctk.CTkEntry(self.frame_derecho, placeholder_text="CURP del paciente")
        self.entry_curp.pack(pady=5)

        self.entry_gmail = ctk.CTkEntry(self.frame_derecho, placeholder_text="Tu correo Gmail")
        self.entry_gmail.pack(pady=5)

        self.entry_motivo = ctk.CTkEntry(self.frame_derecho, placeholder_text="Motivo de la cita (opcional)")
        self.entry_motivo.pack(pady=5)

        self.boton_confirmar = ctk.CTkButton(self.frame_derecho, text="Confirmar cita", command=self.confirmar_cita)
        self.boton_confirmar.pack(pady=10)

        ctk.CTkButton(self, text="Regresar al menú", command=self.volver_al_menu).grid(row=2, column=0, columnspan=2, pady=20)

    def mostrar_horarios(self):
        for widget in self.frame_horarios.winfo_children():
            widget.destroy()

        self.fecha_seleccionada = self.calendario.get_date()
        fecha_obj = datetime.strptime(self.fecha_seleccionada, "%Y-%m-%d")
        dia_semana = fecha_obj.weekday()

        if dia_semana < 5:
            horarios_disponibles = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]
        elif dia_semana == 5:
            horarios_disponibles = ["09:00", "10:00", "11:00"]
        else:
            ctk.CTkLabel(self.frame_horarios, text="No hay citas disponibles los domingos.").pack(pady=10)
            return

        horarios_ocupados = self.obtener_horarios_ocupados(self.fecha_seleccionada)

        for hora in horarios_disponibles:
            color = "red" if hora in horarios_ocupados else "white"
            boton = ctk.CTkButton(
                self.frame_horarios,
                text=hora,
                fg_color=color,
                text_color="black",
                state="disabled" if hora in horarios_ocupados else "normal",
                command=lambda h=hora: self.seleccionar_horario(h, self.fecha_seleccionada)
            )
            boton.pack(pady=5, padx=20, fill="x")

    def obtener_horarios_ocupados(self, fecha):
        ocupados = []
        if os.path.exists(CITAS_FILE):
            with open(CITAS_FILE, "r", newline="", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    if fila['Fecha'] == fecha:
                        ocupados.append(fila['Hora'])
        return ocupados

    def seleccionar_horario(self, hora, fecha):
        self.horario_seleccionado = hora
        self.fecha_seleccionada = fecha
        self.label_cita.configure(text=f"Cita: {fecha} a las {hora}")

    def confirmar_cita(self):
        curp = self.entry_curp.get().strip().upper()
        correo = self.entry_gmail.get().strip()
        motivo = self.entry_motivo.get().strip()

        if not curp or not correo:
            messagebox.showerror("Campos incompletos", "Debes ingresar CURP y Gmail.")
            return

        if not correo.endswith("@gmail.com"):
            messagebox.showerror("Correo inválido", "Ingresa un correo válido de Gmail.")
            return

        if not self.horario_seleccionado or not self.fecha_seleccionada:
            messagebox.showerror("Falta información", "Selecciona un horario disponible.")
            return

        paciente = self.buscar_paciente_por_curp(curp)
        if not paciente:
            messagebox.showerror("CURP no encontrado", "No existe un paciente registrado con ese CURP.")
            return

        cita = {
            "Usuario": self.usuario,
            "Fecha": self.fecha_seleccionada,
            "Hora": self.horario_seleccionado,
            "Gmail": correo,
            "CURP_Paciente": curp,
            "Nombre_Paciente": paciente["Nombre"],
            "Sexo": paciente["Sexo"],
            "Edad": paciente["Edad"],
            "Motivo": motivo
        }

        archivo_existe = os.path.exists(CITAS_FILE)

        with open(CITAS_FILE, "a", newline="", encoding="utf-8") as archivo:
            fieldnames = ["Usuario", "Fecha", "Hora", "Gmail", "CURP_Paciente", "Nombre_Paciente", "Sexo", "Edad", "Motivo"]
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            if not archivo_existe:
                writer.writeheader()
            writer.writerow(cita)

        messagebox.showinfo("Cita confirmada", "Tu cita ha sido registrada con éxito.")
        self.entry_curp.delete(0, 'end')
        self.entry_gmail.delete(0, 'end')
        self.entry_motivo.delete(0, 'end')
        self.label_cita.configure(text="Selecciona un horario")
        self.horario_seleccionado = None

    def buscar_paciente_por_curp(self, curp):
        if os.path.exists(PACIENTES_FILE):
            with open(PACIENTES_FILE, "r", newline="", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    if fila["CURP"].strip().upper() == curp:
                        return fila
        return None

    def volver_al_menu(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)
