import pymongo
import json
import os

def conectar_mongo():

    client = pymongo.MongoClient("mongodb://root:root@localhost:27017")
    db = client["bluesky_db"]
    return db

def extraer_json_mongo(db, coleccion, ruta_salida):

    coleccion_mongo = db[coleccion]

    documentos = list(coleccion_mongo.find())

    documentos_json = json.dumps(documentos, default=str, indent=4)

    with open(ruta_salida, 'w', encoding='utf-8') as archivo:
        archivo.write(documentos_json)

    print(f"Se ha extraído la colección '{coleccion}' a '{ruta_salida}'")

def main():
    db = conectar_mongo()

    coleccion = "publicaciones"
    ruta_salida = "1_3_Perez_Mas_Endika.json"

    extraer_json_mongo(db, coleccion, ruta_salida) 

if __name__ == "__main__":
    main()