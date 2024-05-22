import streamlit as st
from services.connect import preventivo
import pandas as pd


try:
    logado = st.session_state['Login']
except:
    st.switch_page('./Login.py')


c1, c2 = st.columns(2)

c1.page_link('./pages/HomePage.py', label='Home')
c2.page_link('./pages/3Registro_devolucao.py',label='Registrar Devolução')

st.title('Pedidos Pendentes')

df = preventivo(st.session_state['Usuário'])



df['DATA_ENTREGA_PREVISTA'] = pd.to_datetime(df['DATA_ENTREGA_PREVISTA'], format='%d/%m/%Y').sort_values('DATA_ENTREGA_PREVISTA')
pedidos =  pd.pivot_table(df, 'PEDIDO' ,'STATUS PRAZO', 'DATA_ENTREGA_PREVISTA', 'nunique')

st.dataframe(pedidos)

st.dataframe(df)
