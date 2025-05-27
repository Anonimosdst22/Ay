import os
import toml
import openrouteservice

def verificar_secrets():
    ruta_secrets = os.path.join(".streamlit", "secrets.toml")

    if not os.path.exists(ruta_secrets):
        print("❌ No se encontró el archivo '.streamlit/secrets.toml'")
        return

    try:
        config = toml.load(ruta_secrets)
        api_key = config["api"]["ors_key"]
        print("✅ API key encontrada en 'secrets.toml'")
    except Exception as e:
        print(f"❌ Error leyendo el archivo secrets.toml: {e}")
        return

    try:
        client = openrouteservice.Client(key=api_key)
        coords = ((-74.0721, 4.7301), (-74.10058, 4.65615))
        route = client.directions(coords)
        print("✅ Conexión a OpenRouteService exitosa.")
    except Exception as e:
        print(f"❌ Error al conectar con OpenRouteService: {e}")

if __name__ == "__main__":
    verificar_secrets()
