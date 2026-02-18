#Importar da biblioteca Selenium o navegador
from selenium import webdriver
#Importar da biblioteca Selenium o método By
from selenium.webdriver.common.by import By
#Importar da biblioteca Selenium o método Select
from selenium.webdriver.support.select import Select
#importar ferramenta que permite criar uma expera
from selenium.webdriver.support.ui import WebDriverWait
#importar ferramenta que permite determinar uma condição que o programa avance para a próxima linha
from selenium.webdriver.support import expected_conditions as EC
#Importar ferramenta para tratar exceções
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
#Importar da biblioteca date tame o método datetime
import datetime
#Importar da biblioteca time o método sleep
import time
#Importar a biblioteca pandas, nomeando-a "pd"
from time import sleep
#Importar a biblioteca random
import random
import os
import re

#DEFINE DICIONÁRIO DE CLASSES PROCESSUAIS
todas_as_classes_processuais = {'Classes' :['Ação Cautelar'
                                            'Ação Cível Originária'
                                            'Ação Declaratória de Constitucionalidade',
                                            'Ação Direta de Inconstitucionalidade',
                                            'Ação Direta de Inconstitucionalidade por Omissão',
                                            'Arguição de Descumprimento de Preceito Fundamental',
                                            'Agravo de Instrumento','Arguição de Impedimento',
                                            'Ação Originária','Ação Originária Especial',
                                            'Ação Penal','Ação Rescisória','Recurso Extraordinário com Agravo',
                                            'Arguição de Suspeição','Conflito de Competência','Comunicação',
                                            'Exceção de Incompetência',
                                            'Exceção de Litispendência',
                                            'Extradição','Habeas Corpus',
                                            'Habeas Data','Intervenção Federal',
                                            'Inquérito','Mandado de Injunção',
                                            'Mandado de Segurança','Petição',
                                            'Prisão Preventiva para Extradição',
                                            'Proposta de Súmula Vinculante',
                                            'Reclamação','Recurso Extraordinário',
                                            'Recurso em Habeas Corpus','Recurso em Habeas Data',
                                            'Recurso em Mandado de Injunção',
                                            'Recurso em Mandado de Segurança',
                                            'Revisão Criminal',
                                            'Suspensão do Incidente de Resolução de Demandas Repetitivas',
                                            'Suspensão de Liminar','Suspensão de Segurança',
                                            'Suspensão de Tutela Provisória','Tutela Provisória Antecedente',
                                            'Admissão de Assistente',
                                            'Impugnação ao valor da causa',
                                            'Incidente de falsidade',
                                            'Oposição','Suspeição de perito',
                                            'Embargos à Execução',
                                            'Cumprimento de Sentença',
                                            'Execução contra a Fazenda Pública',
                                            'Execução de Pena',
                                            'Extensão','Incidente de Assunção de Competência',
                                            'Tutela Provisória Incidental',
                                            'Agravo Regimental',
                                            'Embargos de Declaração',
                                            'Embargos Divergentes',
                                            'Embargos Infringentes'],
                                 'Siglas' :['AC',
                                            'ACO',
                                            'ADC',
                                            'ADI',
                                            'ADO',
                                            'ADPF',
                                            'AI',
                                            'AImp',
                                            'AO',
                                            'AOE',
                                            'AP',
                                            'AR',
                                            'ARE',
                                            'AS',
                                            'CC',
                                            'Cm',
                                            'EI',
                                            'EL',
                                            'Ext',
                                            'HC',
                                            'HD',
                                            'IF',
                                            'Inq',
                                            'MI',
                                            'MS',
                                            'Pet',
                                            'PPE',
                                            'PSV',
                                            'Rcl',
                                            'RE',
                                            'RHC',
                                            'RHD',
                                            'RMI',
                                            'RMS',
                                            'RvC',
                                            'SIRDR',
                                            'SL',
                                            'SS',
                                            'STP',
                                            'TPA',
                                            'AAs',
                                            'IVC',
                                            'IFa',
                                            'Ops',
                                            'SPer',
                                            'EE',
                                            'CS',
                                            'EFP',
                                            'EP',
                                            'Extn',
                                            'IAC',
                                            'TPI',
                                            'AgR',
                                            'ED',
                                            'EDv',
                                            'EI'],
                                 'Partes_ativas': ['Agravante',
                                                   'Arguente',
                                                   'Autor',
                                                   'Comunicante',
                                                   'Embargante',
                                                   'Excipiente',
                                                   'Exequente',
                                                   'Impetrante',
                                                   'Impugnante',
                                                   'Opoente',
                                                   'Paciente',
                                                   'Proponente',
                                                   'Reclamante',
                                                   'Recorrente',
                                                   'Requerente',
                                                   'Suscitante',
                                                   'Polo ativo',
                                                   'Querelante'],
                                 'Abreviaturas_partes_ativas':['AGTE.(S)',
                                                               'ARGTE.(S)',
                                                               'AUTOR(A/S)(ES)',
                                                               'COMTE.(S)',
                                                               'EMBTE.(S)',
                                                               'EXCPTE.(S)',
                                                               'EXQTE.(S)',
                                                               'IMPTE.(S)',
                                                               'IMPUGTE.(S)',
                                                               'OPOENTE(S)',
                                                               'PACTE.(S)',
                                                               'PROPTE.(S)',
                                                               'RECLTE.(S)',
                                                               'RECTE.(S)',
                                                               'REQTE.(S)',
                                                               'SUSTE.(S)',
                                                               'POLO AT',
                                                               'QTE.(S)'],
                                 'Partes_passivas': ['Agravado',
                                                     'Arguido',
                                                     'Beneficiário',
                                                     'Coator',
                                                     'Embargado',
                                                     'Excepto',
                                                     'Executado',
                                                     'Extraditando',
                                                     'Impetrado',
                                                     'Impugnado',
                                                     'Investigado',
                                                     'Oposto',
                                                     'Reclamado',
                                                     'Recorrido',
                                                     'Requerido',
                                                     'Réu',
                                                     'Suscitado',
                                                     'Polo passivo',
                                                     'Querelado'],
                                 'Abreviaturas_partes_passivas':['AGDO.(A/S)',
                                                                 'ARGDO.(A/S)',
                                                                 'BENEF.(A/S)',
                                                                 'COATOR(A/S)(ES)',
                                                                 'EMBDO.(A/S)',
                                                                 'EXCPTO.(A/S)',
                                                                 'EXCDO.(A/S)',
                                                                 'EXTDO.(A/S)',
                                                                 'IMPDO.(A/S)',
                                                                 'IMPUGDO.(A/S)',
                                                                 'INVEST.(A/S)',
                                                                 'OPOSTO(S)',
                                                                 'RECLDO.(A/S)',
                                                                 'RECDO.(A/S)',
                                                                 'REQDO.(A/S)',
                                                                 'RÉU(É)(S)',
                                                                 'SUSDO.(A/S)'
                                                                 ,'POLO PAS'
                                                                 ,'QDO.(A/S)'],
                                 'Procuradores': ['ADVOGADO(A/S)',
                                                  'ADVOGADO(A/S) DATIVO(A/S)',
                                                  'ADVOGADO(A/S) LITISCONSORTE(S)',
                                                  'DEFENSOR PÚBLICO',
                                                  'PROCURADOR(ES)'],
                                 'Abreviaturas_procuradores': ['ADV.(A/S)',
                                                               'ADV.DAT.(A/S)',
                                                               'ADV.LIT.(A/S)',
                                                               'DP',
                                                               'PROC.(A/S)(ES)'],
                                 'Terceiros': ['AMICUS CURIAE',
                                               'ASSISTENTE LITISCONSORCIAL',
                                               'ASSISTENTE(S)',
                                               'AUTORIDADE POLICIAL',
                                               'BENEFICIÁRIO(A/S)',
                                               'CURADOR(A/S)(ES) ESPECIAL(AIS)',
                                               'INTERESSADO(A/S)',
                                               'LITISCONSORTE',
                                               'LITISCONSORTE ATIVO',
                                               'LITISCONSORTE PASSIVO'],
                                 'Abreviaturas_terceiros': ['AM. CURIAE.',
                                                            'ASS.LIT.',
                                                            'ASSIST.(S)',
                                                            'AUT. POL.',
                                                            'BENEF.(A/S)',
                                                            'CURADOR(A/S)(ES)',
                                                            'INTDO.(A/S)',
                                                            'LITISC.',
                                                            'LIT.ATIV.',
                                                            'LIT.PAS.'],
                                }

