import streamlit as st
from services.connect import preventivo
import pandas as pd
from io import StringIO


def to_csv(df):
    output = StringIO()
    df.to_csv(output, index=False)
    processed_data = output.getvalue()
    return processed_data

try:
    logado = st.session_state['Login']
except:
    st.switch_page('./Login.py')

st.write(st.secrets['KEY'])

c1, c2 = st.columns(2)

c1.page_link('./pages/HomePage.py', label='Home')
c2.page_link('./pages/3Registro_devolucao.py',label='Registrar Devolução')

st.title('Pedidos Pendentes')

df = preventivo(st.session_state['Usuário'])



df['DATA_ENTREGA_PREVISTA'] = pd.to_datetime(df['DATA_ENTREGA_PREVISTA'], format='%d/%m/%Y')
df = df.sort_values('DATA_ENTREGA_PREVISTA')
pedidos =  pd.pivot_table(df, 'PEDIDO' ,'STATUS PRAZO', 'DATA_ENTREGA_PREVISTA', 'nunique')

button = st.button('GERAR CSV')

if button:
    with st.spinner('Gerando arquivo.'):
        csv_data = to_csv(df = df.sort_values('DATA_ENTREGA_PREVISTA'))
        st.download_button(
            label="Baixar dados como CSV",
            data=csv_data,
            file_name='dados.csv',
            mime='text/csv'
        )

st.dataframe(pedidos)

st.dataframe(df)

