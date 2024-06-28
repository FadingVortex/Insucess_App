import streamlit as st
import pandas as pd
import services.connect as C
from time import sleep

st.set_page_config(
    page_title="Status dos Pedidos",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Pode ser "wide" ou "centered"
    initial_sidebar_state="collapsed",  # Pode ser "auto", "expanded", ou "collapsed"
)

c1, c2 = st.columns(2)

c1.page_link('./pages/HomePage.py', label='Home')
c2.page_link('./pages/5Pedidos_Saida_Loja.py',label='Consultar Pedidos')

st.title('Importar Lote')

table = st.empty()

with st.form("FormStatus"):

    Ped = st.selectbox('Lotes',C.consulta_lotes())
    button = st.form_submit_button('Consultar')

if button:
    table.table(C.consultar_pedidos_importar(Ped).assign(hack='').set_index('hack'))

import_button = st.button("Importar Lote")

if import_button and table.empty:
    st.write(C.import_lote(st.session_state['Usuário'], Ped))
