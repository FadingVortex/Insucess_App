import streamlit as st
from time import sleep
import services.connect as C

with open('./frontend/LoginPageStyle.css') as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

st.title("Transportadoras Magalu 2650")

with st.form(key="form-login",clear_on_submit=True):
    User = st.selectbox('Usuário', C.transportadoras())

    Pass = st.text_input("Senha")

    login_button = st.form_submit_button("Login")
    st.markdown("""<div class="cores-container">
    <span class="cores-span amarelo"></span>
    <span class="cores-span laranja"></span>
    <span class="cores-span vermelho"></span>
    <span class="cores-span rosa"></span>
    <span class="cores-span roxo"></span>
    <span class="cores-span azul"></span>
    <span class="cores-span azul-escuro"></span>
    <span class="cores-span azul-claro"></span>
    <span class="cores-span verde"></span>
    <span class="cores-span verde-claro"></span>
</div>""", unsafe_allow_html=True)

    if login_button:
        if Pass == '123':
            st.session_state['Usuário'] = User
            st.session_state['Login'] = 'Logado'
            st.success('Login realizado com sucesso!')
            sleep(2)
            st.switch_page('./pages/HomePage.py')
            
        else:
            st.error("Favor verificar os dados.")
    