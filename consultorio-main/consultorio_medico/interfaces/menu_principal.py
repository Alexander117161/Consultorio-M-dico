import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
from interfaces.editar_citas_usuario import EditarCitasUsuario
from interfaces.modulo_atencion_medica import ModuloAtencionMedica
from interfaces.receta_medica import RecetaMedica
from interfaces.gestion_personal import GestionPersonalFrame
from interfaces.farmacia import GestionFarmaciaFrame
from interfaces.estadisticas import EstadisticasFrame


class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller, usuario):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.usuario = usuario

        self.label = ctk.CTkLabel(self, text="Menú Principal", font=("Arial", 24))
        self.label.pack(pady=(30, 10))

        # Cargar y mostrar la imagen desde URL
        try:
            url = "https://garcialawfirmtj.com/wp-content/uploads/2019/05/Screen-Shot-2019-05-15-at-7.29.19-PM-1.png"
            response = requests.get(url)
            imagen_pil = Image.open(BytesIO(response.content))
            imagen_pil = imagen_pil.resize((400, 200))  # Ajusta el tamaño

            self.imagen = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(400, 200))
            self.label_imagen = ctk.CTkLabel(self, image=self.imagen, text="")
            self.label_imagen.pack(pady=10)
        except Exception as e:
            print("Error al cargar imagen:", e)

        # Botones del menú
        self.btn_registro = ctk.CTkButton(self, text="Registro de Pacientes", width=250, command=self.abrir_registro)
        self.btn_registro.pack(pady=10)

        self.btn_citas = ctk.CTkButton(self, text="Agendar Cita", width=250, command=self.abrir_gestion_citas)
        self.btn_citas.pack(pady=10)

        self.btn_editar_citas = ctk.CTkButton(self, text="Editar mis citas", command=self.abrir_editar_citas)
        self.btn_editar_citas.pack(pady=10)

        self.btn_atencion = ctk.CTkButton(self, text="Módulo de Atención Médica", width=250, command=self.abrir_atencion_medica)
        self.btn_atencion.pack(pady=10)

        self.boton_receta = ctk.CTkButton(self, text="Receta médica", command=self.abrir_receta_medica)
        self.boton_receta.pack(pady=10)

        self.btn_gestion_personal = ctk.CTkButton(self, text="Gestión de Médicos y Personal", width=250, command=self.abrir_gestion_personal)
        self.btn_gestion_personal.pack(pady=10)

        self.btn_farmacia = ctk.CTkButton(self, text="Farmacia y Stock", width=250, command=self.abrir_farmacia)
        self.btn_farmacia.pack(pady=10)

        self.btn_estadisticas = ctk.CTkButton(self, text="Estadísticas e Informes", width=250, command=self.abrir_estadisticas)
        self.btn_estadisticas.pack(pady=10)

        self.btn_salir = ctk.CTkButton(self, text="Cerrar Sesión", command=self.volver_login, width=250)
        self.btn_salir.pack(pady=30)

    def abrir_registro(self):
        from interfaces.registro_paciente import RegistroPaciente
        self.destroy()
        registro = RegistroPaciente(self.master, self.controller, self.usuario)
        registro.pack(fill="both", expand=True)

    def abrir_gestion_citas(self):
        from interfaces.gestion_citas import AgendarCita
        self.destroy()
        cita = AgendarCita(self.master, self.controller, self.usuario)
        cita.pack(fill="both", expand=True)

    def abrir_editar_citas(self):
        self.destroy()
        vista = EditarCitasUsuario(self.master, self.controller, self.usuario)
        vista.pack(fill="both", expand=True)

    def abrir_atencion_medica(self):
        self.destroy()
        vista = ModuloAtencionMedica(self.master, self.controller, self.usuario)
        vista.pack(fill="both", expand=True)

    def abrir_receta_medica(self):
        self.destroy()
        vista = RecetaMedica(self.master, self.controller, self.usuario)
        vista.pack(fill="both", expand=True)

    def volver_login(self):
        from interfaces.login import LoginScreen
        self.destroy()
        login = LoginScreen(self.master, self.controller)
        login.pack(fill="both", expand=True)

    def abrir_gestion_personal(self):
        self.destroy()
        from .personal import Personal
        gestion_personal = Personal()
        vista = GestionPersonalFrame(self.master, gestion_personal=gestion_personal)
        vista.pack(fill="both", expand=True)

    def abrir_farmacia(self):
        self.destroy()
        vista = GestionFarmaciaFrame(self.master, self.controller, self.usuario)
        vista.pack(fill="both", expand=True)

    def abrir_estadisticas(self):
        self.destroy()
        estadisticas = EstadisticasFrame(self.master, self.controller, self.usuario)
        estadisticas.pack(fill="both", expand=True)

