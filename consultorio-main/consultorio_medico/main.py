import customtkinter as ctk

# Configurar estilo general
ctk.set_appearance_mode("light")   # o "dark"
ctk.set_default_color_theme("blue")  # puedes cambiar a "green", "dark-blue", etc.

# Crear la ventana principal
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión Médica")
        self.geometry("900x800")
        self.resizable(False, False)

        self.mostrar_login()

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        from interfaces.login import LoginScreen
        self.limpiar_pantalla()
        self.login_screen = LoginScreen(self, self)
        self.login_screen.pack(fill="both", expand=True)

    def mostrar_menu_principal(self, usuario):
        from interfaces.menu_principal import MenuPrincipal
        self.limpiar_pantalla()
        self.menu = MenuPrincipal(self, self, usuario)
        self.menu.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
