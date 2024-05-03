import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    './services/credentials.json', scope)
client = gs.authorize(credentials)
drive_service = build('drive', 'v3', credentials=credentials)

base_insucessos = client.open_by_key('1SjqHE5LsPYCCldD7ZoXMKFrRGE1oD9FdhK7uHZ8S8Co').worksheet('Insucessos')
base_cad = client.open_by_key('1SjqHE5LsPYCCldD7ZoXMKFrRGE1oD9FdhK7uHZ8S8Co').worksheet('CAD')
base_devolucoes = client.open_by_key('1eqYyWwshEQPo0DpkhdgrG2ZLycJrj8kGprgRoHrnAGc').worksheet('Comprovantes')

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'andrew.dantas@magazineluiza.com.br'
smtp_password = 'ffbu aqdo duxw dhlu'


def enviar_email(texto):
        # Construir o e-mail
    sender_email = 'andrew.dantas@magazineluiza.com.br'
    receiver_email = 'gerente@magazineluiza.com.br'
    subject = 'Teste de E-mail'
    body = texto

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Iniciar conexão SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login no servidor SMTP
    server.login(smtp_username, smtp_password)

    # Enviar e-mail
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)

    # Encerrar conexão SMTP
    server.quit()

def verificar_pedidos(usuario):
    pedidos = base_insucessos.get_values('a2:n')   
    df = pd.DataFrame(pedidos)
    df = df[[0,1,2,3,4,11,13]]
    df.columns = ['Registro', 'Pedido', 'Motivo', 'Observação', 'Transportadora', 'Histórico', 'Status']
    df['Registro'] = pd.to_datetime(df['Registro'], format='%d/%m/%Y %H:%M:%S')
    df = df[df['Transportadora'] == usuario]
    
    return df.sort_values('Registro', ascending=False)

def inserir_pedido(pedido, transportadora, motivo, observacao, filial):
    try:
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