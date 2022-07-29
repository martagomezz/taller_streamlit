# importar librerias
import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
import texto as tx

# configuración de la página
def config_page():
    st.set_page_config(
        page_title = 'Calidad del aire en Madrid',
        page_icon = ':leaves:',
        layout = 'wide'
    )

# cache
st.cache(suppress_st_warning=True)

# cargar los datos
def cargar_datos(path):
    df = pd.read_csv(path, index_col=0)
    return df

# HOME
def home(df):
    img = Image.open('madrid.jpg')
    st.image(img, use_column_width='auto')
    with st.expander('¿Quieres saber más?'):
        st.write(tx.texto_info)
    pass
    with st.expander('¿Quieres saber más sobre los íxodos de nitrógeno?'):
        st.write(tx.texto_nox)
    pass
    with st.expander('¿Quieres saber más sobre el material particulado?'):
        st.write(tx.texto_PM25)
    pass
    with st.expander('¿Quieres saber más sobre el Ozono?'):
        st.write(tx.texto_ozono)
    pass

# DATOS
def datos(df):
    # mostramos la tabla con el dataset
    st.write(df) 
    
    # mostramos el mapa con las estaciones
    st.map(df) # solo funciona si tienes internet
    
    # mostramos dos listados/columnas: 1. estaciones de control y 2. contaminantes.

    col1, col2 = st.columns(2)

    with col1:
        st.write(pd.DataFrame(sorted(df['name'].unique()), columns = ['Estaciones de Control']))

    with col2:
        st.write(pd.DataFrame(sorted(df['magnitud'].unique()), columns = ['Contaminantes']))
    
    # mostrar el archivo html
    filehtml = open('heatmap.html','r')
    sc = filehtml.read()
    components.html(sc, height = 700)

# FILTROS
def filtros(df):

    # Crear un desplegable para el contaminante
    lista_contaminante = list(df['magnitud'].unique())
    filtro_contaminante = st.sidebar.selectbox('Selecciona un contaminante',lista_contaminante)
    df = df[df['magnitud'] == filtro_contaminante]

    # Crear un desplegable para la estación de control
    lista_estacion = list(df['name'].unique())
    filtro_estacion = st.sidebar.selectbox('Selecciona una estación',lista_estacion)
    df = df[df['name'] == filtro_estacion]

    # Crear un desplegable para el año
    lista_anno = list(df['anno'].unique())
    filtro_anno = st.sidebar.selectbox('Selecciona un año',lista_anno)
    df = df[df['anno'] == filtro_anno]

    # Crear un check box para intervalo de meses
    st.sidebar.write('Quieres seleccionar un intervalor de meses?')    
    check_meses = st.sidebar.checkbox('Filtrar por intervalo')

    if check_meses:
        mes_min = df['mes'].min()
        mes_max = df['mes'].max()

        if mes_min != mes_max:
            intervalo = range(mes_min,mes_max+1)
            filtro_meses = st.sidebar.select_slider('Acota los meses',intervalo,value=(mes_min,mes_max))
            mask1 = df['mes'] >= filtro_meses[0]
            mask2 = df['mes'] <= filtro_meses[1]
            df2 = df[mask1&mask2] # Nombramos un nuevo dataframe

      # Mostramos la tabla con el dataset
        st.write(df2) 

    else: 
         st.write(df) 

    # Mostramos un  mapa donde aparezca la estación de control selecciona
    st.map(df)

    # Mostramos dos listados/columnas: 
    col1, col2 = st.columns(2)

    # 1. valores medios contaminante seleccionado
    with col1:
        st.write('Niveles medios del contaminante seleccionado por mes')
        st.write(df[['mes','nivel']].groupby('mes').mean())

    # 2. gráfica valores medios por mes
    with col2:
        st.write('Gráfica valores medios del contaminante seleccionado por mes')
        st.area_chart(df[['mes','nivel']].groupby('mes').mean(), height = 450)

    # Muestra un gráfico de barras con valores medios de los meses seleccionados en el slider.
    if check_meses ==  True:
        st.bar_chart(df2[['mes','nivel']].groupby('mes').mean())
