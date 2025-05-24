import customtkinter as ctk
from tkinter import messagebox
from .personal import Personal
from utils import json_utils

class GestionPersonalFrame(ctk.CTkFrame):
    def __init__(self, master=None, gestion_personal=None, controller=None, usuario=None, **kwargs):
        super().__init__(master, **kwargs)
        self.gestion_personal = gestion_personal or Personal()
        self.gestion_personal.medicos = json_utils.leer_json("medicos.json", [])
        self.gestion_personal.asistentes = json_utils.leer_json("asistentes.json", [])

        self.controller = controller  
        self.usuario = usuario  

        self.create_widgets()
        self.actualizar_listas()

    def create_widgets(self):
        self.frm_medico = ctk.CTkFrame(self)
        self.frm_medico.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(self.frm_medico, text="Registrar Médico", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        ctk.CTkLabel(self.frm_medico, text="Nombre:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.entry_medico_nombre = ctk.CTkEntry(self.frm_medico, width=250)
        self.entry_medico_nombre.grid(row=1, column=1, padx=5, pady=2)

        ctk.CTkLabel(self.frm_medico, text="Especialidad:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.entry_medico_esp = ctk.CTkEntry(self.frm_medico, width=250)
        self.entry_medico_esp.grid(row=2, column=1, padx=5, pady=2)

        ctk.CTkLabel(self.frm_medico, text="Horario:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.entry_medico_horario = ctk.CTkEntry(self.frm_medico, width=250)
        self.entry_medico_horario.grid(row=3, column=1, padx=5, pady=2)

        self.btn_registrar_medico = ctk.CTkButton(self.frm_medico, text="Registrar Médico", command=self.registrar_medico)
        self.btn_registrar_medico.grid(row=4, column=0, columnspan=2, pady=10)

        self.frm_asistente = ctk.CTkFrame(self)
        self.frm_asistente.pack(fill='x', padx=10, pady=5)

        ctk.CTkLabel(self.frm_asistente, text="Registrar Asistente", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        ctk.CTkLabel(self.frm_asistente, text="Nombre:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.entry_asistente_nombre = ctk.CTkEntry(self.frm_asistente, width=250)
        self.entry_asistente_nombre.grid(row=1, column=1, padx=5, pady=2)

        ctk.CTkLabel(self.frm_asistente, text="Horario:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.entry_asistente_horario = ctk.CTkEntry(self.frm_asistente, width=250)
        self.entry_asistente_horario.grid(row=2, column=1, padx=5, pady=2)

        self.btn_registrar_asistente = ctk.CTkButton(self.frm_asistente, text="Registrar Asistente", command=self.registrar_asistente)
        self.btn_registrar_asistente.grid(row=3, column=0, columnspan=2, pady=10)

        import tkinter.ttk as ttk

        self.frm_listados = ctk.CTkFrame(self)
        self.frm_listados.pack(fill='both', expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frm_listados, text="Médicos Registrados:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w')
        self.tree_medicos = ttk.Treeview(self.frm_listados, columns=("ID", "Nombre", "Especialidad", "Horario"), show='headings', height=6)
        for col in ("ID", "Nombre", "Especialidad", "Horario"):
            self.tree_medicos.heading(col, text=col)
            self.tree_medicos.column(col, width=150)
        self.tree_medicos.pack(fill='x', pady=5)

        ctk.CTkLabel(self.frm_listados, text="Asistentes Registrados:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w', pady=(10, 0))
        self.tree_asistentes = ttk.Treeview(self.frm_listados, columns=("ID", "Nombre", "Horario"), show='headings', height=6)
        for col in ("ID", "Nombre", "Horario"):
            self.tree_asistentes.heading(col, text=col)
            self.tree_asistentes.column(col, width=150)
        self.tree_asistentes.pack(fill='x', pady=5)

        self.btn_regresar_menu = ctk.CTkButton(self, text="Regresar al menú", command=self.volver_menu_principal)
        self.btn_regresar_menu.pack(pady=10)

    def registrar_medico(self):
        nombre = self.entry_medico_nombre.get().strip()
        especialidad = self.entry_medico_esp.get().strip()
        horario = self.entry_medico_horario.get().strip()

        if not nombre or not especialidad or not horario:
            messagebox.showerror("Error", "Todos los campos para el médico son obligatorios.")
            return

        self.gestion_personal.registrar_medico(nombre, especialidad, horario)
        json_utils.guardar_json("medicos.json", self.gestion_personal.medicos)
        messagebox.showinfo("Éxito", f"Médico {nombre} registrado.")
        self.limpiar_campos_medico()
        self.actualizar_listas()

    def registrar_asistente(self):
        nombre = self.entry_asistente_nombre.get().strip()
        horario = self.entry_asistente_horario.get().strip()

        if not nombre or not horario:
            messagebox.showerror("Error", "Todos los campos para el asistente son obligatorios.")
            return

        self.gestion_personal.registrar_asistente(nombre, horario)
        json_utils.guardar_json("asistentes.json", self.gestion_personal.asistentes)
        messagebox.showinfo("Éxito", f"Asistente {nombre} registrado.")
        self.limpiar_campos_asistente()
        self.actualizar_listas()

    def limpiar_campos_medico(self):
        self.entry_medico_nombre.delete(0, ctk.END)
        self.entry_medico_esp.delete(0, ctk.END)
        self.entry_medico_horario.delete(0, ctk.END)

    def limpiar_campos_asistente(self):
        self.entry_asistente_nombre.delete(0, ctk.END)
        self.entry_asistente_horario.delete(0, ctk.END)

    def actualizar_listas(self):
        for i in self.tree_medicos.get_children():
            self.tree_medicos.delete(i)
        for i in self.tree_asistentes.get_children():
            self.tree_asistentes.delete(i)

        for m in self.gestion_personal.listar_medicos():
            self.tree_medicos.insert('', 'end', values=(m['id'], m['nombre'], m['especialidad'], m['horario']))
        for a in self.gestion_personal.listar_asistentes():
            self.tree_asistentes.insert('', 'end', values=(a['id'], a['nombre'], a['horario']))

    def volver_menu_principal(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)
