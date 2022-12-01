import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64
#st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

df = pd.read_csv('programasinternacionaleslimpio.csv')

#st.write(df)
st.set_page_config(page_title='Programas Internacionales', page_icon=":earth_americas:", layout="wide")

file_ = open("Flag-globe-2.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

t1, t2 = st.columns(2)
with t1:
    st.header('Gerardo Barajas Sánchez - A00828760')
    st.title('Analisis de datos de programas internacionales')
    st.write('En esta pagina tratare de comprobar 3 hipotesis diferentes a traves la visualizacion de datos')

with t2:
    st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True)


st.title('Hipotesis a probar')

st.header('Que porcentage de alumnos de fueron asignados en su primera opcion por su país seleccionado, promedio y region.')


Pais_de_origen = df['PaisSeleccionado'].unique().tolist()
pais = st.selectbox('Seleccione el pais en el cual se realizo la solicitud', Pais_de_origen, 0)
df = df[df['PaisSeleccionado']==pais]

promedio_alumnos = df['Rango de Promedios'].unique().tolist()
promedio = st.selectbox('¿Cual es es el promedio que buscas?', promedio_alumnos, 0)
df = df[df['Rango de Promedios']==promedio]

Region_alumnos = df['Región'].unique().tolist()
region = st.selectbox('¿Cual region quieres observar?', Region_alumnos, 0)
df = df[df['Región']==region]

fig = px.parallel_categories(df, dimensions=['PaisSeleccionado','Rango de Promedios','Región','Intercambio Internacional','PrimeraOpcion','PaisAsignado'],
                color="Promedio", 
                color_continuous_scale=["orange", "red",
                                        "green", "blue",
                                        "purple"],
                #labels={'Region':'Regions in USA','Category':'Categories','Quantity':'Quantity per month'}
                )

fig.update_layout(width=800)

st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.header('Porcentage de alumnos que realizaron un Intercambio Internacional o un Study Abroad por periodo')
        df = pd.read_csv('programasinternacionaleslimpio.csv')
        Periodo = df['PeriodoAcadémico'].unique().tolist()
        per = st.selectbox('Seleccione el Periodo Academico', Periodo, 0)
        df = df[df['PeriodoAcadémico']==per]

        df_p = df.groupby(['Intercambio Internacional']).size().reset_index()
        df_p['percentage'] = df.groupby(['Intercambio Internacional']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        df_p.columns = ['Intercambio Internacional', 'Counts', 'Percentage']
        df_p['Percentage'] = ((df_p['Counts'] / df_p['Counts'].sum()) * 100)
        fig2 = px.pie(df_p, values='Counts', names='Intercambio Internacional')

        st.plotly_chart(fig2, use_container_width=True)
    with col2:

        #df = pd.read_csv('programasinternacionaleslimpio.csv')
        st.header('Porcentage de alumnos que fueron asignados en su primera opcion.')
        #Inter = df['Intercambio Internacional'].unique().tolist()
        #inter = st.selectbox('Seleccione su metodo de intercambio', Inter, 0)
        #df = df[df['Intercambio Internacional']==inter]

        #df_p = df.groupby(['PrimeraOpcion']).size().reset_index()
        #df_p['percentage'] = df.groupby(['PrimeraOpcion']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        #df_p.columns = ['Oportunidad', 'Counts', 'Percentage']
        #df_p['Percentage'] = (df_p['Counts'] / df_p['Counts'].sum()) * 100
        #fig3 = px.pie(df_p, values='Counts', names='Oportunidad')

        #st.plotly_chart(fig3, use_container_width=True)
        df = pd.read_csv('programasinternacionaleslimpio.csv')
        df_p = df.groupby(['Intercambio Internacional','PrimeraOpcion']).size().reset_index()
        df_p.columns = ['Intercambio Internacional','PrimeraOpcion' ,'Counts']
        df_p['percentage'] = df_p.groupby(['Counts']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
        df_p.columns = ['Oportunidad','PrimeraOpcion' ,'Counts', 'Percentage']
        df_p['Percentage'] = (df_p['Counts'] / df_p['Counts'].sum()) * 100
        fig4 = px.sunburst(df_p, path=['Oportunidad', 'PrimeraOpcion'], values='Percentage')
        st.plotly_chart(fig4, use_container_width=True) 

