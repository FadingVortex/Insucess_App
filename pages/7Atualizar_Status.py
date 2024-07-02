import streamlit as st
import pandas as pd
import services.connect as C

st.set_page_config(
    page_title="Status dos Pedidos",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Pode ser "wide" ou "centered"
    initial_sidebar_state="collapsed",  # Pode ser "auto", "expanded", ou "collapsed"
)

if 'df' not in st.session_state or st.session_state['df'] == None:
    st.session_state['df'] = pd.DataFrame()

c1, c2 = st.columns(2)

c1.page_link('./pages/HomePage.py', label='Home')
c2.page_link('./pages/5Pedidos_Saida_Loja.py',label='Consultar Pedidos')


st.title('Atualizar Status Pedido')

table = st.empty()

with st.form("FormStatus"):

    Ped = st.number_input('Pedido', 900000000, step=1)
    status = st.selectbox('Status', ['Entregue', 'Endereço não Localizado', 'Cliente Ausente', 'Avaria'])
    button = st.form_submit_button('Consultar')

if button:
    DF = C.consultar_pedidos_status(Ped)
    st.session_state['df'] = DF
    df2 = DF.assign(hack='').set_index('hack')
    table.table(df2)

import_button = st.button("Registrar Status")

if import_button and table.empty:
    st.write(C.atualizar_status(st.session_state['df'], status, 'teste'))
    st.session_state['df'] = None
