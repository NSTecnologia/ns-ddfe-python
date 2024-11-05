from src.DDFeAPI import DDFeAPI

ddfeAPI = DDFeAPI()

cnpjInteressado = ''
caminho = './Notas/'
tpAmb = '1'
nsu = '3801'
modelo = '55'
chave = '' #Deixar vazio quando o download por por nsu
incluirPDF = 'true'
apenasComXML = 'false'
comEventos = 'false'

retorno = ddfeAPI.download_unico(
    cnpj_interessado=cnpjInteressado,
    caminho=caminho,
    tp_amb=tpAmb,
    nsu=nsu,
    modelo=modelo,
    chave=chave,
    incluir_pdf=incluirPDF,
    apenas_com_xml=apenasComXML,
    com_eventos=comEventos)

print(retorno)

