import customtkinter as ctk
from tkinter import messagebox
import csv
import os
from tkcalendar import Calendar
from datetime import datetime

CITAS_FILE = "base_datos/citas.csv"

class EditarCitasUsuario(ctk.CTkFrame):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent)
        self.controller = controller
        self.master = parent
        self.usuario = usuario

        ctk.CTkLabel(self, text=f"Editar citas de {self.usuario.upper()}", font=("Arial", 22)).pack(pady=20)

        self.lista_citas = ctk.CTkScrollableFrame(self, width=800, height=400)
        self.lista_citas.pack(padx=20, pady=10)

        self.cargar_citas()
        ctk.CTkButton(self, text="Volver al menú", command=self.volver_al_menu).pack(pady=10)

    def cargar_citas(self):
        if not os.path.exists(CITAS_FILE):
            ctk.CTkLabel(self.lista_citas, text="No hay citas registradas.").pack()
            return

        with open(CITAS_FILE, "r", newline="", encoding="utf-8") as archivo:
            reader = list(csv.DictReader(archivo))

        self.citas_usuario = [c for c in reader if c['Usuario'] == self.usuario]

        if not self.citas_usuario:
            ctk.CTkLabel(self.lista_citas, text="No tienes citas registradas.").pack()
            return

        for i, cita in enumerate(self.citas_usuario):
            frame = ctk.CTkFrame(self.lista_citas)
            frame.pack(pady=5, fill="x")

            info = f"{cita['Fecha']} {cita['Hora']} - {cita['Nombre']} ({cita['CURP']})"
            ctk.CTkLabel(frame, text=info).pack(side="left", padx=10)

            editar_btn = ctk.CTkButton(frame, text="Editar", width=80, command=lambda idx=i: self.editar_cita(idx))
            editar_btn.pack(side="left", padx=5)

            eliminar_btn = ctk.CTkButton(frame, text="Eliminar", width=80, fg_color="red", command=lambda idx=i: self.eliminar_cita(idx))
            eliminar_btn.pack(side="left", padx=5)

    def editar_cita(self, idx):
        cita = self.citas_usuario[idx]
        fecha_actual = cita['Fecha']

        ventana = ctk.CTkToplevel(self)
        ventana.title("Editar cita")
        ventana.geometry("350x500")
        ventana.lift()
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Selecciona nueva fecha", font=("Arial", 14)).pack(pady=10)
        calendario = Calendar(ventana, selectmode='day', date_pattern='yyyy-mm-dd')
        calendario.pack(pady=10)

        contenedor_horarios = ctk.CTkScrollableFrame(ventana)
        contenedor_horarios.pack(pady=10, fill="both", expand=True)

        def actualizar_horarios():
            for widget in contenedor_horarios.winfo_children():
                widget.destroy()

            nueva_fecha = calendario.get_date()
            dia = datetime.strptime(nueva_fecha, "%Y-%m-%d").weekday()

            if dia == 6:
                ctk.CTkLabel(contenedor_horarios, text="No hay citas los domingos.").pack(pady=10)
                return

            horarios = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"] if dia < 5 else ["09:00", "10:00", "11:00"]
            ocupados = self.obtener_horarios_ocupados(nueva_fecha, exclude=cita)

            for h in horarios:
                estado = "disabled" if h in ocupados else "normal"
                color = "red" if h in ocupados else "white"

                boton = ctk.CTkButton(
                    contenedor_horarios,
                    text=h,
                    state=estado,
                    fg_color=color,
                    text_color="black",
                    command=lambda hora=h, fecha=nueva_fecha: self.confirmar_edicion(idx, fecha, hora, ventana)
                )
                boton.pack(pady=5, padx=20, fill="x")

        actualizar_horarios()
        calendario.bind("<<CalendarSelected>>", lambda _: actualizar_horarios())

    def obtener_horarios_ocupados(self, fecha, exclude=None):
        ocupados = []
        if os.path.exists(CITAS_FILE):
            with open(CITAS_FILE, "r", newline="", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    if fila['Fecha'] == fecha and fila != exclude:
                        ocupados.append(fila['Hora'])
        return ocupados

    def confirmar_edicion(self, idx, nueva_fecha, nueva_hora, ventana):
        self.citas_usuario[idx]['Fecha'] = nueva_fecha
        self.citas_usuario[idx]['Hora'] = nueva_hora
        self.guardar_citas()
        ventana.destroy()
        messagebox.showinfo("Éxito", "La cita fue actualizada.")
        self.refrescar()

    def eliminar_cita(self, idx):
        if idx < len(self.citas_usuario):
            del self.citas_usuario[idx]
            self.guardar_citas()
            messagebox.showinfo("Éxito", "La cita fue eliminada.")
            self.refrescar()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la cita.")

    def guardar_citas(self):
        campos = ["Usuario", "Fecha", "Hora", "Correo", "CURP", "Nombre", "Sexo", "Edad", "Motivo"]
        todas = []
        if os.path.exists(CITAS_FILE):
            with open(CITAS_FILE, "r", newline="", encoding="utf-8") as archivo:
                todas = list(csv.DictReader(archivo))

        filtradas_usuario = [{k: c[k] for k in campos if k in c} for c in self.citas_usuario]
        nuevas = [c for c in todas if c.get('Usuario') != self.usuario] + filtradas_usuario


        try:
            with open(CITAS_FILE, "w", newline="", encoding="utf-8") as archivo:
                writer = csv.DictWriter(archivo, fieldnames=campos)
                writer.writeheader()
                writer.writerows(nuevas)
        except PermissionError:
            messagebox.showerror("Error", "No se pudo escribir en 'citas.csv'. Asegúrate de que no esté abierto.")

    def refrescar(self):
        for widget in self.lista_citas.winfo_children():
            widget.destroy()
        self.cargar_citas()

    def volver_al_menu(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)
