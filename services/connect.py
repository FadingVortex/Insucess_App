import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import streamlit as st


json = {
    "type": "service_account",
    "project_id": "digital-layout-402513",
    "private_key_id": st.secrets['KEY'],
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCs4IPJIjOGPMaO\np1l6MWDUl8XKGU1Nlqeu8VBNoXJktFCilIdV9Rjpjt/Yz0//TASLBD2bw1L8Q1pZ\n3ONSn+OzTxm03RQ8tgT1Y5cM50N/V3HLEPFEWdqe8OJjrdY+CUkW1wHPOdypZMNI\nMt6l9uUcmfNHyZePSPp2zgMS6QAPbBWCsOcUCZLzR9RGzkROtmE4VZsTcw/oyTGA\nzXArIxz+IRUY15dOsTqw/UOuaHzuUN6f4hCeGzDrAYT8lev94Jk2YEmhz8bEhVXW\nu4jlrzDTsihl78ENYm+/tuY60LRqWGYxdXX4bc5IYiVkWkKhzFn0AAE2BtwZIoY/\n8sFdKVC/AgMBAAECggEAF4CAOgBFy+qIPc1/aw66cLxfXb251iH0kuJofd1EbW9c\nBPY3PdbPt7S+Nr3cTMM7XODLNVlE91l6t3vBhbKJ5I8M2hsyDJzcKLYMy2rHMNEk\n/avEePvULkZmKJHx7cYaYxoAu3jMyFST/cU4ooxhklVVjv1Xdtm/fxY7sb7uTKo1\npCCBL4mUnLLue8tHl4eveIwLUJPyFYvd7cMUQVSrh3HVc1eRsTst02cuULIwNkG7\nuolNYqIZtOGmm5Kr0RJJu6IA5B2+O2NGdB1P5Yw6yPr1TJCnzejn+/fsa92wtyUI\n1b2MxLRLmHTp0nFAheO0gehx+LC6czihmG4a3ll9VQKBgQDzirdM/EBI7JmP3Bp3\n5g+ErJwCRy5xfotq9s7NQDDb+Y8bhRsdppFiRDF2uasvd9htxVf+u3zACssDXHW/\n/70Jmsd/IHKODFsjo/9OgGajweUIlg6DIsFa5NA4Ty3vTPaeDLRiqNH1ISlQ8+M8\n8NF/EJpZso04dSU/qEt2tJmfLQKBgQC1uGmf1qAuiNskvwNK6bbSp6OXUIyMU9wC\nzbgRFYgEL53jTb29Dn2hJ2tOwzem5aCJ5sO2FX3j/yJV+Rrb/faoBOIs5jqSzyMP\ndnPDIJ8ScZ69lhks1SjK0BI+CernHHDhvLMYrUNtUvCHVmMjxWccaVbNexf4bykk\ne+8z43gDGwKBgDWBHjAdowniYQJH+tCojHQ7b7LYbI2mnX6MZnaVSaaqNxR2s7RZ\n6crK7IsG02MEU1oaZvChxBB0zpEYeQ4LYz5+8KEvQbuPX15/IxHeB66mZGj0fo+0\nzQHpDw2v54mRQQUMCX07VZUjCe6tBhlXVs8xmJdoMLpckihgEuQrXSypAoGAHTKO\nNhJkFlYC7/qI6uZ2a45n6I4Wpw1qUkD/jC8rdZC5C6aYD+JeKSCOS09uh7BphP7A\n/2agnZuGxs2JlUNO+FwggxpS2vfRKFDd9MIvDOWYndmaHev56+xWogUx6wRU1tBc\n7mAYb15eK0CkGUFEefoq6kUW6uHheG05V9r6k3UCgYEAutN3kL8oCjPcdaLO1VMl\nUZjsHaB1HMZcpI4UlA47TT0A0UnbrcwrWj9r7gaxpZ2Uc41q4ti1v2bPfoY4yTFD\ngPROIKCQ9EdNQfYQZOvmb30Nn8QJpF8BqrdF+ZHypUBvwk42j+UaZjGdAX03CB2M\nIdRqBfEIFS+sX/5yCVWNIcI=\n-----END PRIVATE KEY-----\n",
    "client_email": "case-693@digital-layout-402513.iam.gserviceaccount.com",
    "client_id": "105411206985054446095",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/case-693%40digital-layout-402513.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json, scope)
client = gs.authorize(credentials)
drive_service = build('drive', 'v3', credentials=credentials)

base_insucessos = client.open_by_key('1SjqHE5LsPYCCldD7ZoXMKFrRGE1oD9FdhK7uHZ8S8Co').worksheet('Insucessos')
base_cad = client.open_by_key('1SjqHE5LsPYCCldD7ZoXMKFrRGE1oD9FdhK7uHZ8S8Co').worksheet('CAD')
base_devolucoes = client.open_by_key('1eqYyWwshEQPo0DpkhdgrG2ZLycJrj8kGprgRoHrnAGc').worksheet('Comprovantes')
base_preventivo = client.open_by_key('1gPbStQWesvP3SyUB9r3RmiqHTKncrfFoOlCo_kzaRMU').worksheet('Base SQL')


def preventivo(transportadora):
    log_data = base_preventivo.get_values('a1:q')
    df = pd.DataFrame(log_data[1:], columns=log_data[0])
    df = df.loc[(df['TRANSPORTADOR_TRACK'] == transportadora) & (df['FINALIZADOR'] == 'PENDENTE')] 
    return df[['PEDIDO','ROMANEIO','STATUS PRAZO','DATA_ENTREGA_PREVISTA']]


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