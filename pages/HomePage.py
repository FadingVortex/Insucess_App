import streamlit as st 

try:
    user = st.session_state['Usuário']
except:
    st.switch_page('./Login.py')

with open("./frontend/HomePageStyle.css") as f:
    teste = st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('O que você deseja?')

c1, c2, c3 = st.columns(3)
c1.page_link('./pages/1Registro_insucesso.py', label='Registro de Insucesso')
c2.page_link('./pages/3Registro_devolucao.py', label='Registro de Devolução')
c3.page_link('./pages/4Preventivo.py', label='Preventivo')

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