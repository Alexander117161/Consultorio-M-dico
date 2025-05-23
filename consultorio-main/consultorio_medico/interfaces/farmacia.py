import customtkinter as ctk
from tkinter import messagebox
import tkinter.ttk as ttk
from utils.json_utils import leer_json, guardar_json

class GestionFarmaciaFrame(ctk.CTkFrame):
    def __init__(self, master, controller=None, usuario=None):
        super().__init__(master)
        self.controller = controller
        self.usuario = usuario
        self.medicamentos = leer_json("medicamentos.json", [])

        self.create_widgets()
        self.actualizar_lista()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Registro de Medicamentos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=10, pady=10, fill='x')

        ctk.CTkLabel(form_frame, text="Nombre:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.entry_nombre = ctk.CTkEntry(form_frame, width=200)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Cantidad en stock:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.entry_stock = ctk.CTkEntry(form_frame, width=200)
        self.entry_stock.grid(row=1, column=1, padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Cantidad mínima para alerta:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.entry_alerta = ctk.CTkEntry(form_frame, width=200)
        self.entry_alerta.grid(row=2, column=1, padx=5, pady=2)

        self.btn_registrar = ctk.CTkButton(form_frame, text="Registrar/Actualizar medicamento", command=self.registrar_medicamento)
        self.btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("Nombre", "Stock", "Alerta"), show='headings')
        for col in ("Nombre", "Stock", "Alerta"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.btn_regresar_menu = ctk.CTkButton(self, text="Regresar al menú", command=self.volver_menu_principal)
        self.btn_regresar_menu.pack(pady=10)

    def registrar_medicamento(self):
        nombre = self.entry_nombre.get().strip()
        stock = self.entry_stock.get().strip()
        alerta = self.entry_alerta.get().strip()

        if not nombre or not stock.isdigit() or not alerta.isdigit():
            messagebox.showerror("Error", "Debe ingresar datos válidos.")
            return

        stock = int(stock)
        alerta = int(alerta)

        medicamento_existente = next((m for m in self.medicamentos if m["nombre"].lower() == nombre.lower()), None)

        if medicamento_existente:
            medicamento_existente["stock"] = stock
            medicamento_existente["alerta"] = alerta
        else:
            self.medicamentos.append({
                "nombre": nombre,
                "stock": stock,
                "alerta": alerta
            })

        guardar_json("medicamentos.json", self.medicamentos)
        messagebox.showinfo("Éxito", f"Medicamento {nombre} registrado/actualizado.")
        self.limpiar_campos()
        self.actualizar_lista()
        self.checar_alertas()

    def limpiar_campos(self):
        self.entry_nombre.delete(0, ctk.END)
        self.entry_stock.delete(0, ctk.END)
        self.entry_alerta.delete(0, ctk.END)

    def actualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in self.medicamentos:
            self.tree.insert('', 'end', values=(m["nombre"], m["stock"], m["alerta"]))

    def checar_alertas(self):
        alertas = [m for m in self.medicamentos if m["stock"] <= m["alerta"]]
        if alertas:
            meds = ", ".join([m["nombre"] for m in alertas])
            messagebox.showwarning("Alerta de stock bajo", f"Los siguientes medicamentos tienen bajo stock: {meds}")

    def volver_menu_principal(self):
        from interfaces.menu_principal import MenuPrincipal
        self.destroy()
        menu = MenuPrincipal(self.master, self.controller, self.usuario)
        menu.pack(fill="both", expand=True)

