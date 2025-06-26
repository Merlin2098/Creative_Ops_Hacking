#Importa las librerias necesarias para procesar pdf y monitorear el uso de recursos del sistema
#Import libraries for pdf process and measure the use of resources

import os
import pdfplumber
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import time

#Función que extrae los datos requeridos de cada pdf
#Function that extracts the required data from each pdf
def extract_details(pdf_path):
    document_number = None
    apenom = None
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    if 'L.E / DNI' in line or 'CARNÉ EXT.' in line:
                        parts = line.split('-')
                        if len(parts) > 1:
                            document_number = parts[1].strip().split()[0]
                    if 'Apellidos y nombres:' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            apenom = parts[1].strip()
                if document_number and apenom:
                    return document_number, apenom
    except Exception as e:
        print(f"Error procesando '{pdf_path}': {e}")
    return document_number, apenom

#Función renombra el pdf en base a los valores retornados por la función anterior
#Function that renames the pdf file using the values obtained in the previous function

def rename_pdf(old_path, folder_path):
    document_number, apenom = extract_details(old_path)
    if document_number and apenom:
        apenom_normalized = apenom.replace(' ', '_')
        new_filename = f"{document_number}_{apenom_normalized}_ALTA_SUNAT.pdf"
        new_path = os.path.join(folder_path, new_filename)

        # Manejar nombres duplicados
        if os.path.exists(new_path):
            base, ext = os.path.splitext(new_filename)
            count = 1
            while True:
                new_filename = f"{base}_{count}{ext}"
                new_path = os.path.join(folder_path, new_filename)
                if not os.path.exists(new_path):
                    break
                count += 1

        try:
            os.rename(old_path, new_path)
            return f"Renombrado '{old_path}' a '{new_filename}'"
        except Exception as e:
            return f"Error al renombrar '{old_path}': {e}"
    else:
        return f"Detalles no encontrados en '{old_path}'"

#Aqui se ejecuta el bucle para renombrar todos los pdf presentes en la carpeta de trabajo
#Here we execute the loop for renaming each pdf file in the folder
def rename_pdfs_in_folder_with_performance_check(folder_path, max_workers=4):
    mensajes = []  # Lista para almacenar mensajes
    renamed_count = 0

    while True:
        try:
            # Medir el rendimiento actual del sistema. Diseñado para trabajar en la IDLE de Replit
            # Measure the actual system performance. Designed for working in Replit IDLE
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            # Definir umbrales de rendimiento
            # Define the limits for performance
            CPU_THRESHOLD = 80
            MEMORY_THRESHOLD = 90

            # Verificar si se superan los umbrales
            if cpu_percent > CPU_THRESHOLD or memory_percent > MEMORY_THRESHOLD:
                print("Rendimiento del sistema bajo. Pausando la ejecución...")
                time.sleep(10)  # Pausa durante 10 segundos antes de volver a verificar
                continue

            # Si el rendimiento es aceptable, continuar con la renombrado de archivos PDF
            #If the performance is good, the pdf rename will continue
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for filename in os.listdir(folder_path):
                    if filename.endswith('.pdf'):
                        old_path = os.path.join(folder_path, filename)
                        futures.append(executor.submit(rename_pdf, old_path, folder_path))

                for future in as_completed(futures):
                    mensajes.append(future.result())
                    if "Renombrado" in future.result():
                        renamed_count += 1

            break  # Salir del bucle while cuando termine el procesamiento. Exit loop after the process finishes

        except Exception as e:
            mensajes.append(f"Error inesperado: {e}")
            break  # Salir del bucle while en caso de error. Exit buffe in case of error

    mensajes.append(f"Total de archivos renombrados: {renamed_count}")

    # Imprimir todos los mensajes del buffer. Busca imitar el application screen updating the excel
    # Print all the console messages of the buffer. Similar to the application screen updating in excel
    for mensaje in mensajes:
        print(mensaje)


#El gatillador del programa es la acción de ingresar la ruta de la carpeta de trabajo por parte del usuario
#The trigger of this program is the action of insert the folder path
if __name__ == "__main__":
    try:
        # Solicitar al usuario la ruta de la carpeta que contiene los archivos PDF
        folder_path = input("Ingrese la ruta de la carpeta que contiene los archivos PDF: ")

        # Renombrar archivos PDF con monitoreo de rendimiento
        rename_pdfs_in_folder_with_performance_check(folder_path)

    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
