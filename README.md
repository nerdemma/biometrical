# Biometrical 📸

**Biometrical** es una herramienta de línea de comandos (CLI) de alto rendimiento diseñada para la clasificación automatizada de grandes volúmenes de fotografías. Utiliza visión artificial para separar imágenes con rostros humanos de aquellas que no los contienen, optimizando drásticamente la gestión de activos visuales.

## 🚀 Características Principales

- **Procesamiento Multihilo (Multi-thread)**: Capacidad para procesar múltiples imágenes en paralelo, aprovechando al máximo los núcleos de la CPU para reducir los tiempos de ejecución.
- **Detección Facial Eficiente**: Clasificación precisa mediante el uso de descriptores biométricos.
- **Gestión desde Terminal**: Interfaz ligera ideal para servidores, automatización y flujos de trabajo rápidos.
- **Backups Integrados**: Realiza copias de seguridad de tus archivos de forma segura durante el procesamiento.
- **Multiplataforma**: Testeado y totalmente funcional en **Linux** y **Windows**.

## 🛠️ Requisitos Previos

- **Lenguajes**: Node.js (v16.0.0+) o Python (3.8+)
- **Base de Datos**: MongoDB (v5.0+)
- **Dependencias Core**: OpenCV, Pillow, dotenv.
- **Hardware Mínimo**: Optimizado para funcionar desde 2 núcleos en adelante.

## 📦 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/nerdemma/biometrical.git](https://github.com/nerdemma/biometrical.git)
   cd biometrical