xpathes_pesquisar = {'Processos': '//ul[@class="seletores d-none d-md-block"]//span[@id="abaProcesso"]',
                     'Por_Classe_e_Número': '//option[@value="CLASSE_E_NUMERO"]',
                     'Classe': '//select[@id="Siglas"]',
                     'Digitar_núm_processo': '//input[@id="pesquisaPrincipalClasseNumero"]',
                     'Botão_pesquisar': '//div[@class="form-inline"]//button[@id="btnPesquisar"]',
                     }
xpathes_dados_buscados = {'Código_incidente': '//div[@class="titulo-processo m-0"]//input[@id="incidente"]',
                          'Processo eletrônico': '//div//span[@class="badge bg-primary"]',
                          'Processo físico' : '//div//span[@class="badge bg-secondary"]',
                          'Processo_público':'//div//span[@class="badge bg-success"]',
                          'Segredo_de_justiça': '//div//span[@class="badge bg-warning"]',
                          'Tipo_de_Prioridade': '//div//span[@class="badge bg-danger"]',
                          'Repercussao_geral': '//div//span[@class="badge bg-black"]',
                          'Número_único': '//div[@class="processo-rotulo"]',
                          'Relator': '//div[@class="processo-dados p-l-16"]',
                          'Órgão_de_origem': '//span[@id="orgao-procedencia"]//span[@id="orgao-procedencia"]',
                          'UF_origem': '//div[@class="processo-dados p-l-16"]//span[@id="descricao-procedencia"]//span[@id="descricao-procedencia"]',
                          'Aba_assunto': '//ul[@id="abas_processo"]//a[@href="#informacoes"]',
                          'Assunto': '//div[@class="informacoes__assunto col-12 m-b-8 d-flex"]//li',
                          'Aba_partes': '//div[@class="menu-abas"]//a[@href="#partes"]',
                          'Atributos_sujeitos': '//div[@class="tab-content col-md-12"]//div[@class="detalhe-parte"]',
                          'Nomes_sujeitos': '//div[@class="tab-content col-md-12"]//div[@class="nome-parte"]',
                          'Andamentos': '//div[@id="andamentos"]',
                          'Número_inexistente': '//div[@class="message-404"]',
                          }

#Cria função espera_p_carregar:
def esperar_carregar(navegador, xpath):
   #Define o tempo padrão de 5s de espera
   espera_p_carregar = WebDriverWait(navegador, 3)
   #Estabelece que o elemento procurado procurado seja localizado, como condição para avançar na execução do código.
   espera_p_carregar.until(EC.presence_of_all_elements_located((By.XPATH,xpath)))

#Cria função clicar_em
def clicar_em (navegador, xpath):
    #Definir tempo de espera
    espera = WebDriverWait(navegador, 3)
    #Esperar até que o elemento procurado seja encontrado
    espera.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #Esperar até que o elemento procurado seja clicável
    espera.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #Definir onde clicar
    onde_clicar = navegador.find_element(By.XPATH, xpath)
    #Mostrar na tela o elemento
    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'})", onde_clicar)
    # Tentar clicar
    try:
       onde_clicar.click()
    # Se o método clicar não funcionar, tentar
    except:
       # Mostrar na tela o leemento
       navegador.execute_script("arguments[0].scrollIntoView({block: 'center'})", onde_clicar)
       # Clicar no elemento usando um comando diferente
       navegador.execute_script("arguments[0].click();", onde_clicar)

#Cria função pesquisar_por_classe_e_número
def pesquisar_por_classe_e_número (navegador, classe, número):
    #Encontrar campo de pesquisa de processos
    clicar_em_pesquisar_processos = clicar_em(navegador, xpathes_pesquisar['Processos'])
    #Clicar em critério de pesquisa
    selecionar_critério_de_pesquisa = clicar_em(navegador, xpathes_pesquisar['Por_Classe_e_Número'])
    #Buscar campo de seleção da classe
    campo_seleção = Select(encontrar_elemento(navegador, xpathes_pesquisar['Classe']))
    #Selecionar classe
    campo_seleção.select_by_visible_text(classe)
    #Encontrar campo onde será digitado o número do processo
    onde_digitar = encontrar_elemento(navegador, xpathes_pesquisar['Digitar_núm_processo'])
    #Digitar número do processo
    onde_digitar.send_keys(número)
    #Clicar no botão de pesquisa
    botão_de_pesquisa = clicar_em(navegador, xpathes_pesquisar['Botão_pesquisar'])

#Cria função encontrar elemento
def encontrar_elemento (navegador, xpath):
    esperar_carregar(navegador, xpath)
    resultado = navegador.find_element(By.XPATH, xpath)
    return resultado

def encontrar_todos_os_elementos(navegador, xpath):
   esperar_carregar(navegador, xpath)
   elementos = navegador.find_elements(By.XPATH, xpath)
   return elementos

def extrair_relator (lista):
   for elemento in lista:
        relator = ''
        buscar_relator = 'Relator:'
        if buscar_relator in elemento:
            relator = elemento
   return relator

def extrair_texto_de_vários_elementos (lista):
   lista_de_elementos = []
   for _, elemento in enumerate(lista):
      elemento = lista[_].text
      lista_de_elementos.append(elemento)
   return lista_de_elementos

def encontrar_indices(texto, substring):
    indices = []
    inicio = 0

    while True:
        # Encontra a próxima ocorrência da substring
        inicio = texto.find(substring, inicio)

        # Se não encontrar mais, sai do loop
        if inicio == -1:
            break

        # Adiciona o índice encontrado à lista
        indices.append(inicio)

        # Move o índice de início para a próxima posição
        inicio += len(substring)

    return indices

