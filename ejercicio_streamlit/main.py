# importar librerías
import streamlit as st
import functions as ft

# configurar la página
ft.config_page()

# cargar los datos

path = 'air_quality_madrid.csv' # Ruta relativa de tu base de datos
df = ft.cargar_datos(path)

st.title('Calidad del aire en Madrid') # Añadir un título a tu página

# menú
menu = st.sidebar.selectbox('Selecciona menú', ['Home','Datos','Filtros'])

if menu == 'Home':
    ft.home(df)
elif menu == 'Datos':
    ft.datos(df)
else:
    ft.filtros(df)