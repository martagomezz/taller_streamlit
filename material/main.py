# importar librerías
import streamlit as st
import functions as ft

# configurar la página
ft.config_page()

# cargas los datos
path = 'red_recarga_acceso_publico_2021.csv'
df = ft.cargar_datos(path)

st.title('CARGATRON')

# menú
menu = st.sidebar.selectbox('Selecciona la página',['Home','Datos','Filtros'])

if menu == 'Home':
    ft.home(df)
elif menu == 'Datos':
    ft.datos(df)
else: 
    ft.filtros(df)