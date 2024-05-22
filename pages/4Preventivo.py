import streamlit as st
from services.connect import preventivo


try:
    logado = st.session_state['Login']
except:
    st.switch_page('./Login.py')


st.title('Pedidos Pendentes')

df = preventivo(st.session_state['Usuário'])

pedidos = df.groupby('STATUS PRAZO').agg({'PEDIDO':'nunique'})


st.dataframe(pedidos)

st.dataframe(df)
