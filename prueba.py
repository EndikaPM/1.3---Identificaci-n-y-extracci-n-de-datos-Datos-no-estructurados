import os
import re
from dotenv import load_dotenv
from atproto import Client


def conectar_bluesky():
    load_dotenv()

    BSKY_IDENTIFIER = os.environ.get('BSKY_IDENTIFIER')
    BSKY_PASSWORD = os.environ.get('BSKY_PASSWORD')

    if not BSKY_IDENTIFIER or not BSKY_PASSWORD:
        raise ValueError("Faltan credenciales en el archivo .env")

    client = Client()
    client.login(BSKY_IDENTIFIER, BSKY_PASSWORD)
    print("Conexión con Bluesky exitosa!!!")
    return client


def limpiar_texto(texto: str) -> str:
    """Aplica tratamientos al texto: elimina URLs, emojis y espacios extra."""
    # 1. Eliminar URLs (http://..., https://..., www....)
    texto_sin_url = re.sub(r'https?://\S+|www\.\S+', '', texto)

    # 2. Eliminar emojis y caracteres especiales (mantiene letras, números y puntuación básica)
    texto_limpio = re.sub(r'[^\w\s,.:;!?ñÑáéíóúÁÉÍÓÚ-]', '', texto_sin_url)

    # 3. Eliminar espacios múltiples sobrantes o saltos de línea extra
    texto_final = " ".join(texto_limpio.split())

    return texto_final


def obtener_timeline(client: Client, actor: str, limit: int = 10) -> list[str]:
    """Obtiene el feed de un perfil y devuelve una lista con los textos limpios."""
    # Obtener el feed usando la API de atproto
    feed = client.get_author_feed(actor=actor, limit=limit)

    textos_procesados = []

    # Iterar por cada elemento del feed
    for item in feed.feed:
        # Extraer el texto original del post
        texto_original = item.post.record.text

        # Aplicar los tratamientos de limpieza
        texto_tratado = limpiar_texto(texto_original)

        # Solo guardar si el texto no quedó vacío tras la limpieza
        if texto_tratado:
            textos_procesados.append(texto_tratado)

    return textos_procesados


def main():
    try:
        # 1. Conectar a Bluesky
        cliente_bsky = conectar_bluesky()

        # 2. Definir cuenta a consultar (sin el '@') y el límite de posts
        actor = "publico.es"
        limit = 5

        # 3. Obtener y procesar las publicaciones
        publicaciones = obtener_timeline(cliente_bsky, actor=actor, limit=limit)

        print(f"\n--- Últimas {len(publicaciones)} publicaciones de @{actor} ---")
        for i, post in enumerate(publicaciones, 1):
            print(f"\n[{i}] {post}")

    except Exception as e:
        print(f"Error durante la ejecución: {e}")


if __name__ == "__main__":
    main()