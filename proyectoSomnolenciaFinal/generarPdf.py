from fpdf import FPDF
import psycopg2

# Función para obtener los resultados de la base de datos filtrados por cédula
def obtener_datos_por_ci(ci):
    try:
        # Conexión a la base de datos
        connection = psycopg2.connect(
            host="mainline.proxy.rlwy.net",  # Dirección del servidor de Railway
            dbname="railway",  # Nombre de la base de datos
            user="postgres",  # Usuario
            password="yZKptOSfoKPZkqdJraujkIOTlFmuDCQP",  # Contraseña
            port=57794  # Puerto
        )
        cursor = connection.cursor()

        # Consulta SQL para obtener solo los 6 datos necesarios
        query = """
        SELECT ci, nombre, porcentaje_ojos_cerrados, t_promedio, conclusion, fecha
        FROM supertabla
        WHERE ci = %s
        """
        cursor.execute(query, (ci,))  # Pasamos la cédula como parámetro
        datos = cursor.fetchall()

        return datos

    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()


# Función para generar el PDF con los resultados filtrados por cédula
def generar_pdf(ci):
    # Obtener los datos de la base de datos
    datos = obtener_datos_por_ci(ci)

    if not datos:
        print("No se encontraron datos para la cédula proporcionada.")
        return

    pdf = FPDF(orientation='L', unit='mm', format='A4')  # Establecer la página en horizontal (L)
    pdf.add_page()

    # Establecer fuentes
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Resultados del Test según el CI: {ci}', 0, 1, 'C')

    # Ajustar la posición X para centrar la tabla un poco más a la derecha
    #pdf.set_x(30)  # Ajusta este valor para mover la tabla más a la derecha o izquierda

    # Crear la cabecera de la tabla
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(25, 10, 'CI', border=1, align='C')
    pdf.cell(20, 10, 'Nombre', border=1, align='C')
    pdf.cell(50, 10, 'Porcentaje Ojos Cerrados', border=1, align='C')
    pdf.cell(40, 10, 'Promedio T', border=1, align='C')
    pdf.cell(30, 10, 'Fecha', border=1, align='C')
    pdf.cell(80, 10, 'Conclusión', border=1, align='C')
    pdf.ln()

    # Rellenar la tabla con los datos
    pdf.set_font('Arial', '', 10)
    for row in datos:
        pdf.cell(25, 10, str(row[0]), border=1, align='C')
        pdf.cell(20, 10, row[1], border=1, align='C')
        pdf.cell(50, 10, str(row[2]), border=1, align='C')
        pdf.cell(40, 10, str(row[3]), border=1, align='C')
        pdf.cell(30, 10, str(row[5]), border=1, align='C')  # Convertimos la fecha en string
        pdf.multi_cell(80, 10, row[4], border=1, align='L')  # Alineación a la izquierda para la conclusión

        # Evitar usar `ln()` después de `multi_cell()` porque multi_cell maneja el salto de línea
    # Guardar el archivo PDF
    pdf.output(f"resultados_test_CI_{ci}.pdf")
    print(f"PDF generado exitosamente para el CI: {ci}")
