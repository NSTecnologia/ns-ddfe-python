# DownloadLote.py
from src.DDFeAPI import DDFeAPI

# Instancia a classe DDFeAPI
ddfeAPI = DDFeAPI()

# Parâmetros para realizar o download em lote
cnpjInteressado = ''
caminho = './Notas/'
tpAmb = '1' 
ultNSU = '3780' 
dhInicial = ''
dhFinal = ''
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
