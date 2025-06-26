import os
import sys
import shutil

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

archivos = [f for f in os.listdir(ruta_carpeta) if f.endswith(".pdf")]
archivos_movidos = 0

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

    ruta_destino = os.path.join(ruta_carpeta, nombre_carpeta)
    
    # Verificar si la carpeta existe antes de mover
    if os.path.isdir(ruta_destino):
        shutil.move(os.path.join(ruta_carpeta, archivo), os.path.join(ruta_destino, archivo))
        archivos_movidos += 1
    else:
        print(f"⚠️ Carpeta {ruta_destino} no encontrada, no se movió {archivo}.")

print(f"✔️ Se movieron {archivos_movidos} archivos.")
