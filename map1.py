import folium
import pandas as pd

map = folium.Map(tiles="Stamen Terrain")

def deciding_color(elevation):
    if elevation < 1_000:
        return "green"
    elif elevation >= 1000 and elevation < 2500:
        return "blue"
    else:
        return "orange"


df_volcanoes = pd.read_csv("volcanoes.csv")
lat_volcanoes = list(df_volcanoes["LAT"])
lon_volcanoes = list(df_volcanoes["LON"])
elevation_volcanoes = list(df_volcanoes['ELEV'])
name_volacnoes = list(df_volcanoes["NAME"])

html = """
<h4>Volcano info:</h4>
Name: %s <br>
Elevation = %s m
"""

fgv = folium.FeatureGroup(name="Volcanoes")

for lat, lon, elev, name in zip(lat_volcanoes,lon_volcanoes, elevation_volcanoes, name_volacnoes):
    iframe = folium.IFrame(html=html % (str(name), str(elev)), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lat, lon], popup=folium.Popup(iframe), fill_color=deciding_color(elev),
    radius=6, color="white", fill_opacity=0.8))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
style_function=lambda x:{"fillColor":"yellow" if x["properties"]["POP2005"] < 10_000_000 else "orange" if 10_000_000 <=
x["properties"]["POP2005"] < 20_000_000 else "red"}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")

