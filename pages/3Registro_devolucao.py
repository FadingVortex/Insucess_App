import streamlit as st
from services.connect import registro_dev
from time import sleep



with open('./frontend/DevPageStyle.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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

try:
    user = st.session_state['Usuário']
except:
    st.switch_page('./Login.py')

c1, c2 = st.columns(2)

c1.page_link('./pages/HomePage.py', label='Home')
c2.page_link('./pages/1Registro_insucesso.py',label='Registrar Insucesso')


with st.form(key='Form-Dev', clear_on_submit=True):
    pedido = st.number_input("Pedido", step=1)
    destino = st.selectbox('Destino', [' ','Dqs', 'Filial', 'Cd'])
    arquivo = st.file_uploader('Arquivo')

    button = st.form_submit_button("Registrar", type='primary')
    
    if button and pedido > 0 and arquivo and destino != ' ':
        with st.spinner("Carregando..."):
            verify, mensagem = registro_dev(pedido,user,arquivo,destino)
            if verify == 'Sucesso':
                st.success(mensagem)
            else:
                st.error(mensagem)
    elif button:
        st.error('Verifique os dados....')
        sleep(2)
        st.rerun()