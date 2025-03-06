# help_windows.py
import tkinter as tk

class HelpWindowActividades:
    def __init__(self, master=None):
        self.top = tk.Toplevel(master)
        self.top.title("Ayuda: Actividades")
        self.top.geometry("800x500")  # Tamaño estático
        self.top.configure(bg="#2c3e50")  # Fondo oscuro

        # Hacer la ventana no redimensionable
        self.top.resizable(False, False)

        # Crear un frame para todo el contenido
        self.frame_principal = tk.Frame(self.top, bg="#2c3e50", padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(self.frame_principal, text="Aquí puedes ver información sobre las actividades realizadas para monitorear la somnolencia.",
                 font=("Arial", 12), bg="#2c3e50", fg="#F1C40F", justify="center").pack(pady=10)

        # Crear el área para mostrar los puntos de ayuda
        self.frame_instrucciones = tk.Frame(self.frame_principal, bg="#34495e", relief="solid", bd=2, padx=20, pady=10)
        self.frame_instrucciones.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título de instrucciones
        tk.Label(self.frame_instrucciones, text="Instrucciones", font=("Arial", 14, "bold"), bg="#34495e", fg="#F1C40F").pack(pady=10)

        # Agregar los puntos de la lista con los nuevos mensajes
        puntos = [
            "1. Procure centrar su rostro en la cámara para el análisis.",
            "2. Una vez terminado las actividades de click en el botón volver.",
            "3. Los resultados se mostrarán en la sección de resultados.",
            "4. Asegúrese de haber completado todas las actividades antes de ver los resultados.",
            "5. Si presiona el boton de cerrar los resultados no se guardarán."
        ]
        
        for punto in puntos:
            tk.Label(self.frame_instrucciones, text=punto, font=("Arial", 12), bg="#34495e", fg="#ecf0f1", justify="left").pack(anchor="w", padx=20, pady=5)

        # Botón "Volver"
        self.boton_volver = tk.Button(self.frame_principal, text="Volver", command=self.top.destroy, font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", relief="raised", bd=2)
        self.boton_volver.pack(side=tk.BOTTOM, pady=10)


class HelpWindowTestSomnolencia:
    def __init__(self, master=None):
        # Cambiar Toplevel por Tk para hacer la ventana completamente independiente
        self.top = tk.Tk()
        self.top.title("Ayuda: Test de Somnolencia")
        self.top.geometry("700x500")
        self.top.configure(bg="#ecf0f1")

        # Hacer la ventana no redimensionable
        self.top.resizable(False, False)

        self.frame_principal = tk.Frame(self.top, bg="#ecf0f1", padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame_principal, text="Aquí puedes ver las instrucciones para el Test de Somnolencia.",
                 font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", justify="center").pack(pady=10)

        self.frame_instrucciones = tk.Frame(self.frame_principal, bg="#ffffff", relief="solid", bd=2, padx=20, pady=10)
        self.frame_instrucciones.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame_instrucciones, text="Instrucciones", font=("Arial", 14, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)

        puntos = [
            "1. Inicia el test de somnolencia y sigue las instrucciones.",
            "2. Asegúrate de estar en un lugar cómodo y sin distracciones.",
            "3. Los resultados aparecerán después de completar el test."
        ]
        
        for punto in puntos:
            tk.Label(self.frame_instrucciones, text=punto, font=("Arial", 12), bg="#ffffff", fg="#34495e", justify="left").pack(anchor="w", padx=20, pady=5)

        # Cambiar el comando de este botón para cerrar solo la ventana de ayuda
        self.boton_volver = tk.Button(self.frame_principal, text="Volver", command=self.top.withdraw, font=("Arial", 12, "bold"), bg="#3498db", fg="white", relief="raised", bd=2)
        self.boton_volver.pack(side=tk.BOTTOM, pady=10)




class HelpWindowResultados:
    def __init__(self, master=None):
        self.top = tk.Toplevel(master)
        self.top.title("Ayuda: Resultados")
        self.top.geometry("700x500")
        self.top.configure(bg="#ecf0f1")

        # Hacer la ventana no redimensionable
        self.top.resizable(False, False)

        self.frame_principal = tk.Frame(self.top, bg="#ecf0f1", padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame_principal, text="Aquí puedes ver los resultados de las actividades y el test de somnolencia.",
                 font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", justify="center").pack(pady=10)

        self.frame_instrucciones = tk.Frame(self.frame_principal, bg="#ffffff", relief="solid", bd=2, padx=20, pady=10)
        self.frame_instrucciones.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame_instrucciones, text="Instrucciones", font=("Arial", 14, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)

        puntos = [
            "1. Los resultados se generarán después de completar tanto el test como las actividades.",
            "2. Revisa los resultados completos en la sección de resultados para un análisis detallado.",
            "3. Asegúrate de haber completado todas las etapas del sistema antes de ver los resultados."
        ]
        
        for punto in puntos:
            tk.Label(self.frame_instrucciones, text=punto, font=("Arial", 12), bg="#ffffff", fg="#34495e", justify="left").pack(anchor="w", padx=20, pady=5)

        self.boton_volver = tk.Button(self.frame_principal, text="Volver", command=self.top.destroy, font=("Arial", 12, "bold"), bg="#3498db", fg="white", relief="raised", bd=2)
        self.boton_volver.pack(side=tk.BOTTOM, pady=10)


class HelpWindowConfiguracion:
    def __init__(self, master=None):
        self.top = tk.Toplevel(master)
        self.top.title("Ayuda: Configuración")
        self.top.geometry("800x500")  # Tamaño estático
        self.top.configure(bg="#2c3e50")  # Fondo principal suave

        # Hacer la ventana no redimensionable
        self.top.resizable(False, False)

        # Crear un frame para todo el contenido
        self.frame_principal = tk.Frame(self.top, bg="#2c3e50", padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(self.frame_principal, text="Aquí puedes ver las instrucciones para usar el sistema de monitoreo de somnolencia.",
                 font=("Arial", 12), bg="#2c3e50", fg="#F1C40F", justify="center").pack(pady=10)

        # Crear el área para mostrar los puntos de ayuda
        self.frame_instrucciones = tk.Frame(self.frame_principal, bg="#34495e", relief="solid", bd=2, padx=20, pady=10)
        self.frame_instrucciones.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título de instrucciones
        tk.Label(self.frame_instrucciones, text="Instrucciones", font=("Arial", 14, "bold"), bg="#34495e", fg="#F1C40F").pack(pady=10)

        # Agregar los puntos de la lista
        puntos = [
            "1. Activa la cámara y verifica que tu rostro esté en una posición correcta para el análisis.",
            "2. Recuerda iniciar primero las actividades y después el test.",
            "3. El botón de resultados mostrará tu análisis actual."
        ]
        
        for punto in puntos:
            tk.Label(self.frame_instrucciones, text=punto, font=("Arial", 12), bg="#34495e", fg="#ecf0f1", justify="left").pack(anchor="w", padx=20, pady=5)

        # Botón "Volver"
        self.boton_volver = tk.Button(self.frame_principal, text="Volver", command=self.top.destroy, font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", relief="raised", bd=2)
        self.boton_volver.pack(side=tk.BOTTOM, pady=10)
        
        
class HelpWindowSugerencias:
    def __init__(self, master=None):
        self.top = tk.Toplevel(master)
        self.top.title("Recomendaciones para evitar la somnolencia")
        self.top.geometry("700x500")  # Tamaño de la ventana
        self.top.configure(bg="#2c3e50")  # Fondo oscuro

        # Hacer la ventana no redimensionable
        self.top.resizable(False, False)

        # Crear un frame para todo el contenido
        self.frame_principal = tk.Frame(self.top, bg="#2c3e50", padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(self.frame_principal, text="Recomendaciones para evitar la somnolencia:",
                 font=("Arial", 12), bg="#2c3e50", fg="#F1C40F", justify="center").pack(pady=10)

        # Crear el área para mostrar las recomendaciones
        self.frame_recomendaciones = tk.Frame(self.frame_principal, bg="#34495e", relief="solid", bd=2, padx=20, pady=10)
        self.frame_recomendaciones.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título de recomendaciones
        tk.Label(self.frame_recomendaciones, text="Recomendaciones", font=("Arial", 14, "bold"), bg="#34495e", fg="#F1C40F").pack(pady=10)

        # Agregar las recomendaciones en una lista
        recomendaciones = [
            "1. Duerme entre 7 y 9 horas por noche.",
            "2. Evita la cafeína y las comidas pesadas antes de dormir.",
            "3. Realiza ejercicio regularmente.",
            "4. Mantén una rutina de sueño constante.",
            "5. Evita las siestas largas durante el día.",
            "6. Mantén tu habitación oscura y fresca.",
            "7. Evita el uso de dispositivos electrónicos antes de dormir."
        ]
        
        for recomendacion in recomendaciones:
            tk.Label(self.frame_recomendaciones, text=recomendacion, font=("Arial", 12), bg="#34495e", fg="#ecf0f1", justify="left").pack(anchor="w", padx=20, pady=5)

        # Botón "Cerrar"
        self.boton_cerrar = tk.Button(self.frame_principal, text="Cerrar", command=self.top.destroy, font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", relief="raised", bd=2)
        self.boton_cerrar.pack(side=tk.BOTTOM, pady=10)