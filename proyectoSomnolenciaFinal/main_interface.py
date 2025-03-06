import tkinter as tk
from tkinter import messagebox, Toplevel, Tk
import cv2
import mediapipe as mp
from PIL import Image, ImageTk

from activities import ActivitiesWindow
from sleep_test import CPTTestWindow
from results import ResultsWindow
from drowsiness_monitor import DrowsinessMonitor
from ayudas import HelpWindowConfiguracion
from generarPdf import generar_pdf
from registro import get_ci_usuario
from ayudas import HelpWindowSugerencias

class MainInterface:
    def __init__(self, root=None, usuario_nombre="Usuario"):
        self.usuario_nombre = usuario_nombre
        # Usamos el root pasado o creamos uno nuevo
        self.root = root if root is not None else tk.Tk()
        self.root.title("Sistema de Monitoreo de Somnolencia")
        #self.root.geometry("900x600")
        #self.root.minsize(600, 400)
        self.root.attributes("-fullscreen", True)  # Pantalla completa
        self.root.configure(bg="#2E4053")  # Fondo principal
        
        # Nueva variable para saber si la actividad o test ha finalizado
        #self.callback_actividades = None
        #self.callback_test = None
        

        
        # Agregar la llamada a la ayuda automáticamente después de 5 segundos
        self.root.after(1000, self.mostrar_ayuda)  # Llamará a la función después de 5 segundos



        
        # Inicialización de variables de estado
        self.actividad_completada = False
        self.test_completado = False
        self.camara_encendida = False

        # FRAME SUPERIOR: Mensaje de bienvenida
        self.frame_superior = tk.Frame(self.root, bg="#34495E", padx=10, pady=10, relief=tk.RIDGE, bd=5)
        self.frame_superior.pack(side=tk.TOP, fill=tk.X)
        self.bienvenida = tk.Label(self.frame_superior, text=f"¡Bienvenido!, siempre es un gusto tener aquí {self.usuario_nombre}",
                                   font=("Arial", 14, "bold"), fg="#F7DC6F", bg="#34495E", anchor="w")
        self.bienvenida.pack(side=tk.LEFT, padx=10, pady=20)

        # FRAME PRINCIPAL: Contenedor para el menú lateral y el área de contenido
        self.frame_principal = tk.Frame(self.root, bg="#2E4053")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # MENÚ LATERAL
        self.frame_menu = tk.Frame(self.frame_principal, width=300, height=500, bg="#1C2833",
                                   padx=30, pady=10, relief=tk.RIDGE, bd=5)
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        #self.frame_menu.pack_propagate(False)

        # Estilo de botones para el menú
        btn_style = {
            "font": ("Arial", 12, "bold"),
            "fg": "#F7DC6F",
            "bg": "#283747",
            "relief": tk.RAISED,
            "bd": 3,
            "activebackground": "#566573",
            "activeforeground": "#F7DC6F"
        }
        
        # Botón: Actividades
        # Cargar la imagen y ajustarla con subsample
        actividades_img = tk.PhotoImage(file="imagenes/actividad.png").subsample(8, 8)
        
        self.btn_actividades = tk.Button(
            self.frame_menu, text="Actividades", image=actividades_img, padx=10, compound=tk.LEFT,
            command=self.open_activities, **btn_style
        )
        self.btn_actividades.image = actividades_img  # Mantener referencia
        self.btn_actividades.pack(pady=10, fill=tk.X, ipady=10)

        # Botón: Test de Somnolencia
        # Cargar la imagen y ajustarla con subsample
        test_img = tk.PhotoImage(file="imagenes/test.png").subsample(8, 8)
        
        self.btn_test = tk.Button(self.frame_menu, text="Test de Atencion", image=test_img, padx=10, compound=tk.LEFT, 
                                  command=self.open_sleep_test, **btn_style)
        self.btn_test.image = test_img # Mantener referencia
        self.btn_test.pack(pady=10, fill=tk.X,  ipady=10)

        # Botón: Resultados
        # Cargar la imagen y ajustarla con subsample
        resultados_img = tk.PhotoImage(file="imagenes/resultado.png").subsample(8, 8)
        
        self.btn_resultados = tk.Button(self.frame_menu, text="Resultados", image=resultados_img, padx=10, compound=tk.LEFT,
                                        command=self.open_results, **btn_style)
        self.btn_resultados.image = resultados_img
        self.btn_resultados.pack(pady=10, fill=tk.X, ipady=10)
        
        
        
        # **Deshabilitar el botón de "Resultados" inicialmente**
        self.btn_resultados.config(state=tk.DISABLED)
        
        
        #Boton para generar el pdf
        pdf_img = tk.PhotoImage(file="imagenes/pdf.png").subsample(8, 8)
        
        self.btn_pdf = tk.Button(self.frame_menu, text="Generar PDF", image=pdf_img, padx=10, compound=tk.LEFT,
                                        command=self.generar_pdf, **btn_style)
        self.btn_pdf.image = pdf_img
        self.btn_pdf.pack(pady=10, fill=tk.X, ipady=10)
        
        #boton de recomendaciones
        
        recomendaciones_img = tk.PhotoImage(file="imagenes/recomendaciones.png").subsample(4, 4)
        
        self.btn_recomendaciones = tk.Button(self.frame_menu, text="Recomendaciones", image=recomendaciones_img, padx=10, compound=tk.LEFT,
                                        command=self.mostrar_sugerencias, **btn_style, width=200, height=80)
        self.btn_recomendaciones.image = recomendaciones_img
        self.btn_recomendaciones.place(x=0, y=450)

        # Botón: Salir (con mayor margen para separarlo)
        # Cargar la imagen y ajustarla con subsample
        salir_img = tk.PhotoImage(file="imagenes/cerrar.png").subsample(8, 8)
        
        self.btn_salir = tk.Button(self.frame_menu, text="Salir", image=salir_img, padx=10, compound=tk.LEFT, 
                                   command=self.cerrar_sesion, **btn_style)
        self.btn_salir.image = salir_img # Mantener referencia
        self.btn_salir.place(x=50 , y=600)

        # Agregar eventos a los botones del menú para efecto visual
        for btn in [self.btn_actividades, self.btn_test, self.btn_resultados, self.btn_salir, self.btn_pdf, self.btn_recomendaciones]:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)
            btn.bind("<ButtonPress-1>", self.on_press)
            btn.bind("<ButtonRelease-1>", self.on_release)

        # ÁREA DE CONTENIDO PRINCIPAL
        self.frame_contenido = tk.Frame(self.frame_principal, bg="#2E4053")
        self.frame_contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # FRAME PARA LA CÁMARA
        self.frame_camara = tk.Frame(self.frame_contenido, width=1500, height=600,
                                     bg="#1C2833", relief=tk.SUNKEN, bd=5)
        self.frame_camara.pack(fill=tk.NONE, expand=True, padx=20, pady=20)

        # Marco para mostrar el contenido de la cámara (vista de cámara)
        self.marco_camara = tk.LabelFrame(self.frame_camara, text="Vista de cámara",
                                           font=("Arial", 12, "bold"), fg="#F7DC6F", bg="#1C2833",
                                           width=1000, height=500, relief=tk.GROOVE, bd=4)
        self.marco_camara.pack(fill=tk.NONE, expand=True, padx=10, pady=10)
        self.marco_camara.pack_propagate(False)

        # Botón para iniciar la cámara, debajo del área de la cámara
        self.btn_camara = tk.Button(self.frame_camara, text="Iniciar cámara", command=self.toggle_camera, **btn_style)
        self.btn_camara.pack(pady=10)
        self.btn_camara.bind("<Enter>", self.on_enter)
        self.btn_camara.bind("<Leave>", self.on_leave)
        self.btn_camara.bind("<ButtonPress-1>", self.on_press)
        self.btn_camara.bind("<ButtonRelease-1>", self.on_release)

        # Botón de Ayuda en la esquina inferior derecha
        self.frame_ayuda = tk.Frame(self.root, bg="#2E4053")
        self.frame_ayuda.place(relx=0.98, rely=0.98, anchor=tk.SE)
        self.btn_ayuda = tk.Button(self.frame_ayuda, text="Ayuda", command=self.mostrar_ayuda, **btn_style)
        self.btn_ayuda.pack()
        self.btn_ayuda.bind("<Enter>", self.on_enter)
        self.btn_ayuda.bind("<Leave>", self.on_leave)
        self.btn_ayuda.bind("<ButtonPress-1>", self.on_press)
        self.btn_ayuda.bind("<ButtonRelease-1>", self.on_release)

        # Área de video: Se crea dentro del marco de cámara
        self.video_container = tk.Frame(self.marco_camara, bg="black", highlightthickness=5, highlightbackground="red")
        self.video_container.pack(expand=True, fill="both", padx=20, pady=20)

        self.video_label = tk.Label(self.video_container, bg="black")
        self.video_label.pack(expand=True, fill="both", padx=5, pady=5)

        # Variables para manejo de cámara y procesamiento
        self.cap = None
        self.running = False
        self.after_id = None  # Para almacenar el id del callback
        self.imgtk = None  # Referencia a la imagen
        
        # Llamadas a las funciones de estado de los botones (activación/desactivación)
        self.callback_actividades = self.actividad_completada_callback
        self.callback_test = self.test_completado_callback


        



    # Métodos para los efectos visuales en botones
    def on_enter(self, event):
        event.widget.config(bg="#1F618D", fg="#F7DC6F")
    def on_leave(self, event):
        event.widget.config(bg="#283747", fg="#F7DC6F")
    def on_press(self, event):
        event.widget.config(relief=tk.SUNKEN)
    def on_release(self, event):
        event.widget.config(relief=tk.RAISED)

    def mostrar_advertencia(self, titulo, mensaje):
        """ Muestra una ventana emergente con información de advertencia """
        ventana = Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("400x200")
        ventana.configure(bg="#2C3E50")

        tk.Label(ventana, text=titulo, font=("Arial", 14, "bold"), fg="white", bg="#2C3E50").pack(pady=10)
        tk.Label(ventana, text=mensaje, font=("Arial", 12), fg="white", bg="#34495E", wraplength=380, justify="center").pack(pady=10)
        tk.Button(ventana, text="Entendido", command=ventana.destroy, font=("Arial", 12, "bold"), bg="#E74C3C", fg="white").pack(pady=10)
        
        

    def actividad_completada_callback(self):
        """Actualizar el estado cuando la actividad se complete."""
        self.actividad_completada = True
        self.block_actividades_button()  # Desactivar el botón de actividades
        self.actualizar_boton_resultados()
        self.block_pdf_button()  # Desactivar el botón de PDF si alguna actividad se ha completado

    def test_completado_callback(self):
        """Actualizar el estado cuando el test se complete."""
        self.test_completado = True
        self.block_test_button()  # Desactivar el botón de test
        self.actualizar_boton_resultados()
        self.block_pdf_button()  # Desactivar el botón de PDF si el test se ha completado

    def actualizar_boton_resultados(self):
        """Activar o desactivar el botón de Resultados dependiendo de si las actividades y el test están completos."""
        if self.actividad_completada and self.test_completado:
            self.btn_resultados.config(state=tk.NORMAL)
        else:
            self.btn_resultados.config(state=tk.DISABLED)

    def block_actividades_button(self):
        """Desactiva el botón de Actividades"""
        self.btn_actividades.config(state=tk.DISABLED)
        
    def block_test_button(self):
        """Desactiva el botón de Test"""
        self.btn_test.config(state=tk.DISABLED)
        
    def block_pdf_button(self):
        """Desactiva el botón de Generar PDF si una de las actividades o test no está completo"""
        if self.actividad_completada and self.test_completado:
            self.btn_pdf.config(state=tk.NORMAL)  # Habilita el botón de PDF solo si ambas actividades se completaron
        else:
            self.btn_pdf.config(state=tk.DISABLED)  # Desactiva el botón de PDF si alguna actividad no se ha completado


    def unblock_resultados_button(self):
        """Habilita el botón de Resultados"""
        self.btn_resultados.config(state=tk.NORMAL)
            
            
            
            
            
            
            
            
            
    def open_activities(self):
        
        """ Abre la ventana de actividades cuando se completa la actividad """
        self.stop_camera()
        #ActivitiesWindow(self.root)
        ActivitiesWindow(self.root, self.callback_actividades)  # Pasamos la función de callback



    def open_sleep_test(self):

        self.stop_camera()
        """Abre el test de somnolencia cuando se completa la actividad"""
        CPTTestWindow(self.root, self.callback_test)  # Pasamos la función de callback
    
    
    def open_results(self):
        """ Verifica si tanto la actividad como el test han sido completados antes de mostrar los resultados.
            Luego, reinicia el proceso para un nuevo análisis.
        """

        
        # 🔄 Reiniciar variables para un nuevo análisis
        self.actividad_completada = False
        self.test_completado = False
        self.camara_encendida = False  # Opcional si deseas que la cámara se apague al iniciar un nuevo análisis
        
        # Abrir la ventana de resultados
        ResultsWindow(self.root)


    def generar_pdf(self):
        ci = get_ci_usuario()
        generar_pdf(ci)
        #mostrar un mensaje de exito
        messagebox.showinfo("PDF Generado", "El PDF ha sido generado con éxito.")
        
    def mostrar_sugerencias(self):
        """ Muestra una ventana con sugerencias para evitar la somnolencia """
        HelpWindowSugerencias(self.root)

        
        
                        
    def mostrar_ayuda(self):
        """ Muestra una ventana de ayuda con información sobre cómo usar el sistema """
        HelpWindowConfiguracion(self.root)

    # Funcionalidad para iniciar y apagar la cámara
    def toggle_camera(self):
        if self.running:
            self.stop_camera()
        else:
            # Encender la cámara
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "No se pudo abrir la cámara")
                return
            self.running = True
            self.btn_camara.config(text="Apagar cámara")
            self.video_container.config(highlightbackground="green")  # Cambiar a verde cuando la cámara está encendida
            self.process_video()

    def stop_camera(self):
        # Apagar la cámara
        self.running = False
        self.btn_camara.config(text="Iniciar cámara")
        self.video_container.config(highlightbackground="red")  # Cambiar a rojo cuando la cámara está apagada
        if self.after_id is not None:
            self.video_label.after_cancel(self.after_id)
            self.after_id = None
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        if self.video_label.winfo_exists():
            self.video_label.config(image="")
        self.imgtk = None
    
    def process_video(self):
        if not self.running or self.cap is None or not self.video_label.winfo_exists():
            return
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            self.imgtk = ImageTk.PhotoImage(image=img)
            try:
                if self.video_label.winfo_exists():
                    self.video_label.configure(image=self.imgtk)
                    self.video_label.image = self.imgtk
            except tk.TclError as e:
                print("Error actualizando la imagen:", e)
        if self.running and self.video_label.winfo_exists():
            self.after_id = self.video_label.after(10, self.process_video)
        else:
            if self.cap:
                self.cap.release()
                self.cap = None


    def cerrar_sesion(self):
        self.root.destroy()
        from login import LoginWindow  # Importación dentro de la función para evitar bucle
        login = LoginWindow()
        login.run()    

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = MainInterface()
    app.run()
