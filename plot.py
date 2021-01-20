#!/usr/bin/env python3

import folium
import pandas as pd
from unicodedata import normalize
from folium import plugins
import re

def tooltip(row, title, items):
    return '<div style="min-width:160px"><p style="margin:5px 0px; font-size: 1.2em">{}</p>'.format(title) + ''.join(['<p style="margin:5px 0px"><strong>{}</strong>: {}</p>'.format(i[0], row[i[1]]) for i in items if row[i[1]]  != '']) + '</div>'

def normalize_value(value):
    if value != value or len(value.split()) == 0:
        return ''
    else:
        return re.sub('\(|\)|\'|\"|\`', '', normalize(u'NFKD', str(value)).encode('ascii', 'ignore').decode('utf8')).title()

def draw_points(serviciodf, title, tooltip_items, color, radius):
    serviciodf[[i[1] for i in tooltip_items]] = serviciodf[[i[1] for i in tooltip_items]].apply(lambda x: [normalize_value(y) for y in x])
    for row in serviciodf.to_dict(orient='records'):
        folium.CircleMarker(location=[row['latitud'], row['longitud']],
                            stroke = True,
                            fill_opacity = .5,
                            radius=radius,
                            weight=1,
                            color='#a3a3a3',
                            popup = tooltip(row, title, tooltip_items),
                            fill_color=color).add_to(folium_map)

folium_map = folium.Map(location = [-16.4340009,-65.2686204],
                        zoom_start = 6,
                        tiles = "https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png",
                        attr = '<a href="https://www.openstreetmap.org/copyright">OSM</a>')

df = pd.read_csv('data/establecimientos.csv')
draw_points(df[df.atencion_covid.apply(lambda x: normalize_value(x)) == 'Si'], 'Establecimiento Con Atención Covid-19', [['Nombre', 'nombre_establecimiento'], ['Tipo', 'tipo'], ['Nivel', 'nivel'], ['Subsector', 'subsector'], ['Dependencia', 'dependencia'], ['Número', 'numero_contacto']], '#f57d6e', 7)
draw_points(df[df.atencion_covid.apply(lambda x: normalize_value(x)) != 'Si'], 'Establecimiento Sin Atención Covid-19', [['Nombre', 'nombre_establecimiento'], ['Tipo', 'tipo'], ['Nivel', 'nivel'], ['Subsector', 'subsector'], ['Dependencia', 'dependencia'], ['Número', 'numero_contacto']], '#9f9493', 7)
draw_points(pd.read_csv('data/farmacias.csv'), 'Farmacia', [['Nombre', 'nombre_farmacia'], ['Número', 'numero_contacto']], '#6aa2f2', 6)
draw_points(pd.read_csv('data/laboratorios.csv'), 'Laboratorio', [['Nombre', 'nombre_laboratorio'], ['Subsector', 'subsector'], ['Número', 'numero_contacto'], ['Método de Prueba', 'metodo']], '#ad94df', 7)
draw_points(pd.read_csv('data/medicina_tradicional.csv'), 'Medicina Tradicional', [['Nombre', 'nombre_proveedor'], ['Número', 'numero_contacto']], '#87c8be', 6)

plugins.LocateControl(drawCircle=False, 
                      drawMarker=False,
                      setView='once',
                      initialZoomLevel = 17,
                      strings = {
                          'title': 'Ir a mi ubicación',
                          'popup': "Estás a {distance} metros de este punto"
                      },).add_to(folium_map)

plugins.FloatImage('leyenda.png', bottom=2, left=2).add_to(folium_map)

folium_map.save('docs/index.html')