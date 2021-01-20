#!/usr/bin/env python3

import pandas as pd
import requests

servicios = [{'url': 'ws-medicinaTradicional.php', 'filename': 'medicina_tradicional.csv', 'type': 'single'},
             {'url': 'ws-laboratorios.php', 'filename': 'laboratorios.csv', 'type': 'single'},
             {'url': 'ws-medicamentos.php', 'filename': 'medicamentos.csv', 'type': 'single'},
             {'url': 'ws-establecimientosSnis.php', 'filename': 'establecimientos.csv', 'type': 'departamental'},
             {'url': 'ws-farmacias.php', 'filename': 'farmacias.csv', 'type':'departamental'}]

def get_data(servicio):
    if servicio['type'] == 'single':
        get_single(servicio)
    if servicio['type'] == 'departamental':
        get_departamental(servicio)

def get_single(servicio):
    pd.DataFrame(requests.get('https://servicios.boliviasegura.gob.bo/api/{}'.format(servicio['url'])).json()['data']).to_csv('data/{}'.format(servicio['filename']), index=False)

def get_departamental(servicio):
    df = pd.DataFrame()
    for i in range(1,10):
        df = pd.concat([df, pd.DataFrame(requests.get('https://servicios.boliviasegura.gob.bo/api/{}?id_departamento={}'.format(servicio['url'], i)).json()['data'])])
    df.to_csv('data/{}'.format(servicio['filename']), index=False)

for servicio in servicios:
    get_data(servicio)