import base64
import requests
import json
import os
from datetime import datetime

class DDFeAPI:
    def __init__(self):
        self.token = 'COLOQUE SEU TOKEN AQUI'

    # Esta função envia um conteúdo para uma URL, em requisições do tipo POST
    def envia_conteudo_para_api(self, conteudo_a_enviar, url, tp_conteudo):
        headers = {
            'X-AUTH-TOKEN': self.token,
            'Content-Type': 'application/json' if tp_conteudo == 'json' else 'application/xml' if tp_conteudo == 'xml' else 'text/plain'
        }
        try:
            response = requests.post(url, headers=headers, data=conteudo_a_enviar)
            response.raise_for_status()  # Lança um erro para códigos de status de erro
            resposta_json = response.json()
            print('Resposta completa da API:', json.dumps(resposta_json, indent=4))
            return resposta_json
        except requests.RequestException as e:
            print('Erro na comunicação:', e)
            print('Info:', response.text if 'response' in locals() else 'Sem resposta')

    # Para manifestar um documento emitido contra seu cliente
    def manifestacao(self, cnpj_interessado, tp_evento, nsu='', x_just='', chave=''):
        if nsu:
            json_data = {
                "CNPJInteressado": cnpj_interessado,
                "nsu": nsu,
                "manifestacao": {
                    "tpEvento": tp_evento,
                    "xJust": x_just if tp_evento == '210240' else None
                }
            }
        else:
            json_data = {
                "CNPJInteressado": cnpj_interessado,
                "chave": chave,
                "manifestacao": {
                    "tpEvento": tp_evento,
                    "xJust": x_just if tp_evento == '210240' else None
                }
            }

        url = 'https://ddfe.ns.eti.br/events/manif'
        self.grava_linha_log('[MANIFESTACAO_DADOS]')
        self.grava_linha_log(json.dumps(json_data))

        resposta = self.envia_conteudo_para_api(json.dumps(json_data), url, "json")

        self.grava_linha_log('[MANIFESTACAO_RESPOSTA]')
        self.grava_linha_log(json.dumps(resposta, indent=4))

        return self.tratamento_manifestacao(resposta)

    def tratamento_manifestacao(self, json_retorno):
        x_motivo = ''
        status = json_retorno.get('status')

        if status == 200:
            x_motivo = json_retorno['retEvento']['xMotivo']
        elif status == -3:
            x_motivo = json_retorno['erro']['xMotivo']
        else:
            x_motivo = json_retorno.get('motivo', '')

        print(x_motivo)
        self.grava_linha_log(x_motivo)

    # Para fazer o download de um unico documento
    def download_unico(self, cnpj_interessado, caminho, tp_amb, nsu='', modelo='', chave='', incluir_pdf='false', apenas_com_xml='false', com_eventos='false'):
        json_data = {
            "CNPJInteressado": cnpj_interessado,
            "modelo": modelo,
            "incluirPDF": incluir_pdf.lower() == 'true',
            "tpAmb": tp_amb,
            "nsu" if nsu else "chave": nsu if nsu else chave,
            "apenasComXml": apenas_com_xml.lower() == 'true',
            "comEventos": com_eventos.lower() == 'true'
        }

        url = 'https://ddfe.ns.eti.br/dfe/unique'
        self.grava_linha_log('[DOWNLOAD_UNICO_DADOS]')
        self.grava_linha_log(json.dumps(json_data))

        resposta = self.envia_conteudo_para_api(json.dumps(json_data), url, "json")
        self.grava_linha_log('[DOWNLOAD_UNICO_RESPOSTA]')
        self.grava_linha_log(json.dumps(resposta, indent=4))

        return self.tratamento_download_unico(caminho, incluir_pdf, resposta)

    def tratamento_download_unico(self, caminho, incluir_pdf, json_retorno):
        status = json_retorno.get('status')

        if status == 200:
            self.download_doc_unico(caminho, incluir_pdf, json_retorno)
            print('Download Único feito com sucesso')
        else:
            print(json.dumps(json_retorno, indent=4))

    def download_doc_unico(self, caminho, incluir_pdf, json_retorno):
        lista_docs = json_retorno.get('listaDocs', [])
        
        if not caminho.endswith('\\'):
            caminho += '\\'

        if not lista_docs:
            xml = json_retorno.get('xml')
            chave = json_retorno.get('chave')
            modelo = json_retorno.get('modelo')
            self.salva_xml(xml, caminho, chave, modelo)

            if incluir_pdf == 'true':
                pdf = json_retorno.get('pdf')
                self.salva_pdf(pdf, caminho, chave, modelo)
        else:
            array_xmls = json_retorno.get('xmls', [])

            for doc_xml in array_xmls:
                xml = doc_xml.get('xml')

                if xml:
                    chave = doc_xml.get('chave')
                    modelo = doc_xml.get('modelo')
                    tp_evento = doc_xml.get('tpEvento', '')

                    self.salva_xml(xml, caminho, chave, modelo, tp_evento)

                    if incluir_pdf == 'true':
                        pdf = doc_xml.get('pdf')
                        self.salva_pdf(pdf, caminho, chave, modelo, tp_evento)

    # Para fazer o download de lote de documentos
    def download_lote(self, cnpj_interessado, caminho, tp_amb, ult_nsu, dhInicial, dhFinal, apenas_com_xml='false', com_eventos='true', incluir_pdf='true'):
        if isinstance(ult_nsu, str) and ult_nsu.isdigit():
            ult_nsu = int(ult_nsu)
        
        if (dhInicial == '' or dhFinal == ''):
            json_data = {
                "CNPJInteressado": cnpj_interessado,
                "ultNSU": ult_nsu,
                "tpAmb": tp_amb,
                "incluirPDF": incluir_pdf,
                "comEventos": com_eventos,
            }
        else:
            json_data = {
                "CNPJInteressado": cnpj_interessado,
                "dhInicial": dhInicial,
                "dhFinal": dhFinal,
                "tpAmb": tp_amb,
                "incluirPDF": incluir_pdf,
                "apenasComXml": apenas_com_xml,
                "comEventos": com_eventos,
            }

        url = 'https://ddfe.ns.eti.br/dfe/bunch'
        
        self.grava_linha_log('[DOWNLOAD_LOTE_DADOS]')
        self.grava_linha_log(json.dumps(json_data))

        resposta = self.envia_conteudo_para_api(json.dumps(json_data), url, "json")

        self.grava_linha_log('[DOWNLOAD_LOTE_RESPOSTA]')
        self.grava_linha_log(json.dumps(resposta, indent=4))

        self.tratamento_download_lote(caminho, incluir_pdf, resposta)
        
        return resposta

    def tratamento_download_lote(self, caminho, incluir_pdf, json_retorno):
        status = json_retorno.get('status')
        if status == 200:
            print('último NSU:', self.download_docs_lote(caminho, incluir_pdf, json_retorno))
        else:
            print(json.dumps(json_retorno, indent=4))

    def download_docs_lote(self, caminho, incluir_pdf, json_retorno):
        if not caminho.endswith(os.sep):
            caminho += os.sep
            
        array_xmls = json_retorno.get('xmls', [])
        for doc_xml in array_xmls:
            xml = doc_xml.get('xml')

            if xml:
                chave = doc_xml.get('chave')
                modelo = doc_xml.get('modelo')
                tp_evento = doc_xml.get('tpEvento') or ''

                self.salva_xml(xml, caminho, chave, modelo, tp_evento)

                if incluir_pdf == 'true':
                    pdf = doc_xml.get('pdf')
                    self.salva_pdf(pdf, caminho, chave, modelo, tp_evento)

        return json_retorno.get('ultNSU')

    #utilitários
    def grava_linha_log(self, msg):
        dir_log = './log/'
        if not os.path.exists(dir_log):
            os.makedirs(dir_log)
        with open(os.path.join(dir_log, f"{datetime.now():%Y%m%d}.log"), 'a+') as arq:
            msg = f"[{datetime.now():%Y/%m/%d %H:%M:%S}]: {msg}\n"
            arq.write(msg)

    def salva_pdf(self, pdf, caminho, chave, modelo, tp_evento=''):
        if pdf is None:
            self.grava_linha_log("Erro: PDF não encontrado para o documento")
            return
        
        extencao = {
            55: '-procNFe.pdf',
            57: '-procCTe.pdf'
        }.get(modelo, '-procNFSeSP.pdf')

        pdf_dir = os.path.join(caminho, 'pdfs')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        local_salvar = os.path.join(pdf_dir, f"{chave}{tp_evento}{extencao}")
        
        with open(local_salvar, "wb") as f:
            f.write(base64.b64decode(pdf))
        
        self.grava_linha_log(f"Arquivo salvo em {local_salvar}")

    def salva_xml(self, xml, caminho, chave, modelo, tp_evento=''):
        extencao = {
            55: '-procNFe.xml',
            57: '-procCTe.xml'
        }.get(modelo, '-procNFSeSP.xml')

        xml_dir = os.path.join(caminho, 'xmls')
        if not os.path.exists(xml_dir):
            os.makedirs(xml_dir)

        local_salvar = os.path.join(xml_dir, f"{chave}{tp_evento}{extencao}")
        
        with open(local_salvar, "w", encoding="utf-8") as f:
            f.write(xml)

        self.grava_linha_log(f"Arquivo salvo em {local_salvar}")
