import customtkinter as ctk
from tkinter import messagebox
import json
import os

USUARIOS_FILE = "usuarios.json"

class RegistroUsuario(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.master = parent

        ctk.CTkLabel(self, text="Registrar nuevo usuario", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Nombre de usuario")
        self.entry_usuario.pack(pady=10)

        self.entry_contraseña = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_contraseña.pack(pady=10)

        ctk.CTkButton(self, text="Guardar usuario", command=self.guardar_usuario).pack(pady=20)
        ctk.CTkButton(self, text="Volver al login", command=self.volver_login).pack()

    def guardar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        contraseña = self.entry_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE, "r") as file:
                usuarios = json.load(file)
        else:
            usuarios = {}

        if usuario in usuarios:
            messagebox.showerror("Error", "Este usuario ya existe.")
            return

        usuarios[usuario] = contraseña

        with open(USUARIOS_FILE, "w") as file:
            json.dump(usuarios, file)

        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        self.volver_login()

    def volver_login(self):
        self.destroy()
        from interfaces.login import LoginScreen
        login = LoginScreen(self.master, self.controller)
        login.pack(fill="both", expand=True)
