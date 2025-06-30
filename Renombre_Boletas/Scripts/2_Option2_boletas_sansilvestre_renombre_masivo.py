import os
import pdfplumber
import shutil
import re

# Solicitar la ruta de la carpeta
# Trigger action: Request the user the folder path
carpeta = input("Ingrese la ruta de la carpeta con las boletas PDF: ")

# Asegurar que la carpeta existe
# Validate that the folder exists
if not os.path.isdir(carpeta):
    print("Error: La carpeta no existe.")
    exit()

# Función auxiliar para formatear el nombre del archivo
# Function to manipulate the file name
def formatear_nombre(nombre, mes_anio):
    """Elimina 'Mes de' y reemplaza ' del ' antes del año con '_'."""
    mes_anio = mes_anio.replace("Mes de ", "")  # Quitar "Mes de"
    mes_anio = re.sub(r"\sdel\s(\d{4})", r"_\1", mes_anio)  # "Diciembre del 2018" → "Diciembre_2018"
    return f"{nombre}_{mes_anio}.pdf"

# Función auxiliar para obtener un nombre único y evitar sobrescrituras
# Auxiliary Function to obtain unique names and avoid errors
def obtener_nombre_unico(ruta):
    """Si el archivo ya existe, agrega un sufijo _1, _2, etc."""
    if not os.path.exists(ruta):
        return ruta  # No hay conflicto, usar el nombre original

    base, ext = os.path.splitext(ruta)
    contador = 1
    nuevo_ruta = f"{base}_{contador}{ext}"

    while os.path.exists(nuevo_ruta):  # Buscar un nombre único
        contador += 1
        nuevo_ruta = f"{base}_{contador}{ext}"

    return nuevo_ruta

# Función para extraer el nombre correctamente
#Function to extract names in a correct way
def extraer_nombre(texto):
    """Extrae el nombre del texto, deteniéndose antes de 'Escala:' si existe."""
    match = re.search(r"NOMBRE:\s*(.*?)(\s+Escala:|\n|$)", texto)
    if match:
        return match.group(1).strip()
    return None

# Contador de archivos renombrados
# Count of files renamed
contador = 0

# Procesar cada archivo PDF en la carpeta
# Loop for process every file in the folder
for archivo in os.listdir(carpeta):
    if archivo.lower().endswith(".pdf"):
        ruta_pdf = os.path.join(carpeta, archivo)

        # Extraer texto del PDF
        # Extract text from the pdf
        nombre = None
        mes_anio = None
        texto = ""

        with pdfplumber.open(ruta_pdf) as pdf:
            if pdf.pages:
                texto = pdf.pages[0].extract_text() or ""

        # Si no hay texto, omitir el archivo
        # No text, skip file
        if not texto:
            print(f"No se pudo extraer texto de {archivo}")
            continue

        # Extraer el nombre
        # Extract file name
        nombre = extraer_nombre(texto)

        # Extraer mes y año
        #Extract month and year
        for linea in texto.split("\n"):
            if linea.startswith("Mes de "):
                mes_anio = linea.strip()
                break

        # Si no se encuentran los datos necesarios, omitir el archivo
        # If the file is empty, skip it
        if not nombre or not mes_anio:
            print(f"Datos insuficientes en {archivo}, no se renombrará.")
            continue

        # Formatear el nombre correctamente antes de renombrar
        nuevo_nombre = formatear_nombre(nombre, mes_anio)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)

        # Asegurar que el nuevo nombre sea único
        ruta_nueva = obtener_nombre_unico(ruta_nueva)

        # Intentar renombrar el archivo
        #Try to rename the file
        try:
            shutil.move(ruta_pdf, ruta_nueva)
            print(f"Renombrado: {archivo} → {os.path.basename(ruta_nueva)}")
            contador += 1
        except Exception as e:
            print(f"Error al renombrar {archivo}: {e}")

# Mostrar el número de archivos renombrados
# Show the number of renamed archives
print(f"\nTotal de archivos renombrados: {contador}")
