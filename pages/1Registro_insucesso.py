import streamlit as st
import services.connect as C
from streamlit_js_eval import streamlit_js_eval
from time import sleep



try:
    logado = st.session_state['Login']
except:
    st.switch_page('./Login.py')

with open('./frontend/RegisterPageStyle.css') as f:
    st.markdown(f"<style>{f.read()}</style", unsafe_allow_html=True)

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

c1, c2 = st.columns(2)

c1.page_link('./pages/HomePage.py', label='Home')
c2.page_link('./pages/3Registro_devolucao.py',label='Registrar Devolução')



st.title('Cadastro De Insucesso')


with st.form('Inserir Insucesso'):
    pedido = st.number_input("Pedido", step=1)
    
    transportadora = st.text_input('Transportadora', value=st.session_state['Usuário'])
    motivo = st.selectbox('Motivo', C.motivos())
    obs = st.text_input("Observação")
    filial = st.text_input("Filial")

    submit_button = st.form_submit_button("Registrar",type='primary')

    if submit_button and pedido > 0 and transportadora != '' and motivo != '' and obs != '' and filial != '':
        mensagem = C.inserir_pedido(pedido, transportadora, motivo, obs, filial)
        st.write(mensagem)
        sleep(2)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    elif submit_button:
        st.write("Favor verifique os dados inseridos.")
    
