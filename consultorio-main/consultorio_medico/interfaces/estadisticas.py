import os
import json
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox

class EstadisticasFrame(ctk.CTkFrame):
    def __init__(self, master=None, controller=None, usuario=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.usuario = usuario

        # Crear título
        ctk.CTkLabel(self, text="Estadísticas e Informes", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Crear textbox para mostrar estadísticas
        self.texto_estadisticas = ctk.CTkTextbox(self, width=700, height=400)
        self.texto_estadisticas.pack(padx=20, pady=10)

        # Botón para cargar estadísticas
        btn_cargar = ctk.CTkButton(self, text="Cargar Estadísticas", command=self.cargar_y_mostrar_estadisticas)
        btn_cargar.pack(pady=10)

        # Botón para regresar al menú
        self.btn_regresar_menu = ctk.CTkButton(self, text="Regresar al menú", command=self.volver_menu_principal)
        self.btn_regresar_menu.pack(pady=10)

    def cargar_y_mostrar_estadisticas(self):
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        ruta_pacientes = os.path.join(BASE_DIR, "base_datos", "pacientes.csv")
        ruta_atenciones = os.path.join(BASE_DIR, "base_datos", "atenciones.csv")
        ruta_medicamentos = os.path.join(BASE_DIR, "medicamentos.json")

        try:
            pacientes = pd.read_csv(ruta_pacientes)
            atenciones = pd.read_csv(ruta_atenciones)
            with open(ruta_medicamentos, 'r', encoding='utf-8') as f:
                medicamentos = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los archivos:\n{e}")
            return

        self.texto_estadisticas.delete("0.0", "end")  # Limpiar texto previo

        # --- Número de pacientes atendidos ---
        pacientes_atendidos = atenciones['CURP'].nunique()
        self.texto_estadisticas.insert("end", f"Número de pacientes atendidos: {pacientes_atendidos}\n\n")

        # Mostrar datos de pacientes atendidos: edad, sexo, comunidad
        pacientes_unicos = pacientes.set_index('CURP').loc[atenciones['CURP'].unique()]
        self.texto_estadisticas.insert("end", "Datos de pacientes atendidos:\n")
        self.texto_estadisticas.insert("end", pacientes_unicos[['Edad', 'Sexo', 'Comunidad']].to_string())
        self.texto_estadisticas.insert("end", "\n\n")

        # --- Enfermedades más frecuentes ---
        # El campo Diagnóstico en atenciones puede tener varios diagnósticos separados por comas
        diagnósticos = atenciones['Diagnóstico'].dropna().str.lower().str.split(r',\s*')
        # Aplanar la lista
        lista_diagnosticos = [diag for sublist in diagnósticos for diag in sublist]
        from collections import Counter
        conteo_enfermedades = Counter(lista_diagnosticos)
        enfermedades_mas_frecuentes = conteo_enfermedades.most_common(10)

        self.texto_estadisticas.insert("end", "Enfermedades más frecuentes:\n")
        for enfermedad, cantidad in enfermedades_mas_frecuentes:
            self.texto_estadisticas.insert("end", f"{enfermedad.title()}: {cantidad}\n")
        self.texto_estadisticas.insert("end", "\n")

        # --- Medicamentos más usados ---
        tratamientos = atenciones['Tratamiento'].dropna().str.lower().str.split(r',\s*')
        lista_tratamientos = [med for sublist in tratamientos for med in sublist]
        conteo_medicamentos = Counter(lista_tratamientos)
        medicamentos_mas_usados = conteo_medicamentos.most_common(10)

        self.texto_estadisticas.insert("end", "Medicamentos más usados:\n")
        for medicamento, cantidad in medicamentos_mas_usados:
            self.texto_estadisticas.insert("end", f"{medicamento.title()}: {cantidad}\n")

    def volver_menu_principal(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)
