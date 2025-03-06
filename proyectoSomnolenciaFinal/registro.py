import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql


# Variable global para almacenar la cédula del usuario
_ci_usuario = None  

# Variable global para almacenar el nombre del usuario
_nombre_usuario = None

def set_nombre_usuario(nombre):
    """Guarda el nombre del usuario verificado."""
    global _nombre_usuario
    _nombre_usuario = nombre

def get_nombre_usuario():
    """Retorna el nombre del usuario almacenado."""
    return _nombre_usuario

def set_ci_usuario(ci):
    """Guarda la cédula del usuario verificado."""
    global _ci_usuario
    _ci_usuario = ci

def get_ci_usuario():
    """Retorna la cédula del usuario almacenada."""
    return _ci_usuario



def ingreso_usuario():
    """
    Crea una ventana Toplevel para que el usuario ingrese sus credenciales.
    Utiliza wait_window para esperar a que se cierre la ventana y retorna True si el login es correcto,
    False en caso contrario.
    """
    resultado = False
    usuario_nombre = None
    
    ventana_ingreso = tk.Toplevel()
    ventana_ingreso.title("Ingreso de usuario")
    #ventana_ingreso.geometry("800x350")
    #ventana_ingreso.resizable(False, False)
    ventana_ingreso.attributes("-fullscreen", True)
    ventana_ingreso.config(bg="#3E4A61")
    
    #Etiqueta de bienvenida en la ventana
    etiqueta = tk.Label(ventana_ingreso, text="Por favor ingrese su Identificador y Contraseña", font=("Arial", 30), fg="white", bg="#3E4A61")
    etiqueta.pack(pady=50)
    
    # Panel izquierdo (Login)
    frame_login = tk.Frame(ventana_ingreso, bg="#6D8B8E", width=350, height=250, bd=5, relief="ridge")
    frame_login.place(relx=0.5, rely=0.5, anchor="center", x=-150)  # Centrado del frame
    
    # Contenedor interno para los campos de entrada
    frame_fields = tk.Frame(frame_login, bg="#6D8B8E", width=350, height=300)
    frame_fields.place(relx=0.5, rely=0.5, anchor="center")

    def on_focus_in(event, placeholder, entry_widget):
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, "end")
            entry_widget.config(fg="black")

    def on_focus_out(event, placeholder, entry_widget):
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder)
            entry_widget.config(fg="gray")
            
    def validar_ci_contrasena(event):
        if event.char == '':  # Permitir Backspace
            return None
        if not event.char.isdigit():
            return "break"
        if event.char == ' ':  # Bloquear espacios
            return "break"
        if not event.char.isalnum():  # Bloquear caracteres especiales
            return "break"

    def validar_contrasena(event):
        if event.char == '':  # Permitir Backspace
            return None
        if not event.char.isdigit():
            return "break"
        if event.char == ' ':  # Bloquear espacios
            return "break"
        if not event.char.isalnum():  # Bloquear caracteres especiales
            return "break"
    
    tk.Label(frame_fields, text="Usuario", bg="#6D8B8E", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    user_entry = tk.Entry(frame_fields, width=20, font=("Arial", 12), fg="gray")
    user_placeholder = "CI:171000000"
    user_entry.insert(0, user_placeholder)
    user_entry.bind("<FocusIn>", lambda event: on_focus_in(event, user_placeholder, user_entry))
    user_entry.bind("<FocusOut>", lambda event: on_focus_out(event, user_placeholder, user_entry))
    user_entry.bind("<KeyPress>", validar_ci_contrasena)
    user_entry.pack(pady=5)

    tk.Label(frame_fields, text="Contraseña", bg="#6D8B8E", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    pass_entry = tk.Entry(frame_fields, width=20, font=("Arial", 12), fg="gray")
    pass_placeholder = "Password"
    pass_entry.insert(0, pass_placeholder)
    pass_entry.bind("<FocusIn>", lambda event: on_focus_in(event, pass_placeholder, pass_entry))
    pass_entry.bind("<FocusOut>", lambda event: on_focus_out(event, pass_placeholder, pass_entry))
    pass_entry.bind("<KeyPress>", validar_contrasena)
    pass_entry.pack(pady=5)
    
    def verificar_campos():
        nonlocal resultado, usuario_nombre
        ci = user_entry.get()
        password = pass_entry.get()
        if ci == "" or password == "":
            messagebox.showwarning("Error", "Ningún campo puede estar vacío.")
            return
        resultado_login, nombre_usuario = verificar_ingreso_usuario(ci, password)
        if resultado_login:
            resultado = True
            usuario_nombre = nombre_usuario
            #set_nombre_usuario(nombre_usuario)  # Guardamos el nombre del usuario en memoria
            set_ci_usuario(ci)  # Guardamos la cédula del usuario en memoria
            ventana_ingreso.destroy()
        else:
            messagebox.showwarning("Error", "Usuario o contraseña incorrectos.")            
            
    login_button = tk.Button(frame_fields, text="Ingresar", bg="#E5AFAF", fg="black", font=("Arial", 12, "bold"), command=verificar_campos)
    login_button.pack(pady=10)
    
    # Panel derecho (Información adicional)
    frame_info = tk.Frame(ventana_ingreso, bg="#3E4A61", width=350, height=250, relief="ridge", bd=5)
    frame_info.place(relx=0.5, rely=0.5, anchor="center", x=250)

    tk.Label(frame_info, text="Bienvenido", bg="#3E4A61", fg="white", font=("Arial", 16, "bold")).pack(pady=15)
    tk.Label(frame_info, text="Accede a tu cuenta fácilmente", bg="#3E4A61", fg="white", font=("Arial", 12)).pack()
    tk.Label(frame_info, text="¿No tienes cuenta? Regístrate en nuevo usuario", bg="#3E4A61", fg="white", font=("Arial", 12)).pack()
    volver_button = tk.Button(frame_info, text="← Volver", bg="#3E4A61", fg="white", font=("Arial", 12, "underline"), command=ventana_ingreso.destroy)
    volver_button.pack(pady=10)
    
    ventana_ingreso.wait_window()
    return resultado, usuario_nombre

def nuevo_usuario():
    # Crear una nueva ventana para el registro
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de nuevo usuario")
    #ventana_registro.geometry("800x300")  # Aumento adicional de tamaño
    #ventana_registro.resizable(False, False)
    ventana_registro.attributes("-fullscreen", True)
    ventana_registro.config(bg="#2C3E50")  # Color de fondo oscuro relajante

    # Etiqueta en la parte superior
    etiqueta = tk.Label(ventana_registro, text="Por favor ingrese los siguientes datos para su registro", font=("Arial", 30), fg="white", bg="#2C3E50")
    etiqueta.pack(pady=10)
    
    #Indicacion de que solo se aceptan numeros en la cedula y en la contraseña
    etiqueta2 = tk.Label(ventana_registro, text="Solo se aceptan números en CI y Contraseña", font=("Arial", 14), fg="white", bg="#2C3E50")
    etiqueta2.pack(pady=10)


    frame_form = tk.Frame(ventana_registro, bg="#34495E", width=500, height=700, bd=5, relief="ridge")
    #frame_form.pack(pady=15)
    frame_form.place(relx=0.5, rely=0.5, anchor="center")  # Centrado del frame

    def validar_nombre(event):
        if event.char == '\x08':  # Permitir Backspace
            return None
        if not event.char.isalpha():
            return "break"
        if event.char == " ":
            return "break"

    def validar_ci_contrasena(event):
        if event.char == '\x08':  # Permitir Backspace
            return None
        if not event.char.isdigit():
            return "break"
        if event.char == " ":
            return "break"
        if not event.char.isalnum():
            return "break"
    
    def on_focus_in(event, placeholder, entry_widget):
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, "end")
            entry_widget.config(fg="white")

    def on_focus_out(event, placeholder, entry_widget):
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder)
            entry_widget.config(fg="gray")
    
    frame_top = tk.Frame(frame_form, bg="#34495E")
    #frame_top.pack()
    frame_top.grid(row=0, column=0, pady=10)  # Usando grid en lugar de pack
    
    tk.Label(frame_top, text="Nombre:", fg="white", bg="#34495E", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(frame_top, width=25, bg="black", fg="white", font=("Arial", 14))
    entry_nombre.insert(0, "Nombre")
    entry_nombre.bind("<FocusIn>", lambda event: on_focus_in(event, "Nombre", entry_nombre))
    entry_nombre.bind("<FocusOut>", lambda event: on_focus_out(event, "Nombre", entry_nombre))
    entry_nombre.bind("<KeyPress>", validar_nombre)
    #entry_nombre.grid(row=0, column=1, padx=5, pady=5)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame_top, text="CI:", fg="white", bg="#34495E", font=("Arial", 14)).grid(row=0, column=2, padx=5, pady=5)
    entry_ci = tk.Entry(frame_top, width=25, bg="black", fg="white", font=("Arial", 14))
    entry_ci.insert(0, "CI:171000000")
    entry_ci.bind("<FocusIn>", lambda event: on_focus_in(event, "CI:171000000", entry_ci))
    entry_ci.bind("<FocusOut>", lambda event: on_focus_out(event, "CI:171000000", entry_ci))
    entry_ci.bind("<KeyPress>", validar_ci_contrasena)
    entry_ci.grid(row=0, column=3, padx=5, pady=5)

    #tk.Label(frame_form, text="Contraseña:", fg="white", bg="#34495E", font=("Arial", 14)).pack()
    tk.Label(frame_form, text="Contraseña:", fg="white", bg="#34495E", font=("Arial", 14)).grid(row=1, column=0, columnspan=4, pady=10)
    
    frame_password = tk.Frame(frame_form, bg="#34495E")
    #frame_password.pack()
    frame_password.grid(row=2, column=0, columnspan=4, pady=10)
    
    entry_contrasena = tk.Entry(frame_password, width=35, show="*", bg="black", fg="white", font=("Arial", 14))
    entry_contrasena.insert(0, "Contraseña")
    entry_contrasena.bind("<FocusIn>", lambda event: on_focus_in(event, "Contraseña", entry_contrasena))
    entry_contrasena.bind("<FocusOut>", lambda event: on_focus_out(event, "Contraseña", entry_contrasena))
    entry_contrasena.bind("<KeyPress>", validar_ci_contrasena)
    entry_contrasena.grid(row=0, column=0, pady=5)
    
    def toggle_password():
        if entry_contrasena.cget('show') == "*":
            entry_contrasena.config(show="")
        else:
            entry_contrasena.config(show="*")
    
    toggle_button = tk.Button(frame_password, text="👁", command=toggle_password, bg="#E74C3C", fg="white", relief="ridge", font=("Arial", 14))
    toggle_button.grid(row=0, column=1, padx=5)
    
    def verificar_campos():
        if entry_nombre.get() == "" or entry_nombre.get() == "Nombre":
            messagebox.showwarning("Error", "El campo 'Nombre' no puede estar vacío.")
            return
        if entry_ci.get() == "" or entry_ci.get() == "CI:171000000":
            messagebox.showwarning("Error", "El campo 'CI' no puede estar vacío.")
            return
        if entry_contrasena.get() == "" or entry_contrasena.get() == "Contraseña":
            messagebox.showwarning("Error", "El campo 'Contraseña' no puede estar vacío.")
            return
        
        nombre = entry_nombre.get()
        ci = entry_ci.get()
        contrasena = entry_contrasena.get()
        
        if verificar_ci_existente(ci):
            messagebox.showwarning("Error", "El CI ya está registrado.")
            return
        
        guardar_usuario(nombre, ci, contrasena)
        messagebox.showinfo("Registro Exitoso", "El usuario ha sido registrado correctamente.")
        ventana_registro.destroy()
    
    frame_buttons = tk.Frame(frame_form, bg="#34495E")
    #frame_buttons.pack(pady=10)
    frame_buttons.grid(row=3, column=0, columnspan=4, pady=10)
    
    boton_guardar = tk.Button(frame_buttons, text="Registrar", command=verificar_campos, bg="#27AE60", fg="white", relief="ridge", font=("Arial", 14))
    boton_guardar.grid(row=0, column=0, padx=5)
    
    boton_volver = tk.Button(frame_buttons, text="Volver", command=ventana_registro.destroy, bg="#E74C3C", fg="white", relief="ridge", font=("Arial", 14))
    boton_volver.grid(row=0, column=1, padx=5)

    ventana_registro.mainloop()



def obtener_conexion():
    """
    Establece una conexión a la base de datos PostgreSQL en Railway.
    """
    conn = psycopg2.connect(
        host="mainline.proxy.rlwy.net",  # Dirección del servidor de Railway
        dbname="railway",  # Nombre de la base de datos (verifícalo en el panel de Railway)
        user="postgres",  # Usuario predeterminado en Railway (o el que hayas creado)
        password="yZKptOSfoKPZkqdJraujkIOTlFmuDCQP",  # Contraseña proporcionada por Railway
        port=57794  # Puerto especificado por Railway
    )
    return conn

def verificar_ci_existente(ci):
    try:
        # Obtener la conexión
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Consulta SQL para verificar si el CI existe
        query = sql.SQL("SELECT 1 FROM usuarios WHERE ci = %s")
        cursor.execute(query, (ci,))

        # Comprobar si se encontró algún registro
        existe = cursor.fetchone()  # Devuelve None si no encuentra ningún registro

        # Cerrar la conexión
        cursor.close()
        conn.close()

        if existe:
            return True  # El CI ya existe
        else:
            return False  # El CI no existe
    except Exception as e:
        print(f"Error al verificar el CI: {e}")
        return False  # Asumimos que no existe en caso de error

def guardar_usuario(nombre, ci, contrasena):
    try:
        # Obtener la conexión
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Consulta SQL para insertar los datos
        query = sql.SQL("INSERT INTO usuarios (nombre, ci, contrasena) VALUES (%s, %s, %s)")

        # Ejecutar la consulta
        cursor.execute(query, (nombre, ci, contrasena))

        # Confirmar la transacción
        conn.commit()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        print("Usuario registrado correctamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar el usuario: {e}")
      
        
def verificar_ingreso_usuario(ci, contrasena):
    try:
        # Obtener la conexión
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Consulta SQL para verificar si el CI y la contraseña son correctos
        query = sql.SQL("SELECT nombre FROM usuarios WHERE ci = %s AND contrasena = %s")
        cursor.execute(query, (ci, contrasena))

        # Obtener el nombre del usuario si existe
        usuario = cursor.fetchone()  # Devuelve None si no encuentra ningún registro
        
        # Guardar el nombre del usuario en memoria
        set_nombre_usuario(usuario[0])
        

        # Cerrar la conexión
        cursor.close()
        conn.close()

        if usuario:
            return True, usuario[0]  # El usuario existe y la contraseña es correcta
        else:
            return False, None  # CI o contraseña incorrectos
    except Exception as e:
        print(f"Error al verificar el ingreso del usuario: {e}")
        return False, None  # Asumimos que el ingreso es incorrecto en caso de error