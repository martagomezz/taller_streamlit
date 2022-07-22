# importar librerías
from doctest import DocFileSuite
from tabnanny import check
import streamlit.components.v1 as components
import streamlit as st # !pip install Streamlit
from PIL import Image # !pip install Pillow
import pandas as pd

# configurar la página
def config_page():
    st.set_page_config(
        page_title = 'Cargatron',
        page_icon = ':electric_plug:',
        layout = 'wide'
    )

# caché
st.cache(suppress_st_warning=True)

# cargar los datos
def cargar_datos(path):
    df = pd.read_csv(path, sep=';')
    df.rename(columns={'latidtud':'lat', 'longitud':'lon'}, inplace=True)
    return df

# HOME
def home(df):
    img = Image.open('puntos-recarga-madrid.jpg')
    st.image(img,use_column_width='auto')
    with st.expander('¿Quieres saber más?'):
        st.write('Es una solucion factible para el cambio climático')
    pass

# DATOS
def datos(df):
    # Dos formas de mostra una tabla
    st.write(df)
    #st.table(df)

    # Mostrar un mapa
    st.map(df) #solo funciona si tienes internet

    # Mostrar archivo html
    filehtml = open('heatmap.html','r')
    sc = filehtml.read()
    components.html(sc, height=700 )

    # Mostrar una tabla filtrada
    nc_distrito = df.groupby('DISTRITO')['Nº CARGADORES'].sum()
    st.write(nc_distrito)

    # Mostrar una gráfica (histograma) con la tabla anterior
    st.bar_chart(nc_distrito)

    # Mostrar otra tabla filtrada, esta vez por operadores
    nc_operador = df.groupby('OPERADOR')['Nº CARGADORES'].sum()
    st.write(nc_operador)

    # Mostrar una gráfica (líneas) con la tabla anterior
    st.line_chart(nc_operador)


# FILTROS
def filtros(df):
    #Crearnos un desplegable
    #st.write(df)
    list_dis = list(df['DISTRITO'].unique())
    filtro_dis = st.sidebar.selectbox('Selecciona un distrito',list_dis)
    df = df[df['DISTRITO'] == filtro_dis]
    st.write(df)

    # Crear un check box (varias opciones)
    st.sidebar.write('Selecciona por operador o por nº de cargadores')
    check_op = st.sidebar.checkbox('Filtrar por operador')
    check_nc = st.sidebar.checkbox('Filtrar por nº de cargadores')

    if check_nc & check_op:
        st.error('Solo puedes filtrar por una de las 2 opciones')
    elif check_op:
        list_op = list(df['OPERADOR'].unique())
        filtro_op = st.sidebar.selectbox('Selecciona un operador',list_op)
        df = df[df['OPERADOR'] == filtro_op]
        #st.write(df)

    elif check_nc: 
        c_min = df['Nº CARGADORES'].min()
        c_max = df['Nº CARGADORES'].max()

        if c_min != c_max:
            intervalo = range(c_min,c_max+1)
            filtro_nc = st.sidebar.select_slider('Selecciona el intervalo',intervalo, value=(c_min,c_max))
            mask1 = df['Nº CARGADORES'] >= filtro_nc[0]
            mask2 = df['Nº CARGADORES'] <= filtro_nc[1]
            df = df[mask1&mask2]
            #st.write(df)

        else:
            pass

    # Crear columnas
    col1, col2 = st.columns(2)

    with col1:
        st.map(df)

    with col2:
        st.table(df[['DIRECCION','EMPLAZAMIENTO','Nº CARGADORES']])

