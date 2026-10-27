import itertools
import os
from dotenv import load_dotenv
from atproto import Client
from google import genai


def conectar_bluesky():
    load_dotenv()

    BSKY_IDENTIFIER = os.environ.get('BSKY_IDENTIFIER')
    BSKY_PASSWORD = os.environ.get('BSKY_PASSWORD')
    client = Client()
    client.login(BSKY_IDENTIFIER , BSKY_PASSWORD)
    print("Conexion con BlueSky exitosa!!!")
    return client

def cliente_gemini(fedd):
    cliente_gemi = genai.Client()

    interation = cliente_gemi.interactions.create(
        model="gemini-3.5-flash",
        input=fedd
    )
    return interation

def limpiar_texto(texto: str) -> str:
    """Aplica tratamientos al texto: elimina URLs, emojis y espacios extra."""
    texto_sin_url = re.sub(r'https?://\S+|www\.\S+', '', texto)

    texto_limpio = re.sub(r'[^\w\s,.:;!?ñÑáéíóúÁÉÍÓÚ-]', '', texto_sin_url)

    texto_final = " ".join(texto_limpio.split())

def obtener_timeline(client: Client, actor: str, limit: int = 10) -> list[str]:
    """Obtener el feed de un perfil y devuelve una lista con el textos limpios."""

    feed = client.get_author_feed(actor=actor, limit=limit)
    textos_procesados = []

    for item in feed.feed:
        texto_original = item.post.record.text

        
        texto_tratado = limpiar_texto(texto_original)

        
        if texto_tratado:
            textos_procesados.append(texto_tratado)

    return textos_procesados


def main():
    try:
        cliente_bsky = conectar_bluesky()

        actor = "publico.es"
        limit = 20

        publicaciones = obtener_timeline(cliente_bsky, actor=actor, limit=limit)

        print(f"\n--- Últimas {len(publicaciones)} publicaciones de @{actor} ---")
        for i, post in enumerate(publicaciones, 1):
            print(f"\n[{i}] {post}")

    except Exception as e:
        print(f"Error al conectar con Bluesky: {e}")


if __name__ == "__main__":
    main()
