import os
import shutil

def obtener_nombre_unico(destino, nombre_archivo):
    """Genera un nombre único si el archivo ya existe en la carpeta destino."""
    nombre_base, extension = os.path.splitext(nombre_archivo)
    contador = 1
    nuevo_nombre = nombre_archivo
    
    while os.path.exists(os.path.join(destino, nuevo_nombre)):
        nuevo_nombre = f"{nombre_base}_{contador}{extension}"
        contador += 1
    
    return nuevo_nombre

def mover_archivos(carpeta_principal, eliminar_carpetas=False):
    """Mueve archivos desde subcarpetas a la carpeta principal, renombrando duplicados."""
    if not os.path.isdir(carpeta_principal):
        print("❌ La ruta ingresada no es válida.")
        return
    
    subcarpetas = [f for f in os.listdir(carpeta_principal) if os.path.isdir(os.path.join(carpeta_principal, f))]
    print(f"📁 Se encontraron {len(subcarpetas)} subcarpetas.")
    
    archivos_movidos = 0
    for subcarpeta in subcarpetas:
        subcarpeta_path = os.path.join(carpeta_principal, subcarpeta)
        
        for archivo in os.listdir(subcarpeta_path):
            archivo_origen = os.path.join(subcarpeta_path, archivo)
            if os.path.isfile(archivo_origen):
                nuevo_nombre = obtener_nombre_unico(carpeta_principal, archivo)
                destino = os.path.join(carpeta_principal, nuevo_nombre)
                
                try:
                    shutil.move(archivo_origen, destino)
                    archivos_movidos += 1
                    print(f"✅ Movido: {archivo} -> {nuevo_nombre}")
                except Exception as e:
                    print(f"❌ Error al mover {archivo}: {e}")

    carpetas_eliminadas = 0
    if eliminar_carpetas:
        for subcarpeta in subcarpetas:
            subcarpeta_path = os.path.join(carpeta_principal, subcarpeta)
            if not os.listdir(subcarpeta_path):  # Verifica si la carpeta está vacía
                os.rmdir(subcarpeta_path)
                carpetas_eliminadas += 1
                print(f"🗑️ Eliminada carpeta vacía: {subcarpeta}")
    
    archivos_restantes = len([f for f in os.listdir(carpeta_principal) if os.path.isfile(os.path.join(carpeta_principal, f))])
    print(f"✅ Proceso completado. Archivos movidos: {archivos_movidos}. Carpetas eliminadas: {carpetas_eliminadas}. Archivos restantes en la carpeta principal: {archivos_restantes}.")

if __name__ == "__main__":
    ruta = input("Ingrese la ruta de la carpeta principal: ")
    mover_archivos(ruta, eliminar_carpetas=True)  # Ahora elimina subcarpetas vacías sin preguntar