def textos_andamentos (lista_de_índices, texto):
    lista_de_andamentos = []
    for _, índice in enumerate(lista_de_índices):
        índice_início_nova_substring = índice
        if texto.find('<div class="andamento-item">',índice+1) != -1:
            índice_final_nova_substring = texto.find('<div class="andamento-item">',índice+1)
        else:
            índice_final_nova_substring = len(texto)
        nova_substring = texto[índice_início_nova_substring:índice_final_nova_substring]
        índice_início_data = nova_substring.find('<div class="andamento-data ">')+len('<div class="andamento-data ">')
        índice_fim_data = nova_substring.find('<',índice_início_data)
        data = nova_substring[índice_início_data:índice_fim_data]
        índice_início_título_andamento = nova_substring.find('<h5 class="andamento-nome ">')+len('<h5 class="andamento-nome ">')
        índice_final_título_andamento = nova_substring.find('<',índice_início_título_andamento)
        título = nova_substring[índice_início_título_andamento:índice_final_título_andamento].replace('\n',' ')
        if nova_substring.find('<div class="col-md-9 p-0">') != -1:
            índice_início_detalhamento = nova_substring.find('<div class="col-md-9 p-0">')+len('<div class="col-md-9 p-0">')
            índice_final_detalhamento = nova_substring.find('<',índice_início_detalhamento)
            detalhamento = nova_substring[índice_início_detalhamento:índice_final_detalhamento].replace('\n',' ')
            detalhamento = detalhamento.replace('&nbsp',' ')
        elif nova_substring.find('<div class="col-md-9 p-0 ">') != -1:
            índice_início_detalhamento = nova_substring.find('<div class="col-md-9 p-0 ">')+len('<div class="col-md-9 p-0 ">')
            índice_final_detalhamento = nova_substring.find('<',índice_início_detalhamento)
            detalhamento = nova_substring[índice_início_detalhamento:índice_final_detalhamento].replace('\n',' ')
            detalhamento = detalhamento.replace('&nbsp',' ')
        else:
            detalhamento =''
        if nova_substring.find('<a href="') != -1:
            índice_início_documento = nova_substring.find('<a href="')+len('<a href="')
            índice_final_documento = nova_substring.find('"',índice_início_documento)
            documento = nova_substring[índice_início_documento:índice_final_documento].replace('amp;','')
        else:
            documento =''
        if nova_substring.find('<i class="far fa-file-alt"></i>') != -1:
            índice_início_descrição_documento = nova_substring.find('<i class="far fa-file-alt"></i>')+len('<i class="far fa-file-alt"></i>')
            índice_final_descrição_documento = nova_substring.find('<',índice_início_descrição_documento)
            descrição_documento = nova_substring[índice_início_descrição_documento:índice_final_descrição_documento].strip()
        elif nova_substring.find('<i class="fas fa-download"></i>') != -1:
            índice_início_descrição_documento = nova_substring.find('<i class="fas fa-download"></i>')+len('<i class="fas fa-download"></i>')
            índice_final_descrição_documento = nova_substring.find('<',índice_início_descrição_documento)
            descrição_documento = nova_substring[índice_início_descrição_documento:índice_final_descrição_documento].strip()
        else:
            descrição_documento = ''
        if nova_substring.find('<span class="andamento-julgador badge bg-info ">') != -1:
            índice_início_órgão_julgador = nova_substring.find('<span class="andamento-julgador badge bg-info ">')+len('<span class="andamento-julgador badge bg-info ">')
            índice_final_órgão_julgador = nova_substring.find('<',índice_início_órgão_julgador)
            órgão_julgador = nova_substring[índice_início_órgão_julgador:índice_final_órgão_julgador].strip()
        else:
            órgão_julgador = ''
        andamentos = f'{data} - {título} # {detalhamento} * {órgão_julgador} $ {descrição_documento} -> {documento}'
        lista_de_andamentos.append(andamentos)
        # for andamento in lista_de_andamentos:
        #     if 'Lançamento indevido' in andamento:
        #         índice = lista_de_andamentos.index(andamento)
        #         lista_de_andamentos.remove(lista_de_andamentos[índice])
    return lista_de_andamentos

def pegar_partes(navegador):
    #PEGAR AS PARTES
    #Clicar na aba correspondente
    clicar_em(navegador, xpathes_dados_buscados['Aba_partes'])
    #Tentar encontrar os elementos contendo os atributos dos sujeitos do processo
    try:
        #Se forem encontradros, extrair os textos e criar uma lista
        buscar_atributos_sujeitos_processo = encontrar_todos_os_elementos(navegador, xpathes_dados_buscados['Atributos_sujeitos'])
        atributos_sujeitos = extrair_texto_de_vários_elementos(buscar_atributos_sujeitos_processo)
    except (TimeoutException, NoSuchElementException):
        #Se não forem encontrados, a lista ficará vazia
        atributos_sujeitos =[]
    #Tentar encontrar os elementos contendo os nomes dos sujeitos do processo
    try:
        #Se forem encontrados, extrair os textos e criar uma lista
        buscar_nome_sujeitos_processo = encontrar_todos_os_elementos(navegador, xpathes_dados_buscados['Nomes_sujeitos'])
        nomes_sujeitos = extrair_texto_de_vários_elementos(buscar_nome_sujeitos_processo)
    except (TimeoutException, NoSuchElementException):
        #Se não forem encontrados, a lista ficará vazia
        nomes_sujeitos = []
    #Criar uma lista para unificar as listas de atributos e nomes dos sujeitos do processo
    atributos_e_nomes_dos_sujeitos = []
    #Se a quantidade de sujeitos processuais for diferente de 0, a lista anteriomente criada deve ser
    #alimentada, unido os atributos e os nomes de cada um dos sujeitos processuais, excluídos o Relator.
    if len(atributos_sujeitos) != 0:
        #Para cada parte
        for _, parte in enumerate(range(0,len(buscar_atributos_sujeitos_processo))):
            #Unir os respectivos nomes e atributos
            parte = f'{atributos_sujeitos[_]}: {nomes_sujeitos[_]}'
            #Acrescentar cada parte à lista com os atritutos e os nomes das partes
            atributos_e_nomes_dos_sujeitos.append(parte)
    return list(dict.fromkeys(atributos_e_nomes_dos_sujeitos))

def separar_sujeitos_e_procuradores(lista_de_sujeitos):
    texto = '\n'.join(lista_de_sujeitos)
    polo_ativo = []
    procuradores_polo_ativo = []
    polo_passivo = []
    procuradores_polo_passivo = []
    terceiros = []
    procuradores_terceiros = []
    atributos_sujeitos = []

    for item in todas_as_classes_processuais['Abreviaturas_partes_ativas']:
        padrão_parte_ativa = rf"{re.escape(item)}.*"
        p1= re.compile(padrão_parte_ativa)
        padrão_atrib_p_ativa = rf"{re.escape(item)}*[:\s]"
        p2 = re.compile(padrão_atrib_p_ativa)
        correspondências1 = p1.finditer(texto)
        for correspondência in correspondências1:
            polo_ativo.append(correspondência.group())
        correspondências2 = p2.finditer(texto)
        for correspondência in correspondências2:
            if correspondência.group() not in atributos_sujeitos:
                atributos_sujeitos.append(correspondência.group())

    for item in todas_as_classes_processuais['Abreviaturas_partes_passivas']:
        padrão_parte_passiva = rf"{re.escape(item)}.*"
        p1 = re.compile(padrão_parte_passiva)
        padrão_atrib_p_passiva = rf"{re.escape(item)}*[:\s]"
        p2 = re.compile(padrão_atrib_p_passiva)
        correspondências1 = p1.finditer(texto)
        for correspondência in correspondências1:
            polo_passivo.append(correspondência.group())
        correspondências2 = p2.finditer(texto)
        for correspondência in correspondências2:
            if correspondência not in atributos_sujeitos:
                atributos_sujeitos.append(correspondência.group())

    for item in todas_as_classes_processuais['Abreviaturas_terceiros']:
        padrão_terceiros = rf"{re.escape(item)}.*"
        p1 = re.compile(padrão_terceiros)
        padrão_atrib_terceiros = rf"{re.escape(item)}*[:\s]"
        p2 = re.compile(padrão_atrib_terceiros)
        correspondências1 = p1.finditer(texto)
        for correspondência in correspondências1:
            terceiros.append(correspondência.group())
        correspondências2 = p2.finditer(texto)
        for correspondência in correspondências2:
            if correspondência.group() not in atributos_sujeitos:
                atributos_sujeitos.append(correspondência.group())

    lista_índices_substrings = []
    for atributo in atributos_sujeitos:
        índice = texto.find(atributo)
        lista_índices_substrings.append(índice)

    for _, índice in enumerate(lista_índices_substrings):
        início = lista_índices_substrings[_]
        try:
            fim = lista_índices_substrings[_+1]
        except:
            fim = len(texto)
        substring = texto[início:fim]

        for abreviatura in todas_as_classes_processuais['Abreviaturas_partes_ativas']:
            if abreviatura in substring:
                for item in todas_as_classes_processuais['Abreviaturas_procuradores']:
                    padrão_procuradores_polo_ativo = rf"{re.escape(item)}.*"
                    p1 = re.compile(padrão_procuradores_polo_ativo)
                    correspondências1 = p1.finditer(substring)
                    for correspondência in correspondências1:
                        procuradores_polo_ativo.append(correspondência.group())
        for abreviatura in todas_as_classes_processuais['Abreviaturas_partes_passivas']:
            if abreviatura in substring:
                for item in todas_as_classes_processuais['Abreviaturas_procuradores']:
                    padrão_procuradores_polo_passivo = rf"{re.escape(item)}.*"
                    p1 = re.compile(padrão_procuradores_polo_passivo)
                    correspondências1 = p1.finditer(substring)
                    for correspondência in correspondências1:
                        procuradores_polo_passivo.append(correspondência.group())
        for abreviatura in todas_as_classes_processuais['Abreviaturas_terceiros']:
            if abreviatura in substring:
                for item in todas_as_classes_processuais['Abreviaturas_procuradores']:
                    padrão_procuradores_terceiros = rf"{re.escape(item)}.*"
                    p1 = re.compile(padrão_procuradores_terceiros)
                    correspondências1 = p1.finditer(substring)
                    for correspondência in correspondências1:
                        if correspondência.group() not in procuradores_terceiros:
                            procuradores_terceiros.append(correspondência.group())
    return list(dict.fromkeys(polo_ativo)), list(dict.fromkeys(procuradores_polo_ativo)), list(dict.fromkeys(polo_passivo)), list(dict.fromkeys(procuradores_polo_passivo)), list(dict.fromkeys(terceiros)), list(dict.fromkeys(procuradores_terceiros))

