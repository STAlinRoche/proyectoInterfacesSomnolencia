import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from pantallaCarga import show_loading_screen  # Función que lanza la pantalla de carga e interfaz principal
from registro import nuevo_usuario, ingreso_usuario  #funciones desde registro.py

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        #self.root.geometry("700x700")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        
        # Primer texto de bienvenida
        texto_bienvenida_1 = tk.Label(self.root, text="Bienvenido al sistema de", 
                                      font=("Edwardian Script ITC", 32), fg="white", bg="black")
        texto_bienvenida_1.pack(pady=0)
        
        # Segundo texto
        texto_bienvenida_2 = tk.Label(self.root, text="reconocimiento de somnolencia", 
                                      font=("Edwardian Script ITC", 32), fg="white", bg="black")
        texto_bienvenida_2.pack(pady=0)
        
        # Texto "by"
        texto_bienvenida_3 = tk.Label(self.root, text="by", 
                                      font=("Edwardian Script ITC", 32), fg="white", bg="black")
        texto_bienvenida_3.pack(pady=0)
        
        # Cargar logo
        try:
            imagen_original = Image.open("imagenes/Logo.png")  # Asegúrate de que la ruta sea correcta
            imagen_redimensionada = imagen_original.resize((250, 200))
            self.logo = ImageTk.PhotoImage(imagen_redimensionada)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")
            self.logo = None
        
        imagen_logo = tk.Label(self.root, image=self.logo, bg="black")
        imagen_logo.pack(pady=10)
        
        # Texto para proceder
        texto_proceder = tk.Label(self.root, text="¿Cómo deseas proceder?", 
                                   font=("Arial", 20), fg="white", bg="black")
        texto_proceder.pack(pady=10)
        
        # Frame para los botones
        frame_boton = tk.Frame(self.root, bg="black", width=475, height=150)
        frame_boton.pack_propagate(False)
        frame_boton.pack(pady=20)
        
        # Cargar imágenes para los botones
        try:
            imagen_sesion = Image.open("imagenes/Iniciar.png")
            imagen_sesion_redimensionada = imagen_sesion.resize((65, 75))
            self.imagen_sesion_tk = ImageTk.PhotoImage(imagen_sesion_redimensionada)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de iniciar sesión: {e}")
            self.imagen_sesion_tk = None

        try:
            imagen_nuevo_usuario = Image.open("imagenes/Nuevo.png")
            imagen_nuevo_usuario_redimensionada = imagen_nuevo_usuario.resize((75, 75))
            self.imagen_nuevo_usuario_tk = ImageTk.PhotoImage(imagen_nuevo_usuario_redimensionada)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de nuevo usuario: {e}")
            self.imagen_nuevo_usuario_tk = None
        
        # Botón para iniciar sesión
        boton_iniciar_sesion = tk.Button(frame_boton, text="Iniciar sesión", font=("Arial", 10), 
                                         width=215, height=75, image=self.imagen_sesion_tk, compound="left", 
                                         bg="black", fg="white", command=self.ingresar)
        boton_iniciar_sesion.pack(side="left", padx=5)
        
        # Botón para nuevo usuario
        boton_nuevo_usuario = tk.Button(frame_boton, text="Nuevo usuario", font=("Arial", 10), 
                                        width=215, height=75, image=self.imagen_nuevo_usuario_tk, compound="left", 
                                        bg="black", fg="white", command=nuevo_usuario)
        boton_nuevo_usuario.pack(side="left", padx=5)
        
        # Cargar la imagen para el botón "Salir"
        try:
            imagen_salir = Image.open("imagenes/cerrarSesion.png")  # Asegúrate de que la ruta sea correcta
            imagen_salir_redimensionada = imagen_salir.resize((50, 50))
            self.imagen_salir_tk = ImageTk.PhotoImage(imagen_salir_redimensionada)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de salir: {e}")
            self.imagen_salir_tk = None
        
        # Botón para salir
        boton_salir = tk.Button(self.root, text="Salir", font=("Arial", 10), 
                                width=215, height=75, image=self.imagen_salir_tk, compound="left", 
                                bg="black", fg="white", command=self.salirdelPrograma)
        boton_salir.pack(pady=10)
        
    def salirdelPrograma(self):
        self.root.destroy()
        messagebox.showinfo("Salir", "Gracias por utilizar el sistema")
        
    def ingresar(self):
        resultado, usuario_nombre = ingreso_usuario()
        if resultado:
            messagebox.showinfo("Ingreso Exitoso", f"Bienvenido, {usuario_nombre}")
            self.root.destroy()
            show_loading_screen(usuario_nombre)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login = LoginWindow()
    login.run()
