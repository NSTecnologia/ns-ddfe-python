from src.DDFeAPI import DDFeAPI

ddfeAPI = DDFeAPI()

cnpjInteressado = ''
caminho = './Notas/'
tpAmb = '1'
nsu = '' #Fica vazio quando a cnsulta por chave
modelo = '55'
chave = '26241041317392000102550010000043621556056452'
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
    com_eventos=apenasComXML)

print(retorno)