def despachos_de_devolução_e_decisões(lista_andamentos):
    lista_documentos =[]
    contador = 0
    for andamento in lista_andamentos:
        if 'Despacho' in andamento and 'Determinada a devolução' in andamento:
            link_documento = andamento[andamento.find('-> ')+3:]
            if link_documento not in '\n'.join(lista_documentos):
                contador += 1
                nome_documento = f'Despacho de devolução {contador}'
                data_disponibilização = andamento[:andamento.find(' -')]
                despacho = f'{data_disponibilização} - {nome_documento} (despacho) # https://portal.stf.jus.br/processos/{link_documento}'
                lista_documentos.append(despacho)
        elif 'Decisão mono' in andamento:
            link_documento = andamento[andamento.find('-> ')+3:]
            data_disponibilização = andamento[:andamento.find(' -')]
            if link_documento not in '\n'.join(lista_documentos):
                contador += 1
                nome_documento = f'Decisão {contador}'
                ato_decisório = f'{data_disponibilização} - {nome_documento} (monocrática) # https://portal.stf.jus.br/processos/{link_documento}'
                lista_documentos.append(ato_decisório)
        elif 'Inteiro t' in andamento:
            link_documento = andamento[andamento.find('-> ')+3:]
            data_disponibilização = andamento[:andamento.find(' -')]
            if link_documento not in '\n'.join(lista_documentos):
                contador += 1
                nome_documento = f'Decisão {contador}'
                ato_decisório = f'{data_disponibilização} - {nome_documento} (acórdão) # https://portal.stf.jus.br/processos/{link_documento}'
                lista_documentos.append(ato_decisório)
    return lista_documentos

def outros_documentos(lista_andamentos):
    lista_documentos =[]
    for andamento in lista_andamentos:
        if 'Despacho' in andamento and 'Determinada a devolução' not in andamento:
            nome_documento = f'Despacho'
            link_documento = andamento[andamento.find('-> ')+3:]
            if link_documento not in '\n'.join(lista_documentos):
                data_disponibilização = andamento[:andamento.find(' -')]
                despacho = f'{data_disponibilização} - {nome_documento} (despacho) # https://portal.stf.jus.br/processos/{link_documento}'
                lista_documentos.append(despacho)
        elif 'download' in andamento and 'Decisão mono' not in andamento and 'Inteiro t' not in andamento:
            link_documento = andamento[andamento.find('-> ')+3:]
            data_disponibilização = andamento[:andamento.find(' -')]
            if link_documento not in '\n'.join(lista_documentos):
                nome_base = andamento[andamento.find(' $ ')+3:andamento.find(' -> ')].strip()
                nome_documento = f'{nome_base}'
                ato_decisório = f'{data_disponibilização} - {nome_documento} # https://portal.stf.jus.br/processos/{link_documento}'
                lista_documentos.append(ato_decisório)        
    return lista_documentos

def documentos_despachos_devolução (lista_andamentos):
    lista_documentos =[]
    contador = 0
    for andamento in lista_andamentos:
        if 'Despacho' in andamento and 'Determinada a devolução' in andamento:
            contador += 1
            nome_documento = f'Despacho de devolução {contador}'
            link_documento = andamento[andamento.find('-> ')+3:]
            data_disponibilização = andamento[:andamento.find(' -')]
            despacho = f'{data_disponibilização} - {nome_documento} (despacho) # https://portal.stf.jus.br/processos/{link_documento}'
            lista_documentos.append(despacho)        
    return lista_documentos

def busca_recursos_internos(lista_de_andamentos):
    critérios_buscas = ['Interposto agravo regimental #',
                        'Opostos embargos de declaração #',
                        'Opostos embargos de divergência #',
                        'Opostos embargos infringentes #']
    lista_de_recursos = []
    for andamento in lista_de_andamentos:
        for item in critérios_buscas:
            critério = item
            if critério in andamento:
                recurso = andamento[:andamento.find(' #')]
                lista_de_recursos.append(recurso)
    return lista_de_recursos


def capturar_julgamentos_virtuais (lista_de_andamentos):

    lista_inicio_sessao = []
    lista_fim_ou_suspensao_sessao = []
    for andamento in lista_de_andamentos:
        inicio = re.compile(rf'(\d{{2}}/\d{{2}}/\d{{4}} - Iniciado Julgamento Virtual)', re.IGNORECASE)
        m = re.search(inicio, andamento)
        if m:
            lista_inicio_sessao.append(m.group())
        
        fim_ou_suspensao = re.compile(rf'(\d{{2}}/\d{{2}}/\d{{4}}.+(Suspenso o julgamento|Processo destacado no Julgamento Virtual #|Retirado do Julgamento Virtual|Finalizado Julgamento Virtual #))', re.IGNORECASE)
        m2 = re.search(fim_ou_suspensao, andamento)
        if m2:
            lista_fim_ou_suspensao_sessao.append(m2.group())

    if len(lista_inicio_sessao) > len(lista_fim_ou_suspensao_sessao):
        lista_fim_ou_suspensao_sessao.append('Em andamento')

    eventos = list(zip(lista_inicio_sessao,lista_fim_ou_suspensao_sessao))
    lista_eventos = []
    for evento in eventos:
        string_evento = f"{evento[0]} -|- {evento[1]}"
        lista_eventos.append(string_evento)
    return lista_eventos

def pedidos_de_destaque(lista_de_andamentos):
    
    lista_destaque = []
    lista_ministros = []
    nome_ministro = None
    
    for andamento in lista_de_andamentos:
        # Procura por pedido de destaque
        padrao_destaque = re.compile(r'\d{2}/\d{2}/\d{4} - (Retirado do Julgamento Virtual # Pedido de Destaque|Processo destacado no Julgamento Virtual)', re.IGNORECASE)
        
        if re.search(padrao_destaque, andamento):
            m_destaque = re.search(padrao_destaque, andamento)
            destaque = m_destaque.group()
            destaque = destaque.replace(" Retirado do Julgamento Virtual #","")
            lista_destaque.append(destaque)
            
            # Se encontrou destaque, procura o ministro NA MESMA LINHA
            padrao_ministro = re.compile(r'\*\s*(.*?)\s*\$', re.IGNORECASE)
            m_ministro = re.search(padrao_ministro, andamento)
            
            if m_ministro:
                # nome do Ministro
                nome_ministro = m_ministro.group(1)
                lista_ministros.append(nome_ministro)
            else:
                lista_ministros.append("")

    eventos = (list(zip(lista_destaque, lista_ministros)))

    return eventos if eventos else [("", "")]

