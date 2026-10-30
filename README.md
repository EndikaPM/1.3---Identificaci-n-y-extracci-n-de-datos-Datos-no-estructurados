# 🦋 Bluesky Feed Extractor & LLM Analyzer

> Herramienta en Python para la extracción, limpieza de datos no estructurados de perfiles de Bluesky, almacenamiento persistente en MongoDB y análisis temático inteligente utilizando la API de Google Gemini.

## 📋 Tabla de Contenidos

 1. [Características Principales](#-características-principales-features)

 2. [Tecnologías Utilizadas](#-tecnologías-utilizadas)

 3. [Requisitos Previos](#-requisitos-previos)

 4. [Instalación y Configuración](#-instalación-y-configuración)

 5. [Guía de Uso](#-guía-de-uso)

 6. [Estructura del Proyecto](#-estructura-del-proyecto)

 7. [Cómo Contribuir](#-cómo-contribuir-contributing)

 8. [Autores y Agradecimientos](#-autores-y-agradecimientos)

9. [Licencia](#-licencia)

## ✨ Características Principales

* **Conexión Segura con AT Protocol:** Autenticación en Bluesky mediante variables de entorno y contraseñas de aplicación (*App Passwords*).

* **Extracción de Timelines:** Obtención configurable de publicaciones de perfiles públicos de Bluesky.

* **Procesamiento de Datos No Estructurados:**

  * Eliminación de enlaces y URLs (`http`, `https`, `www`).

  * Filtrado de emojis y caracteres especiales manteniendo la semántica y signos de puntuación del idioma.

  * Normalización de espacios y saltos de línea.

* **Persistencia en MongoDB:**

  * Almacenamiento organizado de las publicaciones en la colección `publicaciones`.

  * Guardado de los reportes generados por la LLM en la colección `analisis_cuentas`.

* **Análisis Inteligente con Google Gemini:** Generación de resúmenes temáticos y caracterización del perfil analizado usando la **Interactions API** y los modelos más recientes de Google GenAI.

* **Exportación Local:** Guardado automático del informe en un archivo `.txt` de fácil lectura.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+

* **Librerías principales:**

  * [`atproto`](https://github.com/MarshalX/atproto): SDK oficial para interactuar con la red de Bluesky / AT Protocol.

  * [`google-genai`](https://pypi.org/project/google-genai/): SDK oficial de Google para trabajar con los modelos de Gemini.

  * [`pymongo`](https://pymongo.readthedocs.io/): Conector oficial de Python para bases de datos MongoDB.

  * [`python-dotenv`](https://pypi.org/project/python-dotenv/): Gestión de credenciales y variables de entorno.

* **Base de Datos:** MongoDB local o remoto (compatible con Docker).

## 📌 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de contar con:

1. **Python 3.10** o superior instalado.

2. Una instancia de **MongoDB** en ejecución (localmente en `localhost:27017` o mediante un contenedor Docker).

3. Una cuenta de **Bluesky** (con Handle completo, ej: `usuario.bsky.social`).

4. Una **API Key de Google Gemini** obtenida desde [Google AI Studio](https://aistudio.google.com/).

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```
git clone https://github.com/tu-usuario/bluesky-gemini-analyzer.git
cd bluesky-gemini-analyzer

```

### 2. Crear y activar el entorno virtual

En Windows (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```

En Linux/macOS:

```
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Instalar las dependencias

```
pip install atproto pymongo google-genai python-dotenv

```

### 4. Configurar las variables de entorno (`.env`)

Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```
# Credenciales de Bluesky
BSKY_IDENTIFIER="tu_usuario.bsky.social"
BSKY_PASSWORD="tu_contraseña_de_aplicacion"

# API Key de Google Gemini
GEMINI_API_KEY="tu_gemini_api_key"

```

> **Nota:** Para mayor seguridad en Bluesky, genera una *App Password* desde **Ajustes > Avanzado > Contraseñas de aplicación**.

## 🚀 Guía de Uso

### Ejecutar el script principal

Para iniciar la extracción, procesamiento y análisis, ejecuta:

```
python main.py

```

### Ejemplo de flujo de ejecución

```
import os
from dotenv import load_dotenv
from atproto import Client
from google import genai

load_dotenv()

# 1. Conectar a Bluesky
client = Client()
client.login(os.environ.get('BSKY_IDENTIFIER'), os.environ.get('BSKY_PASSWORD'))

# 2. Obtener el feed
feed = client.get_author_feed(actor="publico.es", limit=10)

# 3. Analizar con Gemini (Interactions API)
cliente_gemi = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
interaction = cliente_gemi.interactions.create(
    model="gemini-4-argon",
    input="Analiza los siguientes feeds..."
)

print(interaction.output_text)

```

### Salida esperada

1. Mensaje de confirmación de conexión a Bluesky y MongoDB.

2. Inserción de documentos de publicaciones en la colección `publicaciones`.

3. Consulta a la API de Gemini mediante la Interactions API.

4. Generación de un archivo `.txt` local con el informe (ejemplo: `analisis_publico_es.txt`).

5. Inserción del informe en la colección `analisis_cuentas` de MongoDB.

## 📁 Estructura del Proyecto

```
1.3-DATOS_NO_ESTRUCTURADOS/
├── .venv/                      # Entorno virtual de Python
├── .env                        # Archivo de variables de entorno (no incluir en git)
├── .gitignore                  # Exclusiones de Git
├── main.py                     # Script principal de ejecución
├── analisis_publico_es.txt     # Ejemplo de reporte generado en texto plano
└── README.md                   # Documentación del proyecto

```

## 🤝 Cómo Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto:

1. Realiza un **Fork** del repositorio.

2. Crea una rama para tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).

3. Haz commit de tus cambios (`git commit -m 'Añade nueva funcionalidad'`).

4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).

5. Abre un **Pull Request**.

## 👥 Autores y Agradecimientos

* **Desarrollador / Alumno:** Proyecto realizado en el módulo de *Sistemas de Bid Data* por *Endika Pérez Mas*.

* **Herramientas de terceros:**

  * [Bluesky Social / AT Protocol](https://bsky.app) por la API de publicaciones.

  * [Google AI Studio](https://ai.google.dev/) por el acceso a la plataforma Gemini y la Interactions API.

  * [MongoDB](https://www.mongodb.com/) por la solución NoSQL de almacenamiento.

## 📄 Licencia

Este proyecto está distribuido bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para obtener más información.