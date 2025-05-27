import streamlit as st
import folium
from streamlit_folium import folium_static
import openrouteservice

# Obtener API key desde secrets
ors_key = st.secrets["api"]["ors_key"]
client = openrouteservice.Client(key=ors_key)

# Coordenadas: origen y destino
origen = (-74.0721, 4.7301)  # Casa
destino = (-74.10058, 4.65615)  # Universidad Libre - Sede El Bosque

# Puntos intermedios para construir distintas rutas
alternativas = [
    [origen, destino],
    [origen, (-74.085, 4.70), destino],
    [origen, (-74.09, 4.69), (-74.095, 4.675), destino],
    [origen, (-74.08, 4.705), (-74.09, 4.68), destino],
    [origen, (-74.075, 4.72), (-74.08, 4.70), (-74.095, 4.67), destino],
]

rutas = []
duraciones = []

for puntos in alternativas:
    try:
        ruta = client.directions(coordinates=puntos, profile='driving-car', format='geojson')
        duracion = ruta['features'][0]['properties']['summary']['duration'] / 60
        rutas.append(ruta)
        duraciones.append(duracion)
    except Exception as e:
        st.error(f"Error obteniendo la ruta: {e}")
        rutas.append(None)
        duraciones.append(float('inf'))

# Interfaz
st.title("Rutas a la Universidad Libre - Sede El Bosque")
opcion = st.selectbox("Selecciona una opción de ruta", [f"Opción {i+1} - {int(duraciones[i])} min" for i in range(5)])
idx = int(opcion.split()[1]) - 1
ruta_sel = rutas[idx]

# Mostrar ruta en el mapa
coords = ruta_sel['features'][0]['geometry']['coordinates']
midpoint = coords[len(coords) // 2]
m = folium.Map(location=[midpoint[1], midpoint[0]], zoom_start=14, tiles="CartoDB positron")

# Marcadores
folium.Marker(location=[origen[1], origen[0]], tooltip="Casa", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(location=[destino[1], destino[0]], tooltip="Universidad Libre", icon=folium.Icon(color="red")).add_to(m)

# Rutas en el mapa
for i, ruta in enumerate(rutas):
    if ruta:
        color = "blue" if i == idx else "gray"
        coords_ruta = ruta['features'][0]['geometry']['coordinates']
        coords_latlon = [(lat, lon) for lon, lat in coords_ruta]
        folium.PolyLine(locations=coords_latlon, color=color, weight=6 if i == idx else 2, opacity=0.8).add_to(m)

# Mostrar duración y distancia
info = ruta_sel['features'][0]['properties']['segments'][0]
distancia = info['distance'] / 1000  # km
duracion = info['duration'] / 60  # min
st.markdown(f"**Duración estimada:** {duracion:.1f} minutos")
st.markdown(f"**Distancia estimada:** {distancia:.2f} km")

# Mostrar instrucciones
st.subheader("Resumen del trayecto:")
for step in info['steps']:
    st.markdown(f"- {step['instruction']} ({int(step['distance'])} m)")

folium_static(m)