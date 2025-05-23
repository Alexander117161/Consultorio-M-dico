import customtkinter as ctk
from tkinter import messagebox
import csv
import os
from datetime import datetime

ATENCIONES_FILE = "base_datos/atenciones.csv"
PACIENTES_FILE = "base_datos/pacientes.csv"

class RecetaMedica(ctk.CTkFrame):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent)
        self.controller = controller
        self.master = parent
        self.usuario = usuario

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=40, fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(10, 5))

        self.buap_logo_label = ctk.CTkLabel(self.header_frame, text="BUAP", font=("Arial", 28, "bold"))
        self.buap_logo_label.pack(side="left", padx=(20, 0))

        ctk.CTkLabel(self.header_frame, text="Benemérita Universidad Autónoma De Puebla", font=("Arial", 18, "bold")).pack(side="left", expand=True, padx=20)

        ctk.CTkFrame(self.main_frame, height=2, fg_color="gray").pack(fill="x", pady=5)

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=10)

        self.left_content_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.left_content_frame.pack(side="left", fill="y", padx=(0, 20))

        ctk.CTkLabel(self.left_content_frame, text="NOMBRE\nDEL PACIENTE", justify="left").pack(anchor="nw", pady=(0, 10))
        self.patient_name_label = ctk.CTkLabel(self.left_content_frame, text="[Nombre del Paciente]", justify="left", font=("Arial", 12, "bold"))
        self.patient_name_label.pack(anchor="nw")

        ctk.CTkLabel(self.left_content_frame, text="FECHA DE LA RECETA", justify="left").pack(anchor="nw", pady=(10, 5))
        self.date_label = ctk.CTkLabel(self.left_content_frame, text="[Fecha]", justify="left")
        self.date_label.pack(anchor="nw")

        ctk.CTkLabel(self.left_content_frame, text="EDAD | SEXO | PESO | TALLA", justify="left").pack(anchor="nw", pady=(10, 5))
        self.details_label = ctk.CTkLabel(self.left_content_frame, text="[Detalles]", justify="left")
        self.details_label.pack(anchor="nw")

        self.right_content_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.right_content_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(self.right_content_frame, text="Descripción", font=("Arial", 12, "bold")).pack(anchor="nw")
        self.description_textbox = ctk.CTkTextbox(self.right_content_frame, height=100, width=400, wrap="word")
        self.description_textbox.pack(fill="x", pady=5)
        self.description_textbox.insert("1.0", "[Detalle de la prescripción]")
        self.description_textbox.configure(state="disabled")

        ctk.CTkLabel(self.right_content_frame, text="[Firma del Médico]", font=("Arial", 12)).pack(anchor="se", pady=(50, 0), padx=20)

        ctk.CTkFrame(self.main_frame, height=2, fg_color="gray").pack(fill="x", pady=5)

        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.footer_frame.pack(fill="x", pady=(5, 10))
        ctk.CTkLabel(self.footer_frame, text="Benemérita Universidad Autónoma De Puebla", font=("Arial", 10)).pack(side="left", padx=20)

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10)
        ctk.CTkLabel(self.input_frame, text="Generar Receta Médica", font=("Arial", 22)).pack(pady=20)
        self.entry_curp = ctk.CTkEntry(self.input_frame, placeholder_text="Ingresa CURP del paciente", width=300)
        self.entry_curp.pack(pady=10)
        ctk.CTkButton(self.input_frame, text="Buscar última atención", command=self.generar_receta).pack(pady=10)
        ctk.CTkButton(self.input_frame, text="Volver al menú", command=self.volver_al_menu).pack(pady=10)

        ctk.CTkButton(self.input_frame, text="Guardar receta", command=self.guardar_receta).pack(pady=10)

    def generar_receta(self):
        curp = self.entry_curp.get().strip().upper()
        if not os.path.exists(ATENCIONES_FILE):
            messagebox.showerror("Error", "No hay registros de atención médica.")
            return

        with open(ATENCIONES_FILE, "r", encoding="utf-8") as archivo:
            reader = list(csv.DictReader(archivo))
            atenciones = [r for r in reader if r["CURP"].strip().upper() == curp]

        if not atenciones:
            messagebox.showinfo("Sin resultados", "No se encontró atención médica para ese CURP.")
            self._clear_recipe_fields()
            return

        ultima = atenciones[-1]

        nombre = ultima.get("Nombre", "")

        apellidop = ""
        apellidom = ""
        if os.path.exists(PACIENTES_FILE):
            with open(PACIENTES_FILE, "r", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    if fila['CURP'] == curp:
                        apellidop = fila.get("Apellidop", "")
                        apellidom = fila.get("Apellidom", "")
                        break

        nombre_completo = f"{nombre} {apellidop} {apellidom}".strip()
        edad = ultima.get("Edad", "-")
        sexo = ultima.get("Sexo", "-")
        peso = ultima.get("Peso", "-")
        talla = ultima.get("Talla", "-")
        sintomas = ultima.get("Síntomas", "-")
        diagnostico = ultima.get("Diagnóstico", "-")
        tratamiento = ultima.get("Tratamiento", "-")

        self.patient_name_label.configure(text=nombre_completo)
        self.date_label.configure(text=f"Fecha: {ultima['Fecha']}")
        self.details_label.configure(text=f"{edad} años | {sexo} | {peso} kg | {talla} cm")

        self.description_textbox.configure(state="normal")
        self.description_textbox.delete("1.0", "end")
        self.description_textbox.insert("1.0", f"Síntomas: {sintomas}\nDiagnóstico: {diagnostico}\nTratamiento: {tratamiento}")
        self.description_textbox.configure(state="disabled")


    def _clear_recipe_fields(self):
        self.patient_name_label.configure(text="[Nombre del Paciente]")
        self.date_label.configure(text="[Fecha]")
        self.details_label.configure(text="[Detalles]")
        self.description_textbox.configure(state="normal")
        self.description_textbox.delete("1.0", "end")
        self.description_textbox.insert("1.0", "[Detalle de la prescripción]")
        self.description_textbox.configure(state="disabled")

    def guardar_receta(self):
        texto = self.description_textbox.get("1.0", "end").strip()
        nombre = self.patient_name_label.cget("text")
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_nombre = f"receta_{nombre.replace(' ', '_')}_{fecha}.txt"

        try:
            with open(archivo_nombre, "w", encoding="utf-8") as archivo:
                archivo.write(f"Receta Médica - {nombre}\n\n")
                archivo.write(f"{self.date_label.cget('text')}\n")
                archivo.write(f"{self.details_label.cget('text')}\n\n")
                archivo.write(texto)
            messagebox.showinfo("Éxito", f"Receta guardada como {archivo_nombre}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la receta: {e}")


    def volver_al_menu(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)