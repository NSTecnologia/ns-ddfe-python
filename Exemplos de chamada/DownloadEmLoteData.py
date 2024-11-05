# DownloadLote.py
from src.DDFeAPI import DDFeAPI

# Instancia a classe DDFeAPI
ddfeAPI = DDFeAPI()

# Parâmetros para realizar o download em lote
cnpjInteressado = ''
caminho = './Notas/'
tpAmb = '1' 
ultNSU = '' 
dhInicial = '01/08/2024 00:00:00-03:00'
dhFinal = '20/08/2024 00:00:00-03:00'
incluirPDF = 'true'
apenasComXML = 'false'
comEventos = 'true'

# Realiza o download em lote de documentos
retorno = ddfeAPI.download_lote(
    cnpj_interessado=cnpjInteressado,
    caminho=caminho,
    tp_amb=tpAmb,
    ult_nsu=ultNSU,
    dhInicial=dhInicial,
    dhFinal=dhFinal,
    apenas_com_xml=apenasComXML,
    com_eventos=comEventos,
    incluir_pdf=incluirPDF
)

print(retorno)
