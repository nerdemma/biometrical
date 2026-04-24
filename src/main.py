import os
import shutil
import cv2
import sys
import multiprocessing
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# == Parámetros y configuración ==
HAAR_CASCADE_PATH = 'haarcascade_frontalface_default.xml'
SUPPORTED_EXT = ('.jpg', '.jpeg', '.png')
TEMP_RESIZE_DIM = 480 

# Nombres de subcarpetas dentro del directorio de destino
FACES_SUBDIR = 'faces'
OBJECTS_SUBDIR = 'objects'
LOGS_SUBDIR = 'logs'

# === Cargar detector de caras Haar Cascade de OpenCV ===
try:
    detector = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    if detector.empty():
        raise IOError(f"❌ Error: El archivo '{HAAR_CASCADE_PATH}' no se pudo cargar o está vacío.")
    print("✅ Detector de caras Haar Cascade de OpenCV cargado correctamente.")
except IOError as e:
    print(e)
    sys.exit(1)

# ---
## Funciones de ayuda

def resize_for_detection(image, max_dim):
    """
    Redimensiona la imagen para que su dimensión más grande sea 'max_dim'.
    Evita que las dimensiones resultantes sean cero o negativas.
    """
    h, w = image.shape[:2]
    
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        
        # Asegurarse de que las dimensiones sean válidas
        if new_w <= 0 or new_h <= 0:
            raise ValueError("Las dimensiones de redimensionamiento calculadas no son válidas.")
        
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return image

def get_all_images(root_dir):
    """Obtiene todas las imágenes de un directorio de forma recursiva."""
    root_path = Path(root_dir)
    return [str(p) for p in root_path.rglob('*') if p.suffix.lower() in SUPPORTED_EXT]

# ---
## Lógica principal de procesamiento

def process_image(file_path, dest_root):
    """
    Procesa una imagen individual, la clasifica y la mueve a su destino.
    Devuelve un mensaje de estado y una entrada de log.
    """
    filename = Path(file_path).name
    dest_path_faces = Path(dest_root) / FACES_SUBDIR / filename
    dest_path_objects = Path(dest_root) / OBJECTS_SUBDIR / filename

    # Si la imagen ya está en el destino, no la procesa de nuevo.
    if dest_path_faces.exists() or dest_path_objects.exists():
        return f"[{filename}] ⚠️ Archivo ya en destino, saltando.", None

    original_image = cv2.imread(file_path)
    if original_image is None:
        return f"[{filename}] ❌ Error al cargar la imagen.", None
    
    h, w = original_image.shape[:2]

    try:
        # Redimensionar temporalmente para el análisis
        resized_image = resize_for_detection(original_image, TEMP_RESIZE_DIM)
        
        # Convertir a escala de grises para la detección (más eficiente)
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        
        # Detectar caras usando Haar Cascade
        faces = detector.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Determinar destino y mover el archivo
        if len(faces) > 0:
            dest_dir = Path(dest_root) / FACES_SUBDIR
            resultado = f"Cara(s) detectada(s): {len(faces)}"
        else:
            dest_dir = Path(dest_root) / OBJECTS_SUBDIR
            resultado = "Sin rostro"
        
        dest_path = dest_dir / filename
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(file_path, dest_path)

        return f"[{filename}] ✅ Procesado: {resultado} | Resolución original: {w}x{h}", resultado

    except (cv2.error, ValueError, Exception) as e:
        return f"[{filename}] ⚠️ Error de procesamiento: {e}", None

# ---
## Bucle principal del script

def main():
    print("📁 Ingresa el directorio de origen (se buscará recursivamente):")
    source_root = input("Ruta de origen: ").strip('"').strip()

    if not Path(source_root).is_dir():
        print("❌ Error: La ruta de origen no es válida.")
        sys.exit(1)

    print("➡️ Ingresa el directorio de destino:")
    dest_root = input("Ruta de destino: ").strip('"').strip()
    
    # Crear las subcarpetas de destino y logs
    for subdir in [FACES_SUBDIR, OBJECTS_SUBDIR, LOGS_SUBDIR]:
        os.makedirs(Path(dest_root) / subdir, exist_ok=True)

    # Generar un registro de log único en la carpeta de destino
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = Path(dest_root) / LOGS_SUBDIR / f'procesamiento_{timestamp}.log'

    image_files = get_all_images(source_root)
    total_files = len(image_files)

    if not image_files:
        print("⚠️ No se encontraron imágenes en el directorio proporcionado.")
        sys.exit(0)

    # Definir el número de trabajadores para la piscina de hilos
    max_workers = max(1, multiprocessing.cpu_count() - 1)
    print(f"\n🔍 Se encontraron {total_files} imágenes. Usando {max_workers} hilos. Iniciando procesamiento...\n")

    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"\n--- Procesamiento iniciado: {datetime.now()} ---\n")

        processed_count = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(process_image, file, dest_root): file for file in image_files}

            for future in as_completed(future_to_file):
                result, log_entry = future.result()
                if log_entry:
                    log.write(f"{result}\n")
                
                # Actualizar la barra de progreso
                processed_count += 1
                progress = (processed_count / total_files) * 100
                sys.stdout.write(f"\rProgreso: [{processed_count}/{total_files}] {progress:.2f}% completado.  ")
                sys.stdout.flush()

        sys.stdout.write("\n")
        sys.stdout.flush()

        log.write(f"--- Procesamiento finalizado: {datetime.now()} ---\n")

if __name__ == "__main__":
    main()