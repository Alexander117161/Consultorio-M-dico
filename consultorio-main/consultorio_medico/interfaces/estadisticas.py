import os
import json
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from collections import Counter

class EstadisticasFrame(ctk.CTkFrame):
    def __init__(self, master=None, controller=None, usuario=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.usuario = usuario

        ctk.CTkLabel(self, text="Estadísticas e Informes", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        self.texto_estadisticas = ctk.CTkTextbox(self, width=700, height=400)
        self.texto_estadisticas.pack(padx=20, pady=10)

        btn_cargar = ctk.CTkButton(self, text="Cargar Estadísticas", command=self.cargar_y_mostrar_estadisticas)
        btn_cargar.pack(pady=10)

        self.btn_regresar_menu = ctk.CTkButton(self, text="Regresar al menú", command=self.volver_menu_principal)
        self.btn_regresar_menu.pack(pady=10)

    def cargar_y_mostrar_estadisticas(self):
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        ruta_pacientes = os.path.join(BASE_DIR, "base_datos", "pacientes.csv")
        ruta_atenciones = os.path.join(BASE_DIR, "base_datos", "atenciones.csv")
        ruta_medicamentos = os.path.join(BASE_DIR, "medicamentos.json")

        try:
            pacientes = pd.read_csv(ruta_pacientes)
            # Ajustar nombres columnas si es necesario
            pacientes.columns = ['CURP', 'Nombre', 'ApellidoPaterno', 'ApellidoMaterno', 'Edad', 'Sexo', 'Comunidad']
            atenciones = pd.read_csv(ruta_atenciones)
            with open(ruta_medicamentos, 'r', encoding='utf-8') as f:
                medicamentos = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los archivos:\n{e}")
            return

        self.texto_estadisticas.delete("0.0", "end")

        # Normalizar CURP para evitar problemas por espacios o mayúsculas/minúsculas
        curps_atendidos = atenciones['CURP'].dropna().str.strip().str.upper().unique()
        pacientes['CURP'] = pacientes['CURP'].str.strip().str.upper()

        # Filtrar pacientes que están en el archivo de pacientes y fueron atendidos
        pacientes_atendidos = pacientes[pacientes['CURP'].isin(curps_atendidos)]

        self.texto_estadisticas.insert("end", f"Número de pacientes atendidos: {len(pacientes_atendidos)}\n\n")

        self.texto_estadisticas.insert("end", "Pacientes atendidos:\n")
        for _, row in pacientes_atendidos.iterrows():
            nombre_completo = f"{row['Nombre']} {row['ApellidoPaterno']} {row['ApellidoMaterno']}"
            datos = f"{nombre_completo} - Edad: {row['Edad']}, Sexo: {row['Sexo']}, Comunidad: {row['Comunidad']}"
            self.texto_estadisticas.insert("end", f"{datos}\n")
        self.texto_estadisticas.insert("end", "\n")

        # --- Enfermedades más frecuentes ---
        # Primero, aseguramos que la columna 'Síntomas' existe y limpiamos espacios
        if 'Síntomas' in atenciones.columns:
            sintomas_raw = atenciones['Síntomas'].dropna().astype(str).str.lower()
            # Separar posibles múltiples síntomas por coma
            sintomas_separados = sintomas_raw.str.split(r',\s*')
            # Aplanar la lista y limpiar espacios extras
            lista_sintomas = [s.strip() for sublist in sintomas_separados for s in sublist if s.strip() != '']
            # Contar ocurrencias
            conteo_sintomas = Counter(lista_sintomas)

            # Mostrar resultados
            self.texto_estadisticas.insert("end", "Enfermedades más frecuentes:\n")
            for enfermedad, cantidad in conteo_sintomas.most_common():
                self.texto_estadisticas.insert("end", f"{enfermedad.title()}: {cantidad} veces atendido\n")
            self.texto_estadisticas.insert("end", "\n")
        else:
            self.texto_estadisticas.insert("end", "No se encontró la columna 'Síntomas' en atenciones.csv\n\n")



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
