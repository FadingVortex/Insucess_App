import streamlit as st
import pandas as pd
import services.connect as consultar_pedidos_len
from time import sleep

st.set_page_config(
    page_title="Status dos Pedidos",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Pode ser "wide" ou "centered"
    initial_sidebar_state="collapsed",  # Pode ser "auto", "expanded", ou "collapsed"
)
st.sidebar.page_link('./pages/HomeFilial.py', label='Home')
st.sidebar.page_link('./pages/Solicitação.py')

try:
    log = st.session_state['Login']
except:
    st.switch_page('./Login.py')


st.title('Status Pedidos')

with st.form("FormStatus"):

    Ped = st.number_input('Pedido', step=1, label_visibility='hidden')
    button = st.form_submit_button('Consultar')

    if button:
        st.table(consultar_pedidos_len(st.session_state['Usuário']).assign(hack='').set_index('hack'))
    else:
        st.table(consultar_pedidos_len(st.session_state['Usuário']).assign(hack='').set_index('hack'))
