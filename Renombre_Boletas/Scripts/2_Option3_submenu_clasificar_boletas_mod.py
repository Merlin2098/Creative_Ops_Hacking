import os
import subprocess
import time
import psutil

# Rutas de los scripts en el escritorio (Moficar manualmente cuando cambies la ubicación de la carpeta o quieras ejecutar el script desde otro equipo

ruta_crear_carpetas = r"C:\Users\Ricardo Uculmana\Documents\Scripts_Chamba\Scripts_Python\BOLETAS SAN SILVESTRE\crear_carpetas_mod.py"

ruta_mover_archivos = r"C:\Users\Ricardo Uculmana\Documents\Scripts_Chamba\Scripts_Python\BOLETAS SAN SILVESTRE\mover_archivos_mod.py"

# Obtener la ruta de la carpeta con los PDFs solicitando al usuario ingresarla manualmente en la consola
ruta_carpeta = input("Ingrese la ruta de la carpeta con los PDFs: ").strip()

# Validar que la ruta exista
if not os.path.isdir(ruta_carpeta):
    print("❌ Error: La carpeta no existe.")
    exit()

# Preguntar una vez si quiere clasificar por Año o Mes
# Primero se deben clasificar las boletas por año
#luego se vuelve a ejecutar el menu para clasificarlas por mes
modo = input("¿Desea clasificar por (1) Año o (2) Mes? Ingrese 1 o 2: ").strip()
if modo not in ["1", "2"]:
    print("❌ Opción inválida.")
    exit()

# Función para verificar el uso del CPU a fin de optimizar el uso de recursos
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Ejecutar el script de creación de carpetas con los parámetros
subprocess.run(["python", ruta_crear_carpetas, ruta_carpeta, modo])
cpu_usage = get_cpu_usage()
if cpu_usage > 50:
    print(f"⚠️ Uso de CPU alto ({cpu_usage}%). Esperando 5 segundos...")
    time.sleep(5)

# Ejecutar el script de mover archivos con los parámetros
subprocess.run(["python", ruta_mover_archivos, ruta_carpeta, modo])
cpu_usage = get_cpu_usage()
if cpu_usage > 50:
    print(f"⚠️ Uso de CPU alto ({cpu_usage}%). Esperando 5 segundos...")
    time.sleep(5)

print("✔️ Proceso completado.")