def pedidos_de_vista (lista_de_andamentos):

    lista_vista = []
    lista_ministros = []
    nome_ministro = None
    
    for andamento in lista_de_andamentos:
        # Procura por "Vista ao(à) Ministro #"
        padrao_vista = re.compile(r'(\d{2}/\d{2}/\d{4} - Vista ao\(à\)) Ministro\(a\)', re.IGNORECASE)
        m_vista = re.search(padrao_vista, andamento)
        # Se encontrou ambos no mesmo andamento, adiciona à lista
        if m_vista:
            m_vista = re.search(padrao_vista, andamento)
            vista = m_vista.group(1)
            lista_vista.append(vista)

            # Procura pelo nome do ministro (MIN. + nome com 2 ou mais palavras)
            padrao_ministro = re.compile(r'\*\s*(.*?)\s*\$', re.IGNORECASE)
            # padrao_ministro = re.compile(r'pediu vista dos autos [oa] ((Min.*?)\s+([A-ZÁÀÂÃÄÅÇÉÈÊËÍÌÎÏÓÒÔÖÕÚÙÛÜ][A-Za-záàâãäåçéèêëíìîïóòôöõúùûü]+\s+[A-ZÁÀÂÃÄÅÇÉÈÊËÍÌÎÏÓÒÔÖÕÚÙÛÜ][A-Za-záàâãäåçéèêëíìîïóòôöõúùûü]+))')
            m_ministro = re.search(padrao_ministro, andamento)
            if m_ministro:
                nome_ministro = m_ministro.group(1)
                lista_ministros.append(nome_ministro)
            else:
                lista_ministros.append("")

    eventos = (list(zip(lista_vista, lista_ministros)))

    return eventos if eventos else [("", "")]

def reduzir_aquivos_temporarios (caminho_log_snapshots, quantidade):
    lista_arq_temp = []
    lista_apagar = []
    for nome_arquivo in os.listdir(caminho_log_snapshots):
        if os.path.isfile(os.path.join(caminho_log_snapshots, nome_arquivo)):
            caminho_arquivo = os.path.join(caminho_log_snapshots, nome_arquivo)
        try:
            lista_arq_temp.append(caminho_arquivo)
        except:
            pass
    lista_arq_temp.sort()
    if len(lista_arq_temp) > quantidade:
        lista_apagar = lista_arq_temp[:len(lista_arq_temp)-quantidade]
        for arquivo in lista_apagar:
            os.remove(arquivo)

