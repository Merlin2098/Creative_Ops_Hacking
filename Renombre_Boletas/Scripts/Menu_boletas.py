#Este script
import os
import subprocess

# Funcion para validar que el script este en la ruta proporcionada
def ejecutar_script(script_path):
    if os.path.exists(script_path):
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: No se encontró el script en {script_path}")

# Definir las rutas de los scripts. Modificar según su propio equipo
script_extraer_boletas = r"C:\Users\User\Documents\Scripts_Chamba\Scripts_Python\BOLETAS SAN SILVESTRE\1_boletas_extrar_carpeta_mod.py"
script_renombrar_boletas = r"C:\Users\User\Documents\Scripts_Chamba\Scripts_Python\BOLETAS SAN SILVESTRE\2_boletas_sansilvestre_renombre_masivo.py"
script_clasificar_boletas = r"C:\Users\User\Documents\Scripts_Chamba\Scripts_Python\BOLETAS SAN SILVESTRE\3_menu_clasificar_boletas_mod.py"

#Inicio del bucle para mostrar las opciones del menu en la consola
while True:
    print("\nBienvenido al menú de boletas. ¿Qué operación desea realizar?")
    print("1) Extraer las boletas de cada carpeta")
    print("2) Renombrar las boletas (PDF)")
    print("3) Clasificar las boletas")
    print("4) Salir")
    
    opcion = input("Ingrese el número de la opción deseada: ").strip()
# Condicional para ejecutar cada script definido en base a las rutas de archivo brindadas al inicio del codigo
    if opcion == "1":
        ejecutar_script(script_extraer_boletas)
    elif opcion == "2":
        ejecutar_script(script_renombrar_boletas)
    elif opcion == "3":
        ejecutar_script(script_clasificar_boletas)
    elif opcion == "4":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida, por favor intente nuevamente.")

#Loop para que el usuario pueda realizar otra operación y no tenga que ejecutar nuevamente todo el script

    continuar = input("¿Desea realizar otra operación? (S/N): ").strip().upper()
    if continuar != "S":
        print("Finalizando el programa...")
        break
