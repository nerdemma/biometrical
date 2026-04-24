import os
import shutil

def leer_archivos_del_log(log_path):
    archivos = set()
    with open(log_path, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith("---") or not linea:
                continue
            partes = linea.split(" | ")
            if partes:
                archivos.add(partes[0])
    return archivos

def copiar_archivos(origen, destino, archivos_log):
    if not os.path.exists(destino):
        os.makedirs(destino)

    archivos_en_destino = set(os.listdir(destino))  # Solo una lectura de disco

    copiados = []
    omitidos = []

    archivos_en_origen = os.listdir(origen)
    total = len(archivos_en_origen)

    for idx, archivo in enumerate(archivos_en_origen, 1):
        origen_path = os.path.join(origen, archivo)

        if not os.path.isfile(origen_path):
            continue  # Ignorar subdirectorios

        if archivo in archivos_en_destino:
            omitidos.append((archivo, "Ya existe en destino"))
            continue

        if archivo in archivos_log:
            omitidos.append((archivo, "Registrado en log"))
            continue

        try:
            shutil.copy2(origen_path, os.path.join(destino, archivo))
            copiados.append(archivo)
        except Exception as e:
            omitidos.append((archivo, f"Error al copiar: {e}"))

        if idx % 1000 == 0:
            print(f"Procesados {idx}/{total} archivos...")

    # Resumen
    print("\nResumen final:")
    print(f"Total archivos en origen: {total}")
    print(f"Copiados: {len(copiados)}")
    print(f"Omitidos: {len(omitidos)}")

    return copiados, omitidos

def guardar_resumen(copiados, omitidos, ruta_archivo="resumen_copia.txt"):
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write("Archivos copiados:\n")
        for a in copiados:
            f.write(f"  - {a}\n")

        f.write("\nArchivos omitidos:\n")
        for a, motivo in omitidos:
            f.write(f"  - {a} ({motivo})\n")

    print(f"\nResumen guardado en: {ruta_archivo}")

def main():
    log_path = input("Ruta del archivo de log: ").strip()
    carpeta_origen = input("Ruta de la carpeta origen: ").strip()
    carpeta_destino = input("Ruta de la carpeta destino: ").strip()

    archivos_log = leer_archivos_del_log(log_path)
    copiados, omitidos = copiar_archivos(carpeta_origen, carpeta_destino, archivos_log)

    guardar = input("\n¿Deseás guardar un resumen en un archivo? (s/n): ").strip().lower()
    if guardar == 's':
        guardar_resumen(copiados, omitidos)

if __name__ == "__main__":
    main()
