# Proyecto-Interfaces-y-Multimedia
# 🚀Sistema de Monitoreo de Somnolencia en Entornos Académicos

## 📌Descripción
Este proyecto implementa un sistema basado en visión por computadora para el monitoreo de somnolencia en entornos académicos. Utiliza el índice PERCLOS, actividades cognitivas y un test de atencion sostenida CPT para evaluar la falta de atencion y el nivel de somnolencia en los estudiantes.

## ✨Características
- 🔍Análisis en tiempo real del índice PERCLOS.
- 👀Medición de PERCLOS mediante visión artificial.
- 🧠Integración de pruebas psicomotoras y cognitivas.
- 💾Almacenamiento de datos en una base de datos PostgreSQL.
- 📂Estructura modular para la ejecución de actividades secuenciales.

## 🛠️ Tecnologías Utilizadas
- 🖥️**Lenguaje**: Python 3.10.0
- 📚**Bibliotecas**: OpenCV, MediaPipe, Tkinter, Psycopg2, Numpy.
- 🗄️**Base de Datos**: PostgreSQL
- 💻 **Entorno**: Windows 10

## Instalación
### 1️⃣ 📥Clona el repositorio:
   ```bash
   git clone https://github.com/STAlinRoche/proyectoInterfacesSomnolencia.git
   ```
### 2️⃣ 📂Accede al directorio del proyecto:
   ```bash
   cd proyectoInterfacesSomnolencia
   ```
### 3️⃣ 🏗️Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate  # En Windows
   ```
### 4️⃣ 🐍Instala la versión de Python 3.10.0.
   
### 5️⃣ 📦Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
### 6️⃣ 🗄️ Configura la base de datos PostgreSQL y actualiza los parámetros en `tablaBD.txt`.

##
## ▶️ Uso
Ejecuta el sistema con:
```bash
python login.py
```

## 📂 Estructura del Proyecto
```
/
├── proyectoSomnolenciaFinal/
│   ├── imagenes/
│   ├── activities.py
│   ├── ayudas.py
│   ├── drowsiness_monitor.py
│   ├── generarPdf.py
│   ├── login.py
│   ├── main_interface.py
│   ├── pantallaCarga.py
│   ├── Ractvidades.py
│   ├── registro.py
│   ├── results.py
│   ├── sleep_test.py
│   ├── tablaBD.txt
│   ├── requirements.txt
├── README.md
```

## 🤝 Contribución
1. 🍴Haz un fork del repositorio.
2. 🌱Crea una nueva rama:
   ```bash
   git checkout -b feature-nueva
   ```
3. 🛠️Realiza tus cambios y haz commit:
   ```bash
   git commit -m "Agregado nueva funcionalidad"
   ```
4. 📤Sube tus cambios:
   ```bash
   git push origin feature-nueva
   ```
5. 🔄Abre un Pull Request.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

## 📩Contacto
Para consultas o colaboraciones, puedes contactarme en: sfroche@espe.edu.ec

