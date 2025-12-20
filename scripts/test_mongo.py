from pymongo import MongoClient
 
client = MongoClient("mongodb://localhost:27017")

try: 
    client.admin.command("ping") 
    print("✅ Conexión a MongoDB exitosa") 
    except Exception as e: print("❌ Error de conexión a MongoDB") 
    print(e)
