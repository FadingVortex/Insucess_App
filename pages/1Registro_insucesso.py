import streamlit as st
import services.connect as C
from streamlit_js_eval import streamlit_js_eval
from time import sleep

try:
    st.session_state['Login']
except:
    st.switch_page('./Login.py')

st.sidebar.page_link('./pages/2Consulta_Pedidos.py',label='Consultar Pedidos')
logout_button = st.sidebar.button('Logout')
if logout_button:
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

st.title('Cadastro de insucesso.')


with st.form('Inserir Insucesso'):
    pedido = st.number_input("Pedido", step=1)
    transportadora = st.selectbox('Transportadora', st.session_state['Usuário'])
    motivo = st.selectbox('Motivo', C.motivos())
    obs = st.text_input("Observação")

    submit_button = st.form_submit_button("Registrar")

    if submit_button and pedido > 0 and transportadora != '' and motivo != '' and obs != '':
        mensagem = C.inserir_pedido(pedido, transportadora, motivo, obs)
        st.write(mensagem)
        sleep(2)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    elif submit_button:
        st.write("Favor verifique os dados inseridos.")
        st.rerun()
