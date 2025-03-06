import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import cv2
import mediapipe as mp
import psycopg2
from Ractvidades import guardar_datos_actividad
from drowsiness_monitor import DrowsinessMonitor
import threading
from ayudas import HelpWindowActividades
from registro import get_ci_usuario


# 📌 Variable global para almacenar los resultados de las actividades
actividades_resultados = {
    "tiempo_ojos": 0,
    "parpadeos": 0,
    "porcentaje_ojos": 0.0
}

def guardar_resultados_actividades(tiempo_ojos, parpadeos, porcentaje_ojos):
    """Guarda los resultados de las actividades en la variable global"""
    global actividades_resultados
    actividades_resultados["tiempo_ojos"] = tiempo_ojos
    actividades_resultados["parpadeos"] = parpadeos
    actividades_resultados["porcentaje_ojos"] = porcentaje_ojos

def get_resultados_actividades():
    """📌 Devuelve los resultados de las actividades"""
    return actividades_resultados


class ActivitiesWindow:
    def __init__(self, master, callback):
        self.top = tk.Toplevel(master)
        self.callback = callback  # Guardamos la función de callback
        self.top.title("Actividades")
        # self.top.geometry("1280x720")
        self.top.attributes("-fullscreen", True)
        self.top.configure(bg="#1C1C3C")
        self.top.state("zoomed")
        
        self.top.after(1000, self.open_help)  # Mostrar la ayuda después de 1 segundo

        # Contenedor izquierdo (Actividades, más grande)
        self.frame_actividades = tk.Frame(self.top, bg="#566573", width=900, height=700, relief=tk.GROOVE, bd=6, highlightbackground="#AEB6BF", highlightthickness=2)
        self.frame_actividades.place(x=30, y=40, width=900, height=700)

        # Contenedor derecho (Cámara y control, más pequeño)
        self.frame_camara = tk.Frame(self.top, bg="#34495E", width=400, height=500, relief=tk.GROOVE, bd=6, highlightbackground="#566573", highlightthickness=2)
        self.frame_camara.place(x=950, y=120, width=575, height=500)

        # Temporizador
        self.timer_label = tk.Label(self.frame_camara, text="05:00", font=("Arial", 32, "bold"), bg="#1F618D", fg="#F4D03F", padx=20, pady=10, relief=tk.RIDGE, bd=4)
        self.timer_label.pack(pady=10, fill=tk.X)

        # Placeholder de la cámara (imagen o texto inicial)
        self.camera_placeholder = tk.Label(self.frame_camara, text="Iniciar Cámara", font=("Arial", 18), bg="#000000", fg="white")
        self.camera_placeholder.pack(fill=tk.BOTH, expand=True)  # Ajuste al tamaño del Frame

        # Botón de cerrar ventana
        self.close_button = tk.Button(self.top, text="Cerrar", font=("Arial", 16, "bold"), bg="#E74C3C", fg="white", relief=tk.RAISED, padx=15, pady=8, borderwidth=5, activebackground="#C0392B", activeforeground="white", cursor="hand2", command=self.close_window)
        self.close_button.place(x=1150, y=650)
        
        
        # Botón de ayuda
        self.help_button = tk.Button(self.top, text="Ayuda", font=("Arial", 16, "bold"), bg="#3498db", fg="white", relief=tk.RAISED, padx=15, pady=8, borderwidth=5, activebackground="#2980b9", activeforeground="white", cursor="hand2", command=self.open_help)
        self.help_button.place(x=1425, y=750)
        

        """"
        # Espacio para la cámara (Usamos un Label para mostrar el video)
        self.camera_placeholder = tk.Label(self.frame_camara, bg="#000000")
        self.camera_placeholder.pack(fill=tk.BOTH)  # Ajustamos el tamaño a todo el espacio disponible
        """""
        # Botón de inicio de actividades
        self.start_button = tk.Button(self.frame_camara, text="Iniciar Actividades", font=("Arial", 16, "bold"), bg="#28B463", fg="white", relief=tk.RAISED, padx=15, pady=8, borderwidth=5, activebackground="#1E8449", activeforeground="white", cursor="hand2", command=self.start_activities)
        self.start_button.pack(pady=20)

        # Variables para el temporizador y actividades
        self.time_left = 300
        self.timer_running = False
        self.activities = [
            ("Actividad de Stroop", self.load_stroop_test, 60),
            ("Actividad de Reacción", self.load_reaction_test, 60),
            ("Lectura de PDF", self.load_pdf_reading, 180)
        ]
        self.current_activity = 0
        self.stroop_running = False
        self.reaction_running = False
        self.stroop_label = None
        self.stroop_timer = None  # Variable para manejar el temporizador
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.missed_answers = 0  # Nueva variable para contar respuestas no respondidas
        
        # Inicializamos el monitor de somnolencia
        self.drowsiness_monitor = DrowsinessMonitor()

        # Iniciar la captura de video en un hilo separado
        self.capture_thread = threading.Thread(target=self.start_video_capture)
        self.capture_thread.daemon = True
        self.capture_thread.start()

        # Configuración para el tamaño fijo de la cámara
        self.camera_width = 500  # Ancho fijo para la cámara
        self.camera_height = 325  # Alto fijo para la cámara

        # Inicializamos MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Variables de control de la cámara
        self.video_thread = None
        self.camera_on = False


    def open_help(self):
        HelpWindowActividades(self.top)

    def close_window(self):
        self.stop_camera()  # Detiene la cámara antes de cerrar
        self.top.destroy()  # Cierra la ventana Toplevel

    def start_video_capture(self):
        # Inicia la captura de video desde la cámara
        self.cap = cv2.VideoCapture(0)
        while self.camera_on:
            ret, frame = self.cap.read()
            if ret:
                # Convertimos el fotograma de BGR a RGB (Tkinter necesita RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Redimensionamos el fotograma para ajustarse al tamaño fijo
                frame_resized = cv2.resize(frame_rgb, (self.camera_width, self.camera_height))

                # Convertimos la imagen a un formato que Tkinter pueda manejar
                img = Image.fromarray(frame_resized)
                img_tk = ImageTk.PhotoImage(image=img)

                # Actualizamos la imagen del Label en Tkinter (se hace en el hilo principal)
                self.camera_placeholder.img_tk = img_tk  # Guardamos la referencia de la imagen
                self.camera_placeholder.config(image=img_tk)

                # Convertimos la imagen a formato BGR para usar con OpenCV
                frame_bgr = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)

                # Detectamos los puntos faciales
                results = self.face_mesh.process(frame_bgr)

                if results.multi_face_landmarks:
                    for landmarks in results.multi_face_landmarks:
                        # Dibujamos los puntos de los ojos en el video
                        self.draw_eye_points(frame_bgr, landmarks)

                        # Calculamos EAR y PERCLOS
                        frame_bgr, ear, perclos = self.drowsiness_monitor.update(frame_bgr, landmarks, frame_bgr.shape[1], frame_bgr.shape[0])

                        # Mostrar EAR y PERCLOS en la imagen con colores personalizados
                        cv2.putText(frame_bgr, f"EAR: {ear:.2f}", (30, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # EAR en verde
                        cv2.putText(frame_bgr, f"PERCLOS: {perclos:.2f}%", (30, 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)  # PERCLOS en rojo

                # Mostrar el frame actualizado en Tkinter
                img_bgr = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img_bgr)
                img_tk = ImageTk.PhotoImage(image=img)
                self.camera_placeholder.img_tk = img_tk
                self.camera_placeholder.config(image=img_tk)

            # Esperamos un poco antes de continuar con el siguiente frame
            time.sleep(0.03)

    def draw_eye_points(self, frame, landmarks):
        # Índices de puntos de los ojos según MediaPipe
        left_eye_indices = [33, 160, 158, 133, 153, 144]
        right_eye_indices = [362, 385, 387, 263, 373, 380]

        # Dibujamos los puntos de los ojos izquierdo y derecho
        for idx in left_eye_indices + right_eye_indices:
            lm = landmarks.landmark[idx]
            x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)


    def start_activities(self):
        
        # Llamar al callback para bloquear el botón de actividades en MainInterface
        if self.callback:
            self.callback()
        
        # Desactivar el botón de cerrar solo al presionar "Iniciar Actividades"
        self.close_button.config(state=tk.DISABLED)  # Desactivar el botón de cerrar cuando inicia la actividad
        #desactivar el botón de ayuda
        self.help_button.config(state=tk.DISABLED)
        #desactivar el botón de inicio de actividades
        self.start_button.config(state=tk.DISABLED)

        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
            self.load_next_activity()
            self.start_camera()
            
 

            
    def start_camera(self):
        self.camera_on = True
        self.camera_placeholder.config(text="Cargando Cámara...")  # Mostrar el mensaje antes de iniciar

        # Iniciar la captura de video en un hilo
        self.video_thread = threading.Thread(target=self.start_video_capture)
        self.video_thread.daemon = True
        self.video_thread.start()
        



    def stop_camera(self):
        self.camera_on = False
        if self.cap.isOpened(): 
            self.cap.release()
            




    def resultados(self):
        # Obtener los resultados al finalizar el análisis
        total_eye_closed_time, blink_rate, perc_closed = self.drowsiness_monitor.get_results()

        # Mostrar resultados por consola cuando se acabe el tiempo
        print(f"Tiempo total de ojos cerrados: {total_eye_closed_time} segundos")
        print(f"Tasa de parpadeo: {blink_rate} parpadeos/minuto")
        print(f"Porcentaje de ojos cerrados: {perc_closed:.2f}%")
        
        ci_usuario = get_ci_usuario()
        guardar_datos_actividad(ci_usuario, total_eye_closed_time, blink_rate, perc_closed)
        

        
        
        # 📌 Guardar los resultados en la variable global
        guardar_resultados_actividades(total_eye_closed_time, blink_rate, perc_closed)

        # 📌 Mostrar resultados en consola (para depuración)
        print(f"📊 Resultados Actividades:")
        print(f"Tiempo de ojos cerrados: {total_eye_closed_time} s")
        print(f"Parpadeos detectados: {blink_rate}")
        print(f"Porcentaje de ojos cerrados: {perc_closed}%")

    
    
    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
        if self.time_left > 0:
            self.time_left -= 1
            self.top.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.stop_camera() # Detener la cámara al finalizar el tiempo
            self.resultados()  # Mostrar resultados después de que el temporizador llegue a 0
            # Bloquear el botón de actividades después de completar los 5 minutos
            # Llamamos al callback para desactivar el botón
            
            
            # **Reactivar el botón de cerrar después de completar la actividad**
            self.close_button.config(state=tk.NORMAL)  # Reactivar al terminar
            #reactivar el botón de ayuda
            self.help_button.config(state=tk.NORMAL)
            
            
        


    def load_next_activity(self):
        if self.current_activity < len(self.activities):
            activity_name, activity_function, duration = self.activities[self.current_activity]
            self.current_activity += 1
            self.display_title(activity_name)
            activity_function()
            self.top.after(duration * 1000, self.load_next_activity)

    def display_title(self, title):
        for widget in self.frame_actividades.winfo_children():
            widget.destroy()
        tk.Label(self.frame_actividades, text=title, font=("Arial", 24, "bold"), bg="#566573").pack(pady=10)

    def load_stroop_test(self):
        self.stroop_running = True

        # Limpieza del frame antes de agregar nuevos elementos
        for widget in self.frame_actividades.winfo_children():
            widget.destroy()

        self.display_title("Actividad de Stroop")

        # Label de la palabra en el centro
        self.stroop_label = tk.Label(self.frame_actividades, font=("Arial", 36, "bold"), bg="#566573")
        self.stroop_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Contenedor para los botones en formato 2x2 con tamaños más grandes
        self.button_frame = tk.Frame(self.frame_actividades, bg="#E0E0F8")
        self.button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Etiqueta para mostrar mensaje de correcto/incorrecto
        self.feedback_label = tk.Label(self.frame_actividades, text="", font=("Arial", 16, "bold"), bg="#566573")
        self.feedback_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        # Etiqueta para mostrar conteo de respuestas
        self.score_label = tk.Label(self.frame_actividades, text="Correctos: 0 | Incorrectos: 0 | Vacíos: 0", font=("Arial", 14, "bold"), bg="#566573")
        self.score_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.schedule_stroop_update()

    def schedule_stroop_update(self):
        if self.stroop_running:
            self.missed_answers += 1  # Contar las palabras no respondidas
            self.update_stroop_test()
            self.update_score_label()
            self.stroop_timer = self.top.after(2000, self.schedule_stroop_update)

    def update_stroop_test(self):
        if not self.stroop_running:
            return
        # Colores posibles para el test
        colors = [
            ("Rojo", "red"), 
            ("Azul", "blue"), 
            ("Verde", "green"), 
            ("Amarillo", "yellow")
        ]
        
        # Elegir una palabra y un color diferente
        self.current_word, self.current_color = random.choice(colors)
        word, color = random.choice(colors)  # Elegir un color diferente
        while word == self.current_word:  # Asegurarse de que el color no coincida con la palabra
            word, color = random.choice(colors)

        # Mostrar la palabra con un color diferente
        self.stroop_label.config(text=self.current_word, fg=color)

        # Limpieza de los botones
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Crear los botones en 2 filas x 2 columnas con colores posibles
        for i in range(2):
            for j in range(2):
                color_name, color_value = colors[i * 2 + j]
                tk.Button(self.button_frame, text=color_name, bg=color_value, width=15, height=5, font=("Arial", 14, "bold"),
                        command=lambda color=color_value: self.check_stroop_answer(color)).grid(row=i, column=j, padx=10, pady=10)

    def check_stroop_answer(self, selected_color):
        if selected_color == self.current_color:
            self.feedback_label.config(text="¡Correcto!", fg="green")
            self.correct_answers += 1
        else:
            self.feedback_label.config(text="Incorrecto", fg="red")
            self.incorrect_answers += 1

        self.missed_answers -= 1  # Restar la cuenta de palabras no respondidas
        self.update_score_label()

        if self.stroop_timer:
            self.top.after_cancel(self.stroop_timer)  # Cancelar el temporizador actual
        self.schedule_stroop_update()  # Reiniciar el temporizador desde cero


    def update_score_label(self):
        self.score_label.config(text=f"Correctos: {self.correct_answers} | Incorrectos: {self.incorrect_answers} | Vacíos: {self.missed_answers}")


    def load_reaction_test(self):
        self.reaction_running = True
        self.reaction_times = []  # Lista para almacenar los tiempos de reacción
        self.failed_attempts = 0  # Contador de fallos
        self.waiting_for_reaction = False  # Evita respuestas antes de tiempo

        # Mensaje de preparación
        self.reaction_label = tk.Label(self.frame_actividades, text="Preparado para reaccionar",
                                    font=("Arial", 24, "bold"), bg="#E0E0F8", width=30, height=3)
        self.reaction_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Relativo al tamaño de la ventana

        # Etiqueta para mostrar el tiempo de reacción
        self.reaction_feedback_label = tk.Label(self.frame_actividades, text="",
                                                font=("Arial", 16), bg="#566573", fg="white")
        self.reaction_feedback_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)  # Más abajo

        # Etiqueta para mostrar puntaje
        self.reaction_score_label = tk.Label(self.frame_actividades, text="Aciertos: 0 | Fallos: 0",
                                            font=("Arial", 16, "bold"), bg="#566573")
        self.reaction_score_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)  # Bajamos más el puntaje


        # Vinculamos la tecla Enter para evitar respuestas antes de tiempo
        self.top.bind("<Return>", self.early_reaction)

        self.schedule_next_attempt()

    def schedule_next_attempt(self):
        """Programa el siguiente intento con un tiempo de preparación aleatorio"""
        self.reaction_label.config(bg="#E0E0F8", text="Preparado para reaccionar")
        self.waiting_for_reaction = False  # Bloquea respuestas antes de tiempo

        # Elegir un tiempo de preparación entre 2 y 4 segundos
        preparation_time = random.randint(2000, 6000)
        self.top.after(preparation_time, self.change_reaction_color)

    def change_reaction_color(self):
        """Cambia el color indicando que el usuario debe reaccionar"""
        if self.reaction_running:
            self.reaction_label.config(bg="red", text="¡Presiona ENTER ahora!")
            self.waiting_for_reaction = True  # Ahora sí se pueden registrar respuestas

            # Guardamos el tiempo exacto en el que cambiamos el color
            self.reaction_start_time = time.time()

            # Cambiamos la función vinculada a Enter para permitir registrar la reacción
            self.top.bind("<Return>", self.reaction_pressed)

            # Si el usuario no reacciona en 1.5 segundos, contará como fallo
            self.reaction_timeout = self.top.after(1500, self.register_fail)

    def reaction_pressed(self, event):
        """Registra el tiempo de reacción cuando el usuario presiona ENTER"""
        if self.reaction_running and self.waiting_for_reaction:  # Solo si está en el estado correcto
            reaction_time = time.time() - self.reaction_start_time
            self.reaction_times.append(reaction_time)

            # Cancelamos el timeout para evitar registrar un fallo
            self.top.after_cancel(self.reaction_timeout)

            # Feedback del tiempo de reacción
            self.reaction_feedback_label.config(text=f"Tiempo de reacción: {reaction_time:.3f} segundos", fg="black")

            # Actualizamos el puntaje
            self.update_reaction_score()

            # Desvinculamos el evento de la tecla Enter hasta la siguiente prueba
            self.top.unbind("<Return>")

            # Programamos el siguiente intento con un tiempo de preparación aleatorio
            self.top.after(1000, self.schedule_next_attempt)

    def early_reaction(self, event):
        """Detecta si el usuario presiona ENTER antes de que el color cambie"""
        if not self.waiting_for_reaction:  # Si aún no era el momento de reaccionar
            self.failed_attempts += 1
            self.reaction_feedback_label.config(text="¡Presionaste demasiado pronto!", fg="red")

            # Actualizar el puntaje de fallos
            self.update_reaction_score()

            # Reiniciar el test después de 1 segundo
            self.top.after(1000, self.schedule_next_attempt)

    def register_fail(self):
        """Registra un fallo si el usuario no presiona Enter a tiempo"""
        if self.waiting_for_reaction:  # Solo registrar si el color ya había cambiado
            self.failed_attempts += 1
            self.reaction_feedback_label.config(text="¡Demasiado tarde!", fg="red")

            # Actualizar el puntaje de fallos
            self.update_reaction_score()

            # Programamos el siguiente intento con un tiempo de preparación aleatorio
            self.top.after(1000, self.schedule_next_attempt)

    def update_reaction_score(self):
        """Actualiza la etiqueta de puntuación"""
        aciertos = len(self.reaction_times)  # Número de reacciones exitosas
        self.reaction_score_label.config(text=f"Aciertos: {aciertos} | Fallos: {self.failed_attempts}")


     
    def load_pdf_reading(self):
        # Iniciar la lectura de PDF (en este caso, la imagen)
        self.display_title("Lectura de PDF")

        # Crear el Canvas directamente en el frame_actividades
        self.canvas = tk.Canvas(self.frame_actividades, bg="white", width=700, height=550)  # Tamaño del Canvas
        self.canvas.place(relx=0.5, rely=0.50, anchor=tk.CENTER)  # Posicionamos el Canvas correctamente

        # Cargar la imagen correctamente desde la ruta
        self.img = Image.open("imagenes/lectura.png")  # Ruta correcta a la imagen cargada
        self.img_tk = ImageTk.PhotoImage(self.img)

        # Crear la imagen en el Canvas y moverla hacia abajo
        self.image_on_canvas = self.canvas.create_image(0, 100, image=self.img_tk, anchor=tk.NW)  # Ajustamos la posición de la imagen

        # Crear las barras de desplazamiento
        self.scrollbar_y = ttk.Scrollbar(self.frame_actividades, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.place(relx=0.89, rely=0.10, height=550)  # Barra de desplazamiento vertical pegada al Canvas

        self.scrollbar_x = ttk.Scrollbar(self.frame_actividades, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.place(relx=0.50, rely=0.90, anchor=tk.CENTER, width=700)  # Barra de desplazamiento horizontal pegada al Canvas

        # Configurar el Canvas para que use las barras de desplazamiento
        self.canvas.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Ajustar la región de desplazamiento del Canvas
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))  # Asegúrate de que el scrollregion esté configurado correctamente

        # Crear un frame para los botones de zoom
        zoom_frame = tk.Frame(self.frame_actividades, bg="#566573")
        zoom_frame.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  # Los botones de zoom se colocan debajo del Canvas

        # Botones para hacer zoom
        self.zoom_in_btn = tk.Button(zoom_frame, text="Zoom In", command=lambda: self.zoom(1.2))  # Aumentar tamaño
        self.zoom_in_btn.grid(row=0, column=0, padx=10)

        self.zoom_out_btn = tk.Button(zoom_frame, text="Zoom Out", command=lambda: self.zoom(0.8))  # Reducir tamaño
        self.zoom_out_btn.grid(row=0, column=1, padx=10)

        # Inicializamos el factor de zoom
        self.zoom_factor = 1.0

    def zoom(self, factor):
        # Actualizar el factor de zoom acumulado
        self.zoom_factor *= factor

        # Calcular el nuevo tamaño basado en el factor de zoom acumulado
        new_width = int(self.img.width * self.zoom_factor)
        new_height = int(self.img.height * self.zoom_factor)

        # Redimensionar la imagen
        img_resized = self.img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)

        # Actualizar la imagen en el canvas
        self.canvas.itemconfig(self.image_on_canvas, image=img_tk)

        # Ajustar las dimensiones del canvas según el tamaño de la nueva imagen
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))  # Asegúrate de actualizar la región de desplazamiento

        # Guardar la imagen redimensionada para evitar que se pierda en la próxima actualización
        self.img_tk = img_tk


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = ActivitiesWindow(root)
    root.mainloop()