def gravar_log_provisório(inicio,
                          iterações_executadas,
                          caminho_log_snapshots,
                          pesquisar_por,
                          processo,
                          lista_a_ser_consultada,
                          classe_processo,
                          classe_e_numero_dados_extraidos,
                          classe_e_numeros_inexistentes,
                          iteracoes_de_pausa_executadas,
                          string_pausas_duração,
                          barra,
                          traço,
                          percentual,
                          retomadas_apos_erro):
        #Grava arquivo de log:
        qtde_de_processos_a_serem_consultados = len(lista_a_ser_consultada)
        base_nome = f"log_provisorio - {datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")}.txt" # nome provisório do arquivo
        final = datetime.datetime.now() #data e hora da gravação
        duração = final - inicio # tempo de duração da execução
        # Formatar exibição de duração do tempo de execução do código
        total_segundos = duração.total_seconds()
        horas = (int(total_segundos//3600))
        minutos = int((total_segundos % 3600) //60)
        segundos = int(total_segundos % 60)
        string_duração = f'{horas}h:{minutos}m:{segundos}s'
        #Define a variável "tempo_medio_de_extracao"
        tempo_medio_de_extracao = 0
        if iterações_executadas != 0:
            tempo_medio_de_extracao = duração.total_seconds() / iterações_executadas
        # Grava arquivo temporário de log
        with open(rf'{caminho_log_snapshots}\{base_nome}', "w", encoding="utf-8") as log_file:
            log_file.write(f'SUCESSO na extração dos dados!!!\n\n')
            log_file.write(f'Nº consultas requisitadas: {qtde_de_processos_a_serem_consultados} processos.\n')
            log_file.write(f"Houve {retomadas_apos_erro:02d} retomadas de consulta após bloqueio pelo servidor do STF ou por queda de internet.\n")
            log_file.write(f"Nº consultas feitas: {len(classe_e_numero_dados_extraidos)+len(classe_e_numeros_inexistentes)} processos.\n\
            \rSe não foram consultados todos os processos e não há arquivo de log de erro ou de log de extração definitivos, verifique o último\
            \rlog temporário gravado na pasta snapshots.\n\n")
            if pesquisar_por == 'intervalo':
                if classe_processo == 'ARE' or classe_processo == 'RE':
                    log_file.write(f"Extração de dados de ARE's ou RE's, cujos números correspondem ao {pesquisar_por} do nº {lista_a_ser_consultada[0]} ao nº {processo}\n\n")
                else:
                    log_file.write(f"Extração de {classe_processo}'s, cujos números correspondem ao {pesquisar_por} do nº {lista_a_ser_consultada[0]} ao nº {processo}\n\n")
            else:
                    if classe_processo == 'ARE' or classe_processo == 'RE':
                        log_file.write(f"Extração de dados de LISTA predefinida de ARE's ou RE's, contendo {len(lista_a_ser_consultada)} nº's de processos.\n\n")
                    else:
                        log_file.write(f"Extração de dados de LISTA predefinida de {classe_processo}'s, contendo {len(lista_a_ser_consultada)} nº's de processos.\n\n")
            log_file.write(f'Qtde de processos cujos dados foram extraídos com sucesso: {len(classe_e_numero_dados_extraidos)}.\n\n')
            log_file.write(f"Qtde de números de processo inexistentes: {len(classe_e_numeros_inexistentes)}\n\n")
            log_file.write(f'Processos cujos dados foram extraídos COM SUCESSO:\n{'\n'.join(classe_e_numero_dados_extraidos)}\n\n')
            log_file.write(f'Processos inexistentes:\n{'\n'.join(classe_e_numeros_inexistentes)}\n\n')
            log_file.write(f"""{iterações_executadas} nº's de processo consultados.\nInicio: {inicio}\n   Fim: {final}\nDuração: {string_duração}.\n
            \rForam feitas {iteracoes_de_pausa_executadas} pausa(s), cuja soma dá {string_pausas_duração}.\n
            \rO tempo médio gasto por consulta foi de {tempo_medio_de_extracao} segundos (incluindo-se, no cálculo, a soma dos tempos das pausas).\n\n""")
            log_file.write('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + ' %\n\n')
            log_file.flush()
        return final
        
def pausar_e_retomar(classe_processo, processo_atual):
    """
    Função para pausar e retomar a execução após erro
    """
    tempo_pausa_minimo = 1800
    tempo_pausa = tempo_pausa_minimo + random.randint(900, 1800)

    print(f"\n{'='*80}")
    print(f"ERRO DETECTADO\nO servidor bloqueou temporariamente o IP ou a internet caiu.\n\nPAUSANDO A EXECUÇÃO do script POR {tempo_pausa} SEGUNDOS")
    print(f"PROCESSO ATUAL: {classe_processo} {processo_atual}")
    print(f"{'='*80}")
    
    # Pausa com contador visual
    for segundo in range(tempo_pausa, 0, -1):
        minutos = segundo // 60
        segundos_restantes = segundo % 60
        horas = minutos // 60
        minutos = minutos % 60
        
        if horas > 0:
            tempo_str = f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"
        else:
            tempo_str = f"{minutos:02d}:{segundos_restantes:02d}"
            
        print(f"\rRetomando em: {tempo_str}", end="", flush=True)
        sleep(1)
    print(f"Retomando a consulta a partir do processo {classe_processo} {processo_atual}")
    
    print(f"\n{'='*80}")
    print(f"RETOMANDO EXECUÇÃO a partir do processo {classe_processo} {processo_atual}")
    print(f"{'='*80}\n")
    return tempo_pausa

def gravar_log_de_erro (inicio,
                        iteracoes_executadas,
                        caminho_logs_definitivos,
                        pesquisar_por,
                        processo,
                        lista_a_ser_consultada,
                        classe_processo,
                        classe_e_numero_dados_extraidos,
                        classe_e_numeros_inexistentes,
                        iteracoes_de_pausa_executadas,
                        string_pausas_duração,
                        barra,
                        traço,
                        percentual,
                        n_erros_consecutivos,
                        erro_capturado,
                        base_nome_erro,
                        retomadas_apos_erro):
    import traceback
    import sys
    
    # Obter informações do erro atual
    exc_type, exc_value, exc_traceback = sys.exc_info()
    
    # Extrair linha e arquivo onde ocorreu o erro
    tb = traceback.extract_tb(exc_traceback)
    ultimo_frame = tb[-1]  # Último frame (onde realmente ocorreu o erro)
    
    arquivo = ultimo_frame.filename
    linha = ultimo_frame.lineno
    funcao = ultimo_frame.name
    codigo_linha = ultimo_frame.line
    
    # Mensagem personalizada
    erro_detalhado = f"Arquivo: {arquivo}\nLinha: {linha}\nFunção: {funcao}\nCódigo: {codigo_linha}\nErro: {erro_capturado}"
    
    # Exibir no terminal
    print(f'Erro inesperado: {erro_capturado}')
    print(f"Erro ocorreu na linha {linha} do arquivo {arquivo}")
    print(f"Função: {funcao}")
    print(f"Código da linha: {codigo_linha}")
    final = datetime.datetime.now() #data e hora da gravação
    duração = final - inicio # tempo de duração da execução
    # Formatar exibição de duração do tempo de execução do código
    total_segundos = duração.total_seconds()
    horas = (int(total_segundos//3600))
    minutos = int((total_segundos % 3600) //60)
    segundos = int(total_segundos % 60)
    string_duração = f'{horas}h:{minutos}m:{segundos}s'
    # Calcular o tempo médio de extração por processo
    tempo_medio_de_extracao = 0
    if iteracoes_executadas != 0: # Verificar se te número de consultas é diferente de zero
        tempo_medio_de_extracao = duração.total_seconds() / iteracoes_executadas  # Dividir o tempo total da execução do programa pela quantidade de consultas feitas
#Grava arquivo temporário de log
    with open(rf'{caminho_logs_definitivos}\{base_nome_erro}', "w", encoding="utf-8") as log_file:
        log_file.write(f"""ERRO NA EXTRAÇÃO DOS DADOS!!!\n
        \rOcorreram {n_erros_consecutivos} erros consecutivos.
        \rHouve {retomadas_apos_erro:02d} retomadas de consulta após bloqueio pelo servidor do STF ou por queda de internet.\n
        \rOBS.: Na quarta tentativa mal sucedida de extração, o laço de iteração é encerrado.
        \rSe o número de erros consecutivos for menor, a janela do navegador pode ter sido fechada acidentalmente pelo usuário.
        \rLaço de iteração encerrado prematuramente e dados gravados...
        \rConsulte o arquivo de log e verifique quais foram o erro ocorrido e a última extração bem sucedida.
        \rReconfigure o extrator para retomar a extração, observando o número do último processo cuja extração foi bem sucedida.\n\n""")
        log_file.write(f'Nº consultas requisitadas: {len(lista_a_ser_consultada)} processos.\n')
        log_file.write(f"Nº consultas feitas: {len(classe_e_numero_dados_extraidos)+len(classe_e_numeros_inexistentes)} processos.\n")
        if pesquisar_por == 'intervalo':                     
            if classe_processo == 'ARE' or classe_processo == 'RE':
                log_file.write(f"Extração de dados de ARE's ou RE's, cujos números correspondem ao {pesquisar_por} do nº {lista_a_ser_consultada[0]} ao nº {processo}\n\n")
                log_file.write(f'Último processo cuja extração foi bem sucedida: {classe_e_numero_dados_extraidos[len(classe_e_numero_dados_extraidos)-1] if len(classe_e_numero_dados_extraidos) > 0 else '__'}\n\n')
            else:
                log_file.write(f"Extração de {classe_processo}'s, cujos números correspondem ao {pesquisar_por} do nº {lista_a_ser_consultada[0]} ao nº {processo}\n\n")
                log_file.write(f'Último processo cuja extração foi bem sucedida: {classe_e_numero_dados_extraidos[len(classe_e_numero_dados_extraidos)-1] if len(classe_e_numero_dados_extraidos) > 0 else '__'}\n\n')
        else:
            if classe_processo == 'ARE' or classe_processo == 'RE':
                log_file.write(f"Extração de dados de LISTA predefinida de ARE's ou RE's, contendo {len(lista_a_ser_consultada)} nº's de processos.\n\n")
                log_file.write(f'Último processo cuja extração foi bem sucedida: {classe_e_numero_dados_extraidos[len(classe_e_numero_dados_extraidos)-1] if len(classe_e_numero_dados_extraidos) > 0 else '__'}\n\n')
            else:
                log_file.write(f"Extração de dados de LISTA predefinida de {classe_processo}'s, contendo {len(lista_a_ser_consultada)} nº's de processos.\n\n")
                log_file.write(f'Último processo cuja extração foi bem sucedida: {classe_e_numero_dados_extraidos[len(classe_e_numero_dados_extraidos)-1] if len(classe_e_numero_dados_extraidos) > 0 else '__'}\n\n')
        log_file.write(f'Qtde de processos cujos dados foram extraídos com sucesso: {len(classe_e_numero_dados_extraidos)}.\n\n')
        log_file.write(f"Qtde de números de processo inexistentes: {len(classe_e_numeros_inexistentes)}\n\n")
        log_file.write(f'Lidas dos processos cujos dados foram extraídos COM SUCESSO:\n{'\n'.join(classe_e_numero_dados_extraidos)}\n\n')
        log_file.write(f'Processos inexistentes:\n{'\n'.join(classe_e_numeros_inexistentes)}\n\n')
        log_file.write(f"""{iteracoes_executadas} processos consultados\nInicio: {inicio}\n   Fim: {final}\nDuração: {string_duração}.\n
        \rForam feitas {iteracoes_de_pausa_executadas} pausa(s), cuja soma dá {string_pausas_duração}.\n
        \rO tempo médio gasto por consulta foi de {tempo_medio_de_extracao} segundos (incluindo-se, no cálculo, a soma dos tempos das pausas).\n\n""")
        log_file.write('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + '%\n\n') # Barra de progresso
        log_file.write(f'Mensagem de erro do sistema:\n {str(erro_capturado) if erro_capturado else "Erro desconhecido"}\n')
        log_file.write(f"Erro ocorreu na linha {linha} do arquivo {arquivo}\n\n")
        log_file.write(f"Função: {funcao}\n\n")
        log_file.write(f"Código da linha: {codigo_linha}\n\n")
        log_file.flush()
        # Exibe no terminal a mensagem de que houve erro na extração e o loop será encerrado e os dados gravadosstring_pausas_duração
        print(f"""{("* " * 50)}\nERRO NA EXTRAÇÃO DOS DADOS!!!\n
        Laço de iteração encerrado prematuramente e dados gravados...\n\n\
        Consulte o arquivo de log e verifique qual foi a última extração bem sucedida.\n\
        Reconfigure o extrator para retomar a extração, observando o número do último processo cuja extração foi bem sucedida.\n{("* " * 60)}""")

def pausas_regulares (limite_para_pausa, inicio, iteracoes_executadas, iteracoes_de_pausa_executadas, tempo_total_de_pausa):
        # Algoritmo para implementar uma pausa na extração a depois de determinado de iterações do laço de iteração
        if iteracoes_executadas >= 1:
            tempo_de_pausa = 0
            if iteracoes_executadas > 0 and iteracoes_executadas % 50 == 0: # Ao final de cada ciclo de 50 pausas
                tempo_de_pausa = random.randint(150, 240) # Estabelece o tempo de pausa entre dois e meio e quatro minutos
                print(f'\n\tPausa de {tempo_de_pausa} segundos, para evitar que o servidor do STF deixe de atender às requisições.\n')
                print(f'\tAguardar o transcurso do tempo programado até a próxima consulta.\n')
            elif iteracoes_executadas >= limite_para_pausa:
                tempo_de_pausa = random.randint(20, 59) # Estabelece o tempo de pausa entre 20 e 59 segundos
                print(f'\n\tPausa de {tempo_de_pausa} segundos, para evitar que o servidor do STF deixe de atender às requisições.\n')
                print(f'\tAguardar o transcurso do tempo programado até a próxima consulta.\n')
            tempo_total_de_pausa += tempo_de_pausa
            horas_pausa = (int(tempo_total_de_pausa//3600)) # Calcula a quantidade de horas inteiras de execução
            minutos_pausa = int((tempo_total_de_pausa % 3600) //60) # Calcula os minutos inteiros, a partir da fração de hora desprezada na primeira conta
            segundos_pausa = int(tempo_total_de_pausa % 60) # Calcula os segundos, a partir da fração desprezada de minutos da segunda conta
            string_pausas_duração = f"{horas_pausa:02d}h:{minutos_pausa:02d}m:{segundos_pausa:02d}s"  #Cria um texto com o formado "0h:0m:0s" para exibir o tempo de execução do programa
            while tempo_de_pausa > 0:
                minutos = tempo_de_pausa //60
                segundos = tempo_de_pausa % 60
                print(f"\t\t\t{minutos:02d}:{segundos:02d}", end="\r", flush=True)
                tempo_de_pausa -= 1
                sleep(1)
                if tempo_de_pausa == 0:
                    qtde_de_consultas_antes_de_pausar = random.randint(10, 30)
                    print(f'\n\n\tPausa encerrada.\n\tRetomando o processo de extração de dados...')
                    print(f'\n\tAté o momento, foram feitas {iteracoes_de_pausa_executadas} pausas, cuja soma dá {string_pausas_duração}\n')
                    final = datetime.datetime.now() #data e hora
                    duração = final - inicio # Calcula a duração da execução, subtraindo o marco inicial do marco final
                    total_segundos = duração.total_seconds() # Converte a duração (incialmente calculada em horas, minutos e segundos) para segundos apenas
                    tempo_medio_de_extracao = duração.total_seconds() / iteracoes_executadas  # Dividir o tempo total da execução do programa pela quantidade de consultas feitas
                    print(f'\n\tTempo médio de extração de cada processo: {tempo_medio_de_extracao} segundos (incluindo a soma dos tempos das pausas).\n')
                    limite_para_pausa = iteracoes_executadas + qtde_de_consultas_antes_de_pausar
                    print("-" * 100)  # Separador visual
        return 1

def eventos_presidência_e_relator (lista_de_andamentos):
  
    eventos_relevantes = ['Admitidos embargos de divergência',
                            'Adotado rito do Art. 12, da Lei 9.868/99',
                            'Agravo de instrumento provido',
                            'Agravo não provido',
                            'Agravo provido e desde logo negado seguimento ao RE',
                            'Agravo provido e desde logo provido o RE',
                            'Agravo provido e desde logo provido parcialmente o RE',
                            'Agravo provido e determinada a devolução pelo regime da repercussão geral',
                            'Agravo provido e julgado mérito de tema com repercussão geral',
                            'Agravo provido e RE pendente de julgamento',
                            'Agravo regimental não conhecido',
                            'Agravo regimental não provido',
                            'Agravo regimental provido',
                            'Agravo regimental provido em parte',
                            'Cancelamento da distribuição',
                            'Concedida a ordem',
                            'Concedida a ordem de ofício',
                            'Concedida a segurança',
                            'Concedida a suspensão',
                            'Concedida em parte a ordem',
                            'Concedida em parte a segurança',
                            'Concedida em parte a suspensão',
                            'Conhecida e julgada sem pronúncia de inconstitucionalidade',
                            'Decisão (Lei 9.868/99) publicada no DJE e no DOU',
                            'Decisão (segredo de justiça)',
                            'Decisão (sigiloso)',
                            'Decisão de julgamento (Lei 9.868/99) publicada no DJE',
                            'Decisão de julgamento (Lei 9.868/99) publicada no DJE e no DOU',
                            'Decisão de julgamento (Lei 9.868/99) publicada no DOU',
                            'Decisão de julgamento (Lei 9.882/99) publicada no DJE',
                            'Decisão de julgamento (Lei 9.882/99) publicada no DJE e no DOU',
                            'Decisão de julgamento (Lei 9.882/99) publicada no DOU',
                            'Decisão pela existência de repercussão geral',
                            'Decisão pela inexistência de repercussão geral',
                            'Decisão pela inexistência de repercussão geral por se tratar de matéria infraconstitucional',
                            'Decisão Ratificada',
                            'Decisão Referendada',
                            'Declarada a extinção da punibilidade',
                            'Declarada a Inconstitucionalidade Incidental de Ato Normativo',
                            'Declinada a competência',
                            'Deferido',
                            'Denegada a ordem',
                            'Denegada a segurança',
                            'Denegada a suspensão',
                            'Determinada a devolução',
                            'Determinada a devolução pelo regime da repercussão geral',
                            'Determinada a remessa ao STJ para julgamento como REsp (art. 1.033 do CPC)',
                            'Determinada a remessa ao STJ para prévio julgamento do REsp (art. 1.031 do CPC)',
                            'Determino a baixa dos autos - remessa indevida',
                            'Determino a distribuição',
                            'Distribuído',
                            'Embargos não conhecidos',
                            'Embargos recebidos',
                            'Embargos recebidos como agravo regimental desde logo não conhecido',
                            'Embargos recebidos como agravo regimental desde logo não provido',
                            'Embargos recebidos como agravo regimental desde logo provido',
                            'Embargos recebidos como agravo regimental desde logo provido em parte',
                            'Embargos recebidos em parte',
                            'Embargos rejeitados',
                            'Fixada a Tese',
                            'Homologação de acordo de não persecução penal - art.28-A do CPP',
                            'Homologação de transação penal',
                            'Homologada a desistência',
                            'Homologado acordo de não persecução penal',
                            'Homologado o acordo',
                            'Improcedente',
                            'Inadmitidos os embargos de divergência',
                            'Interposto agravo regimental',
                            'Julgado mérito de tema com repercussão geral',
                            'Julgado mérito de tema com repercussão geral sem fixação de tese',
                            'Mérito da repercussão geral julgado no processo nº',
                            'Não conhecido(s)',
                            'Não provido',
                            'Negado seguimento',
                            'Negado seguimento por ausência de preliminar, art. 327 do RISTF',
                            'Opostos embargos à execução',
                            'Opostos embargos de declaração',
                            'Opostos embargos de divergência',
                            'Opostos embargos infringentes',
                            'Prejudicado',
                            'Procedente',
                            'Procedente em parte',
                            'Provido',
                            'Provido em parte',
                            'Reafirmação de Jurisprudência no Plenário Presencial',
                            'Reconhecida a repercussão geral e julgado o mérito com reafirmação de jurisprudência no PV',
                            'Reconsideração',
                            'Reconsidero e determino a distribuição',
                            'Reconsidero e devolvo pelo regime da repercussão geral',
                            'Reconsidero e julgo prejudicado o recurso interno',
                            'Registrado à Presidência',
                            'Rejeitado',
                            'Substitui o paradigma de repercussão geral - processo nº']

    lista_eventos_relevantes = []
    lista_registro_presidência = []
    lista_registro_distribuição = []
    eventos_sob_a_direcao_da_presidencia = []
    eventos_sob_a_direcao_do_relator = []
    for andamento in lista_de_andamentos:
        for evento in eventos_relevantes:
            if evento in andamento:
                elemento_encontrado = andamento
                # índice_final = elemento_encontrado.find(' #')
                # elemento_encontrado = elemento_encontrado[0:índice_final]
                if elemento_encontrado[0:elemento_encontrado.find(' #')] not in '\n'.join(lista_eventos_relevantes):
                    lista_eventos_relevantes.append(elemento_encontrado)

    for item in lista_eventos_relevantes:
        if 'Registrado à Presidência' in item:
            lista_registro_presidência.append(item)
    try:
        marcador1 = lista_eventos_relevantes.index(lista_registro_presidência[0])
    except:
        marcador1 = -1

    for item in lista_eventos_relevantes:
        if 'Distribuído' in item:
            lista_registro_distribuição.append(item)
    try:
        marcador2 = lista_eventos_relevantes.index(lista_registro_distribuição[0])
    except:
        marcador2 = -1

    if marcador1 != -1 and marcador2 != -1:
        eventos_sob_a_direcao_da_presidencia = lista_eventos_relevantes[marcador1+1:marcador2]
        if len(eventos_sob_a_direcao_da_presidencia) == 0:
            eventos_sob_a_direcao_da_presidencia = ['Sem ato praticado pela presidência']
        eventos_sob_a_direcao_do_relator = lista_eventos_relevantes[marcador2+1:]
    elif marcador1 != -1 and marcador2 == -1:
        eventos_sob_a_direcao_da_presidencia = lista_eventos_relevantes[marcador1+1:]
        eventos_sob_a_direcao_do_relator = ['Não distribuído']
    elif marcador1 ==-1 and marcador2 != -1:
        eventos_sob_a_direcao_da_presidencia = ['Não registrado à Presidência']
        eventos_sob_a_direcao_do_relator = lista_eventos_relevantes[marcador2+1:]
    else:
        eventos_sob_a_direcao_do_relator = ['Não distribuído']
        eventos_sob_a_direcao_da_presidencia = ['Não registrado à Presidência']
    
    if len(eventos_sob_a_direcao_da_presidencia) == 0:
        eventos_sob_a_direcao_da_presidencia.append("Sem decisão")
    if len(eventos_sob_a_direcao_do_relator) == 0:
        eventos_sob_a_direcao_do_relator.append("Sem decisão")


    return eventos_sob_a_direcao_da_presidencia, eventos_sob_a_direcao_do_relator, lista_eventos_relevantes



def analise_decisoes_presidencia (lista_de_andamentos):
    indicadores_reforma = ['Agravo regimental provido #',
                       'Agravo regimental provido em parte #',
                       'Determinada a devolução pelo regime da repercussão geral #',
                       'Embargos recebidos #',
                       'Embargos recebidos em parte #',
                       'Embargos recebidos como agravo regimental desde logo provido #',
                       'Embargos recebidos como agravo regimental desde logo provido em parte #',
                       'Prejudicado #',
                       'Procedente #',
                       'Procedente em parte #',
                       'Provido #',
                       'Provido em parte #',
                       'Reconsidero e determino a distribuição #',
                       'Reconsidero e devolvo pelo regime da repercussão geral #',
                       'Reconsideração #',
                       ]
    eventos_sob_a_direcao_da_presidencia = eventos_presidência_e_relator(lista_de_andamentos)[0]
    eventos_apos_primeira_decisao_presidencia = eventos_sob_a_direcao_da_presidencia[1:]
    reforma_rec_int_pres = []
    reforma_pres = []
    detalhamento = []
    orgao = []
    for evento in eventos_apos_primeira_decisao_presidencia:
        for indicador in indicadores_reforma:
            padrao = re.compile(rf'(?!.*\badmit.*embargos de diverg[êe]ncia).*(\d{{2}}/\d{{2}}/\d{{4}} - {re.escape(indicador)}.*(?=\s\$))', re.IGNORECASE)
            m = re.search(padrao, evento)
            if m:
                reforma_rec_int_pres.append(m.group())
                reforma_pres.append(m.group())
    if len(reforma_rec_int_pres) > 0:
        reforma_pres = "Sim"
        for item in reforma_rec_int_pres:
            detalhamento.append(item[:item.find(" *")].strip())
            orgao.append(item[item.find("* ")+2:].strip())
    else:
        reforma_pres = "Não"

    return reforma_pres, detalhamento, orgao


def analise_decisoes_relator (lista_de_andamentos):
    indicadores_reforma = ['Agravo regimental provido #',
                       'Agravo regimental provido em parte #',
                       'Embargos recebidos #',
                       'Embargos recebidos em parte #',
                       'Embargos recebidos como agravo regimental desde logo provido #',
                       'Embargos recebidos como agravo regimental desde logo provido em parte #',
                       'Prejudicado #',
                       'Procedente #',
                       'Procedente em parte #',
                       'Provido #',
                       'Provido em parte #',
                       'Reconsidero e determino a distribuição #',
                       'Reconsidero e devolvo pelo regime da repercussão geral #',
                       'Reconsideração #',
                       ]

    eventos_sob_direcao_do_relator = eventos_presidência_e_relator(lista_de_andamentos)[1]
    eventos_apos_primeira_decisao_relator = eventos_sob_direcao_do_relator[1:]
    reforma_rec_int_rel = []
    reforma_rel = []
    detalhamento = []
    orgao = []
    for evento in eventos_apos_primeira_decisao_relator:
        for indicador in indicadores_reforma:
            padrao = re.compile(rf'(?!.*\badmit.*embargos de diverg[êe]ncia).*(\d{{2}}/\d{{2}}/\d{{4}} - {re.escape(indicador)}.*(?=\s\$))', re.IGNORECASE)
            m = re.search(padrao, evento)
            if m:
                reforma_rec_int_rel.append(m.group())
                reforma_rel.append(m.group())
    if len(reforma_rec_int_rel) > 0:
        reforma_rel = "Sim"
        for item in reforma_rec_int_rel:
            detalhamento.append(item[:item.find(" *")].strip())
            orgao.append(item[item.find("* ")+2:].strip())
    else:
        reforma_rel = "Não"
    
    return reforma_rel, detalhamento, orgao

def converter_datas_para_string(dados):
    for chave in ['inicio_tramitacao', 'fim_tramitacao']:
        dados[chave] = [
            data.strftime('%d/%m/%Y') if isinstance(data, datetime.date) else data
            for data in dados[chave]
        ]
    return dados



if __name__ == "__main__":


    import random

    # lista1 = [1, 2, 3]
    # lista1 = [str(item) for item in lista1]
    # lista2 = ['eloi', 'ricardo', 'reffatti']
    # lista3 = list(zip(lista1, lista2))
    # resultado = list(lista3[0])
    # print(lista3)
    # print(' - resultado: '.join(resultado))

    texto = 'PRESIDÊNCIA'