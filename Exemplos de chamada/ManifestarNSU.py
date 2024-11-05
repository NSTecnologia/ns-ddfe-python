from src.DDFeAPI import DDFeAPI

ddfeAPI = DDFeAPI()

CNPJInteressado = ''
tpEvento = '210200'  
nsu = '134'  

retorno_nsu = ddfeAPI.manifestacao(CNPJInteressado, tpEvento, nsu=nsu)
print("Resultado da Manifestação por NSU:", retorno_nsu)