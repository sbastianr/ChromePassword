import psutil
import os


def detectar_usb():
    """Detecta la primera unidad extraíble (USB) conectada al sistema."""
    for particion in psutil.disk_partitions():
        if 'removable' in particion.opts:
            return particion.mountpoint
    return None


def guardar_en_usb(contenido, nombre_archivo="mi_archivo.txt"):
    # Detectar unidad de la memoria USB
    ruta_usb = detectar_usb()

    if ruta_usb:
        # Construir la ruta completa
        ruta_completa = os.path.join(ruta_usb, nombre_archivo)

        try:
            # Guardar el archivo en la memoria USB
            with open(ruta_completa, "w") as archivo:
                archivo.write(contenido)
            print(f"Archivo guardado exitosamente en {ruta_completa}")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
    else:
        print("No se detectó ninguna memoria USB conectada.")

