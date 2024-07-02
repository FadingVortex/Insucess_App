import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import streamlit as st


json = {
    "type": "service_account",
    "project_id": st.secrets['project_id'],
    "private_key_id": st.secrets['KEY'],
    "private_key": st.secrets['private_key'],
    "client_email": st.secrets['client_email'],
    "client_id": st.secrets['client_id'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/case-693%40digital-layout-402513.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json, scope)
client = gs.authorize(credentials)
drive_service = build('drive', 'v3', credentials=credentials)

base_insucessos = client.open_by_key(st.secrets['base_insucessos']).worksheet('Insucessos')
base_cad = client.open_by_key(st.secrets['base_insucessos']).worksheet('CAD')
base_devolucoes = client.open_by_key(st.secrets['base_devolucoes']).worksheet('Comprovantes')
base_preventivo = client.open_by_key(st.secrets['base_preventivo']).worksheet('Base SQL')

sheet = client.open_by_key(st.secrets['base_devolucoes'])
base_saida = sheet.worksheet('Base_Len')
hist_saida = sheet.worksheet('Histórico_Len')

def preventivo(transportadora):
    log_data = base_preventivo.get_values('a1:q')
    df = pd.DataFrame(log_data[1:], columns=log_data[0])
    df = df.loc[(df['TRANSPORTADOR_TRACK'] == transportadora) & (df['FINALIZADOR'] == 'PENDENTE')] 
    return df[['PEDIDO','ROMANEIO','STATUS PRAZO','DATA_ENTREGA_PREVISTA','NOTA']]


def inserir_pedido(pedido, transportadora, motivo, observacao, filial):
    try:
        pedidos = base_insucessos.get_values('b1:b')
        for p in pedidos:
            if p[0] == str(pedido):
                return 'Pedido já está cadastrado, favor aguardar retorno!'
        registro = datetime.now() - timedelta(hours=3)
        registro = registro.strftime('%d/%m/%Y %H:%M:%S')
        
        last_row = len(base_insucessos.get_values('a1:a')) + 1
        r = 'a'+ str(last_row)
        base_insucessos.update([[str(registro), str(pedido), str(motivo), str(observacao), str(transportadora), str(filial)]], r)
        return 'Pedido registrado com sucesso!'
    except:
        return 'Ocorreu um erro, favor tente novamente!'
    
def transportadoras():
    transportadora = base_cad.get_values('e2:e')
    trans = []
    for tr in transportadora: 
        trans.append(tr[0])
    return trans

def motivos():
    motivos = base_cad.get_values('m2:m')
    mot = []
    for m in motivos:
        mot.append(m[0])
    return mot
    
def upload_arquivo(arquivo, nome):
    nome = str(nome)
    tipo = arquivo.type
    tipo = tipo.split('/')[1]
    
    with open(nome + f".{tipo}", "wb") as f:
        f.write(arquivo.read())

    file_metadata = {'name': f'{nome}.{tipo}'}
    media = MediaFileUpload(nome + f".{tipo}", mimetype=arquivo.type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

  
    drive_service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    
    file_id = file.get('id')
    file_link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing' #link de compartilhamento

    return file_link


def registro_dev(pedido, transportadora, arq, destino):
    try:    
        arquivo = upload_arquivo(arq, pedido)
        last_row = len(base_devolucoes.get_values('a:a')) + 1
        carimbo = (datetime.now() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        base_devolucoes.update([[str(carimbo),str(pedido),str(transportadora),str(arquivo),str(destino)]], f'a{str(last_row)}')
        return 'Sucesso','Devolução registrada com sucesso.'
    except:
        return 'Erro', "Ocorreu um erro, favor tentar novamente."

def consultar_pedidos_len( transportadora=0):
    df = pd.DataFrame(base_saida.get_values('a2:h'))
    df = df[[0,1,2,3,4,5,6,7]]
    df.columns = ['Registro', 'Filial', 'Pedido', 'Transportadora', 'Lote', 'Nota', 'Ult_Atualização', 'Status']
    df['Pedido'] =  df['Pedido'].astype(str)
    df = df.loc[df['Transportadora'] == str(transportadora)]
    return df

def import_lote(transportadora = None, lote = 0):
    try:
        last_row = len(hist_saida.get_values('a:a')) + 1
        df = pd.DataFrame(base_saida.get_values('c2:h'))
        df = df.loc[(df[2] == str(lote)) & (df[5] == 'Solicitado')]
        if df.empty:
            return 'Lote já importado ou não existe.'
        df[6] = 'Importado'
        now = (datetime.now() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        df[7] = now
        df[8] = transportadora
        df = df[[0,6,7,2,8]]
        hist_saida.update(df.values.tolist(), 'a'+str(last_row),value_input_option='USER_ENTERED')
        return 'Lote importado com sucesso!'
    except:
        return 'Erro ao importar Lote!'

def update_status(pedido, transportadora, status):
    try:
        pedidos = base_saida.get_values('c2:c')
        if [str(pedido)] not in pedidos:
            return 'Pedido não existe'
        last_row = len(hist_saida.get_values('a:a')) + 1
        now = (datetime.now() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        hist_saida.update( [[pedido, status, now, '', transportadora]] , 'a'+str(last_row),value_input_option='USER_ENTERED')
        return 'Status atualizado'
    except:
        return 'Ocorreu um erro ao atualizar o status!'
        
def consulta_lotes():
    lotes = base_saida.get_values('e2:e')
    lotes_sem_duplicatas = list(set(tuple(sublist) for sublist in lotes))
    lorrr = []
    for errr in lotes_sem_duplicatas: 
        lorrr.append(errr[0])
    return lorrr

def consultar_pedidos_importar(lote):
    df = pd.DataFrame(base_saida.get_values('a2:h'))
    df = df[[0,1,2,3,4,5,6,7]]
    df.columns = ['Registro', 'Filial', 'Pedido', 'Transportadora', 'Lote', 'Nota', 'Ult_Atualização', 'Status']
    df['Pedido'] =  df['Pedido'].astype(str)
    df = df.loc[(df['Lote'] == str(lote)) & (df['Status'] == str('Solicitado'))]
    return df

def consultar_pedidos_status(pedido):
    df = pd.DataFrame(base_saida.get_values('a2:h'))
    df = df[[0,1,2,3,4,5,6,7]]
    df.columns = ['Registro', 'Filial', 'Pedido', 'Transportadora', 'Lote', 'Nota', 'Ult_Atualização', 'Status']
    df['Pedido'] =  df['Pedido'].astype(str)
    df = df.loc[(df['Pedido'] == str(pedido))]
    return df

def atualizar_status(df, status, trans):
    try:
        if df.empty:
            return 'Sem pedido ativo'
        last_row = len(hist_saida.get_values('a:a')) + 1
        df['NOVO_STATUS'] = status
        df['Carimbo'] = (datetime.now() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
        df['trans'] = trans
        df = df[['Pedido', 'NOVO_STATUS', 'Carimbo', 'Lote', 'trans']]
        hist_saida.update(df.values.tolist(), 'a'+str(last_row),value_input_option='USER_ENTERED')
        return 'Status Atualizados'
    except Exception as e:
        return 'Erro ao registrar Status'
