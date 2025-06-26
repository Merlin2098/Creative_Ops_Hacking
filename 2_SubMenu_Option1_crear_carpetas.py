import os
import sys

# Obtener los parámetros de entrada
if len(sys.argv) < 3:
    print("❌ Error: Parámetros insuficientes.")
    exit()

ruta_carpeta = sys.argv[1]
modo = sys.argv[2]

# Validar la ruta
if not os.path.isdir(ruta_carpeta):
    print("❌ Error: La ruta de la carpeta no es válida.")
    exit()

# Obtener los nombres de los archivos en la carpeta
archivos = [f for f in os.listdir(ruta_carpeta) if f.endswith(".pdf")]
carpetas_creadas = set()

for archivo in archivos:
    partes = archivo.split("_")
    if len(partes) < 3:
        continue

    mes = partes[-2]  # Ejemplo: "Marzo"
    anio = partes[-1].replace(".pdf", "")  # Ejemplo: "2022"

    if modo == "1":
        nombre_carpeta = anio
    elif modo == "2":
        nombre_carpeta = f"{mes}_{anio}"
    else:
        print("❌ Opción inválida.")
        exit()

    ruta_carpeta_nueva = os.path.join(ruta_carpeta, nombre_carpeta)
    
    # Crear la carpeta si no existe
    if nombre_carpeta not in carpetas_creadas:
        os.makedirs(ruta_carpeta_nueva, exist_ok=True)
        carpetas_creadas.add(nombre_carpeta)

print(f"✔️ Se crearon las carpetas: {', '.join(carpetas_creadas)}")
