import streamlit as st
import pandas as pd
import numpy as np
import geocoder
import googlemaps
from tabula.io import read_pdf
import statistics
import xgboost as xgb
import shap as shap_lib
import streamlit.components.v1 as components
import plotly.graph_objects as go

hurtos_url = 'df_hurtos.csv'

def plot_top_n_values(names, values, n):
    # Obtener los n valores más importantes
    top_n_values = sorted(zip(names, values), key=lambda x: x[1], reverse=True)[:n]
    top_names, top_values = zip(*top_n_values)

    # Crear la figura de barras
    fig = go.Figure(data=go.Bar(x=top_names, y=top_values))

    # Personalizar el diseño del gráfico
    fig.update_layout(
        xaxis_title='Variables',
        yaxis_title='Importancia',
        title=f'Top {n} valores más importantes'
    )

    # Mostrar el gráfico
    return fig

@st.cache_data(persist=True)
def open_hurtos():
    data = pd.read_csv(hurtos, encoding='utf-8')
    return data

def st_shap(plot, height=None):
    shap_html = f"<head>{shap_lib.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)



API_KEY = 'AIzaSyBZaIOIr5U4xfKUuYmNsf58dOeKH4SPX04'

def buscar_lugares_turismo(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Realiza la búsqueda de lugares cercanos
    places_result = gmaps.places_nearby(location=(lat, lng), radius=radio, type='tourist_attraction')
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Recorre los lugares encontrados y agrega la información a la lista
    for place in places_result['results']:
        nombre = place['name']
        lugares.append(nombre)
        calificacion = place.get('rating', 'N/A')
        rating.append(calificacion)
    
    
    elem = len(lugares)
    if elem == 0:
        return 0
    
    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0

    res = elem * (rat_med / 5)
    
    return res

def buscar_lugares_jardines(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Realiza la búsqueda de lugares cercanos
    places_result = gmaps.places_nearby(location=(lat, lng), radius=radio, type='park')
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Recorre los lugares encontrados y agrega la información a la lista
    for place in places_result['results']:
        nombre = place['name']
        lugares.append(nombre)
        calificacion = place.get('rating', 'N/A')
        rating.append(calificacion)
    
    elem = len(lugares)
    if elem == 0:
        return 0

    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0

    res = elem * (rat_med / 5)
    
    return res

def buscar_lugares_sanidad(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Realiza la búsqueda de lugares cercanos
    places_hospitales = gmaps.places_nearby(location=(lat, lng), radius=radio, type='hospital')
    places_farmacias = gmaps.places_nearby(location=(lat, lng), radius=radio, type='pharmacy')
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Recorre los lugares de hospitales encontrados y agrega la información a la lista
    for place in places_hospitales['results']:
        nombre = place['name']
        lugares.append(nombre)
        calificacion = place.get('rating', 'N/A')
        rating.append(calificacion)
    
    # Recorre los lugares de farmacias encontrados y agrega la información a la lista
    for place in places_farmacias['results']:
        nombre = place['name']
        lugares.append(nombre)
        calificacion = place.get('rating', 'N/A')
        rating.append(calificacion)
    
    num_lugares = len(lugares)
    if num_lugares == 0:
        return 0

    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0
    
    salida = num_lugares * (rat_med / 5)
    
    return salida

def buscar_lugares_transporte(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Realiza la búsqueda de lugares cercanos
    places_result = gmaps.places_nearby(location=(lat, lng), radius=radio, type='transit_station')
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Recorre los lugares encontrados y agrega la información a la lista
    for place in places_result['results']:
        nombre = place['name']
        lugares.append(nombre)
        calificacion = place.get('rating', 'N/A')
        rating.append(calificacion)
    
    elem = len(lugares)
    if elem == 0:
        return 0

    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0

    res = elem * (rat_med / 5)
    
    return res

def buscar_lugares_ocio(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    tipos_lugar = ['night_club','restaurant','bar']
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Realiza la búsqueda de lugares para cada tipo de lugar
    for tipo in tipos_lugar:
        places_result = gmaps.places_nearby(location=(lat, lng), radius=radio, type=tipo)
        
        # Recorre los lugares encontrados y agrega la información a la lista
        for place in places_result['results']:
            nombre = place['name']
            lugares.append(nombre)
            calificacion = place.get('rating', 'N/A')
            rating.append(calificacion)
    
    num_lugares = len(lugares)
    if num_lugares == 0:
        return 0
    
    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0

    puntuacion_deseada = 5
    
    salida = num_lugares * (rat_med / puntuacion_deseada)
    
    return salida

def buscar_lugares_educacion(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    tipos_lugar = ['school','secondary_school','university']
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Realiza la búsqueda de lugares para cada tipo de lugar
    for tipo in tipos_lugar:
        places_result = gmaps.places_nearby(location=(lat, lng), radius=radio, type=tipo)
        
        # Recorre los lugares encontrados y agrega la información a la lista
        for place in places_result['results']:
            nombre = place['name']
            lugares.append(nombre)
            calificacion = place.get('rating', 'N/A')
            rating.append(calificacion)
    
    num_lugares = len(lugares)
    if num_lugares == 0:
        return 0
    
    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0

    puntuacion_deseada = 5
    
    salida = num_lugares * (rat_med / puntuacion_deseada)
    
    return salida

def buscar_lugares_supermercado(lat, lng, radio=700):
    # Configura tu clave de API
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Realiza la búsqueda de lugares cercanos
    places_result = gmaps.places_nearby(location=(lat, lng), radius=radio, type='supermarket')
    
    # Lista para almacenar los resultados
    lugares = []
    rating = []
    
    # Recorre los lugares encontrados y agrega la información a la lista
    for place in places_result['results']:
        nombre = place['name']
        lugares.append(nombre)
        calificacion = place.get('rating', 'N/A')
        rating.append(calificacion)
    
    elem = len(lugares)
    if elem == 0:
        return 0

    valores_validos = [valor for valor in rating if valor != 'N/A']
    if valores_validos:
        rat_med = statistics.mean(valores_validos)
    else:
        return 0

    res = elem * (rat_med / 5)
    
    return res
    

with st.sidebar:
    st.header('Introduce los datos de la vivienda:')
    metros = st.slider('Metros cuadrados',1, 4100, 300)
    zona = st.text_input('Zona',placeholder='Escribe una calle de Valencia').lower()
    num_habs = st.slider('Nº de habitaciones',1, 10, 3)
    banyos = st.slider('Nº de baños',1, 11, 2)
    planta = st.slider('Planta',1, 15, 2)
    tipo = st.sidebar.selectbox('Tipo de vivienda',
                                ['Piso', 'Ático', 'Planta Baja', 'Apartamento', 'Casa o chalet', 'Casa Adosada', 'Finca Rústica', 'Dúplex', 'Loft', 'Estudio']).lower()
    
    antig = st.sidebar.selectbox('Antigüedad',
                                ['1 a 5 años', '5 a 10 años', '10 a 20 años', '20 a 30 años', '30 a 50 años', '50 a 70 años', '70 a 100 años', '+ 100 años'])
    
    options = st.multiselect(
        'Selecciona entre estas opciones',
        ['Ascensor', 'Amueblado', 'Parking', 'Piscina','Trastero','Terraza', 'Balcon','Calefaccion', 'Aire', 'Jardin'],
        ['Ascensor', 'Parking'])
    options = [elem.lower() for elem in options]
    

API_KEY = 'AIzaSyDnhgUgO__35_BWWnY-5sTSmjOIIjWDOYA'
zona = zona + ', valencia'
loc = geocoder.google(zona,key=API_KEY)
latit = loc.lat
longi = loc.lng
cp = loc.postal
if cp == None and latit != None:
    g = geocoder.google([latit,longi],method='reverse',key=API_KEY)
    cp = g.postal

indiv = pd.DataFrame({'m2':[metros],'habs.':[num_habs],'baños':[banyos],'planta':[planta],'tipo':[tipo], 'antigüedad': [antig], 'cod_pos': [cp]})


lista = ['ascensor', 'amueblado', 'parking', 'piscina', 'trastero', 'terraza', 'balcon', 'calefaccion', 'aire', 'jardin',]

dic = {}

for elem in lista:
    if elem in options:
        dic[elem] = [1]
    else:
        dic[elem]= [0]
        
indiv = indiv.assign(**dic)
ordinal_mapping = {'menos de 1 año': 1, '1 a 5 años': 2, '5 a 10 años': 3, '10 a 20 años': 4, '20 a 30 años':5, '30 a 50 años':6,'50 a 70 años':7,'70 a 100 años':8,'+ 100 años':9}
indiv['antigüedad'] = indiv['antigüedad'].map(ordinal_mapping)

hurtos = pd.read_csv(hurtos_url, encoding='utf-8', dtype={'cod_pos': 'category'})

indiv = pd.merge(indiv, hurtos, on='cod_pos',how='left')


indiv['turismo'] = [buscar_lugares_turismo(latit, longi, radio=700)]
indiv['jardines'] = [buscar_lugares_jardines(latit, longi, radio=700)]
indiv['sanidad'] = [buscar_lugares_sanidad(latit, longi, radio=700)]
indiv['transporte'] = [buscar_lugares_transporte(latit, longi, radio=700)]
indiv['ocio'] = [buscar_lugares_ocio(latit, longi, radio=700)]
indiv['educacion'] = [buscar_lugares_educacion(latit, longi, radio=700)]
indiv['supermercado'] = [buscar_lugares_supermercado(latit, longi, radio=700)]



lista = ['apartamento', 'casa adosada', 'casa o chalet', 'dúplex', 'estudio', 'finca rústica', 'loft', 'piso', 'planta baja', 'ático']
dic = {}
for elem in lista:
    if elem == tipo:
        dic['tipo_'+elem]=[1]
    else:
        dic['tipo_'+elem]=[0]
        
indiv = indiv.assign(**dic)

col_modelo = ['m2', 'habs.', 'baños', 'planta', 'antigüedad', 'ascensor',
       'amueblado', 'parking', 'piscina', 'trastero', 'terraza', 'balcon',
       'calefaccion', 'aire', 'jardin',
       'Mayor(+) o menor (-) probabilidad respecto la ciudad de Valencia',
       'turismo', 'jardines', 'sanidad', 'transporte', 'ocio', 'educacion',
       'supermercado', 'tipo_apartamento', 'tipo_casa adosada',
       'tipo_casa o chalet', 'tipo_dúplex', 'tipo_estudio',
       'tipo_finca rústica', 'tipo_loft', 'tipo_piso', 'tipo_planta baja',
       'tipo_ático']


indiv_modelo = indiv[col_modelo]


st.header('Con tus datos introducidos, la entrada al modelo sería:')
st.write(indiv_modelo)

loaded_model = xgb.sklearn.XGBRegressor()
loaded_model.load_model('modelo_xgb.model')

imp = loaded_model.feature_importances_


n = st.slider('Nº de variables más importantes',1, 33, 4)
graf = plot_top_n_values(col_modelo, imp, n)
st.write(graf)

if st.button('PREDECIR PRECIO DE VIVIENDA'):
    
    pred = loaded_model.predict(indiv_modelo)
    
    st.write('El precio de una vivienda con esas características es de: ',pred[0],' €')
    
    st.markdown('## ¿Por qué este piso vale lo que vale?')
    
    explainer = shap_lib.TreeExplainer(loaded_model)
    shap_values = explainer.shap_values(indiv_modelo)

    # visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
    st_shap(shap_lib.force_plot(explainer.expected_value, shap_values[0,:], indiv_modelo.iloc[0,:]))   
    
    
    
else:
    st.write('Dale al botón para predecir')


    
    
    