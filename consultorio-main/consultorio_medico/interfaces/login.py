import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import requests
from io import BytesIO
import json
import os
from interfaces.registro_usuario import RegistroUsuario

usuarios_FILE = "usuarios.json"

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master

        self.label_title = ctk.CTkLabel(self, text="Inicio de Sesión", font=("Arial", 24))
        self.label_title.pack(pady=(30, 10))

        try:
            url = "https://manprec.com/cdn/shop/articles/texto20.jpg?v=1572284555"
            response = requests.get(url)
            imagen_pil = Image.open(BytesIO(response.content))

            self.imagen = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(300, 200))

            self.label_imagen = ctk.CTkLabel(self, image=self.imagen, text="")
            self.label_imagen.pack(pady=10)
        except Exception as e:
            print("Error al cargar imagen:", e)

        # Campo usuario
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario", width=300)
        self.entry_user.pack(pady=10)

        # Campo contraseña
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=300)
        self.entry_pass.pack(pady=10)

        # Botón iniciar sesión
        self.btn_login = ctk.CTkButton(self, text="Iniciar Sesión", command=self.validar_credenciales)
        self.btn_login.pack(pady=20)

        self.boton_registro = ctk.CTkButton(self, text="Registrarse", command=self.abrir_registro)
        self.boton_registro.pack(pady=(0, 20))

    def validar_credenciales(self):
        usuario = self.entry_user.get().strip()
        contraseña = self.entry_pass.get().strip()

        if not os.path.exists(usuarios_FILE):
            messagebox.showerror("Error", "No hay usuarios registrados.")
            return

        with open(usuarios_FILE, "r") as file:
            usuarios = json.load(file)

        if usuario in usuarios and usuarios[usuario] == contraseña:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {usuario}!")
            self.controller.mostrar_menu_principal(usuario)  # << PASA el nombre
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def abrir_registro(self):
        self.destroy()
        registro = RegistroUsuario(self.master, self.controller)
        registro.pack(fill="both", expand=True)
