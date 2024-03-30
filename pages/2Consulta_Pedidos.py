import streamlit as st
import services.connect as C
from streamlit_js_eval import streamlit_js_eval

try: 
    st.session_state['Login']
except:
    st.switch_page('./Login.py')

st.sidebar.page_link('./pages/1Registro_insucesso.py',label='Registrar Insucesso')
logout_button = st.sidebar.button('Logout')

if logout_button:
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

user = st.session_state['Usuário']
st.title("Consulta de Pedidos")


st.dataframe(C.verificar_pedidos(user), hide_index=False)