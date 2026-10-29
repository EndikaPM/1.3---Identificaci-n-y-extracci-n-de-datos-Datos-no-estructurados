import itertools
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from atproto import Client
from google import genai
from pymongo import MongoClient


def conectar_bluesky():
    load_dotenv()

    BSKY_IDENTIFIER = os.environ.get('BSKY_IDENTIFIER')
    BSKY_PASSWORD = os.environ.get('BSKY_PASSWORD')
    
    client = Client()
    client.login(BSKY_IDENTIFIER , BSKY_PASSWORD)
    print("Conexion con BlueSky exitosa!!!")
    return client

def conectar_mongo():
    
    client_mongo = MongoClient("mongodb://root:root@localhost:27017")
    
    db = client_mongo['bluesky_db']
    
    print("Conexión con MongoDB exitosa!!!")
    return db

def cliente_gemini(textos_feed, actor):
    cliente_gemi = genai.Client()

    feed_unificado = "\n- ".join(textos_feed)

    prompt = (
        f"Analiza las siguientes publicaciones pertenecientes a la cuenta @{actor} de Bluesky.\n"
        f"Indica en texto plano de qué trata la cuenta y cuáles son sus temas principales:\n\n"
        f"- {feed_unificado}"
    )

    response = cliente_gemi.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
                        
    return response.text

def limpiar_texto(texto):
    texto_sin_url = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto_limpio = re.sub(r'[^\w\s,.:;!?ñÑáéíóúÁÉÍÓÚ-]', '', texto_sin_url)
    texto_final = " ".join(texto_limpio.split())
    return texto_final

def obtener_timeline(client, db_mongo ,actor, limit = 10):
    coleccion_posts = db_mongo['publicaciones']
    feed = client.get_author_feed(actor=actor, limit=limit)
    textos_procesados = []
    documentos_a_insertar = []

    for item in feed.feed:
        
        texto_original = item.post.record.text
        texto_tratado = limpiar_texto(texto_original)

        if texto_tratado:
            textos_procesados.append(texto_tratado)

            doc = {
                "uri_post": item.post.uri,
                "autor": actor,
                "texto_original": texto_original,
                "texto_limpio": texto_tratado,
                "fecha_creacion": item.post.record.created_at,
                "fecha_captura": datetime.now()
            }
            documentos_a_insertar.append(doc)
        
    if documentos_a_insertar:
        resultado = coleccion_posts.insert_many(documentos_a_insertar)
        print(f"Se insertaron {len(resultado.inserted_ids)} publicaciones en MongoDB.")
    else:
        print("No se encontraron publicaciones para guardar.")

    return textos_procesados

def guardar_analisis(db_mongo, actor, publicaciones, analisis):
    nombre_archivo = f"analisis_{actor.replace('.', '_')}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"ANÁLISIS DE LA CUENTA @{actor}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n\n")
        f.write(analisis)
    
    print(f"Análisis guardado localmente en '{nombre_archivo}'.")

    coleccion_analisis = db_mongo['analisis_cuentas']
    doc_analisis = {
        "autor": actor,
        "total_posts_analizados": len(publicaciones),
        "analisis_llm": analisis,
        "fecha_analisis": datetime.now()
    }
    
    res = coleccion_analisis.insert_one(doc_analisis)
    print(f"Análisis guardado en Mongo con ID: {res.inserted_id}")

def main():
    try:
        load_dotenv()

        cliente_bsky = conectar_bluesky()
        db_mongo = conectar_mongo()

        actor = "publico.es"
        limit = 20

        publicaciones = obtener_timeline(cliente_bsky, db_mongo, actor=actor, limit=limit)

        if publicaciones:
            print("Enviado a Gemini para analizar...")
            analisis = cliente_gemini(publicaciones, actor)
            print(f"Respuesta de gemini {analisis}")

            guardar_analisis(db_mongo, actor, publicaciones, analisis)
            
        else:
            print("No hay publicaciones... ")

        print(f"\n--- Últimas {len(publicaciones)} publicaciones de @{actor} ---")
        for i, post in enumerate(publicaciones, 1):
            print(f"\n[{i}] {post}")

    except Exception as e:
        print(f"Error al conectar con Bluesky: {e}")


if __name__ == "__main__":
    main()
