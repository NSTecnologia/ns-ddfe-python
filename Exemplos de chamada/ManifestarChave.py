from src.DDFeAPI import DDFeAPI

ddfeAPI = DDFeAPI()

CNPJInteressado = ''
tpEvento = '210200'  # Exemplo de "Confirmação da Operação"
xJust = 'TESTE INTEGRAÇÃO NS TECNOLOGIA'  # Justificativa, usada apenas para 210240
chave = ''  # Chave do DF-e

# Chamada da função de manifestação usando a Chave
retorno_chave = ddfeAPI.manifestacao(CNPJInteressado, tpEvento, chave=chave, xJust=xJust)
print("Resultado da Manifestação por Chave:", retorno_chave)
