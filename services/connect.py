import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    './services/credentials.json', scope)
client = gs.authorize(credentials)

base_insucessos = client.open_by_key('1SjqHE5LsPYCCldD7ZoXMKFrRGE1oD9FdhK7uHZ8S8Co').worksheet('Insucessos')
base_cad = client.open_by_key('1SjqHE5LsPYCCldD7ZoXMKFrRGE1oD9FdhK7uHZ8S8Co').worksheet('CAD')

def verificar_pedidos(usuario):
    pedidos = base_insucessos.get_values('a2:n')   
    df = pd.DataFrame(pedidos)
    df = df[[0,1,2,3,4,11,13]]
    df.columns = ['Registro', 'Pedido', 'Motivo', 'Observação', 'Transportadora', 'Histórico', 'Status']
    df['Registro'] = pd.to_datetime(df['Registro'], format='%d/%m/%Y %H:%M:%S')
    df = df[df['Transportadora'] == usuario]
    
    return df.sort_values('Registro', ascending=False)

def inserir_pedido(pedido, transportadora, motivo, observacao):
    try:
        registro = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        last_row = len(base_insucessos.get_values('a1:a')) + 1
        r = 'a'+ str(last_row)
        base_insucessos.update([[str(registro), str(pedido), str(motivo), str(observacao), str(transportadora)]], r)
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
        mot.append(m)
    return mot
    

