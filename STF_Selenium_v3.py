"""Ver a possibilidade fazer nova extração, incluindo o xpath relativo à repercussão geral\
    vide RE 1355228"""

#Importar dicionários e funções
import ModuloSTFSelenium
#Importar navegador
from selenium import webdriver
#Importar ferramenta para tratamento de exceções
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from urllib3.exceptions import ReadTimeoutError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#Importar ferramenta sleep
from time import sleep
import datetime
import random
import os
import json
import traceback
import sys
import urllib3



def executar_extracao_STF (classe_pesquisada,
                            pesquisar_por,
                            núm_inicial,
                            núm_final,
                            lista_de_processos,
                            caminho_gravação_de_dados,
                            caminho_logs_definitivos,
                            caminho_log_snapshots,
                            pausa_no_meio_do_laço_de_repetição,
                            callback_progresso=None):
    
    """Função para executar a extração de dados do STF, conforme os parâmetros definidos pelo usuário."""

    caminho_log_snapshots = rf'{caminho_logs_definitivos}\snapshots' # Define a variável com o nome do diretório onde serão armazenados os logs_provisórios
    os.makedirs(rf'{caminho_log_snapshots}', exist_ok=True) #Cria a pasta onde serão armazenados os logs_provisórios

    """RECOMENDA-SE O USO DA PAUSA a seguir durante a consulta de MUITOS PROCESSOS."""

    pausa_no_meio_do_laço_de_repetição = 'não' # "Digite "sim" ou "não" para executar uma pausa por tempo aleatório entre 2 e 8 segundos no início de cada laço de repetição.
    # Recomendada em caso de suscessivos erros na extração.

    #Definir lista a ser consultada
    classe_e_numeros_inexistentes = [] # Variável para armazenar a lista contendo a classe e o número dos processos inexisntes.
    classe_e_numero_dados_extraidos = [] # Variável para armazenar a lista contendo a classe e o número dos processos cuja extração foi bem sucedida.
    lista_provisória_are = [] # Variável auxiliar apenas números (sem a classe) dos processos inexistentes.
    if pesquisar_por.lower() == 'lista':
        # Se a opção for "lista", a variável lista_a_ser_consultada recebe o valor da variável lista_de_processos
        lista_a_ser_consultada = lista_de_processos
    else:
        # Senão, a variável lista_a_ser_consultada recebe o valor da variável lista criada a partir do intervalo criado a partir dos valores das
        # variáveis núm_inicial e núm_final
        lista_a_ser_consultada = list(range(núm_inicial,núm_final+1))
    #Criar uma lista para armazenar os dados capturados
    lista_dados_capturados = []
    #Definir navegador a ser usado
    navegador = webdriver.Chrome()
    #Definir endereço a ser acessado pelo navegador
    url = 'https://portal.stf.jus.br/'
    #Abrir navegador e acessar o endereço indicado
    navegador.get(url)
    #Maximizar janela do navegador
    navegador.maximize_window()
    #Criar uma variável iteracoes_executadas para armazenar o número de consultas
    iteracoes_executadas = 0
    #Cria um limte para a pausa
    limite_para_pausa = iteracoes_executadas + random.randint(10, 30)
    #Cria uma variável para contar as pausas executadas
    iteracoes_de_pausa_executadas = 0
    # Criar uma variável para armazenar o tempo total das pausas feitas durante a execução do código
    tempo_total_de_pausa = 0
    # Criar uma variável para armazenar o tempo das pausas em formato hh:mm:ss
    string_pausas_duração = '00h:00m:00'
    #Cria variável para armazenar o número de retomadas após erro
    retomadas_apos_erro = 0
    # Criar uma variável para armazenar o valor referente à data e à hora em que o código começou a ser executado
    inicio = datetime.datetime.now()
    base_nome_erro = None #Variável para armazenar o nome do arquivo de log de erro, para fins de comparação antes de gerar o log final.
    base_nome_interrucao_usuario = None
    data_e_hora_fim = None
    #Variável para armazenar o número de erros consecutivos
    n_erros_consecutivos = 0
    #Cria uma variável para armazenar a quantidad ede erros ocorridos durante a execução do laço for
    erros_ocorridos = 0
    #Criar arquivo "Numeros inexistentes" para registro dos números inexistentes no mesmo diretório dos arquivos de log
    # LIMPA O DIRETÓRIO onde serão armazenados os snaps de log
    for nome_arquivo in os.listdir(caminho_log_snapshots):
        caminho_arquivo = os.path.join(caminho_log_snapshots, nome_arquivo)
        if os.path.isfile(caminho_arquivo):  # Garante que é um arquivo, não pasta
            os.remove(caminho_arquivo)
    #Criar laço de repetição dentro do qual serão buscadas as informações para cada processo da lista
    while iteracoes_executadas < len(lista_a_ser_consultada):
        processo = lista_a_ser_consultada[iteracoes_executadas]
        classe_processo = classe_pesquisada
        tamanho_anterior = len(classe_e_numeros_inexistentes)
        tamanho_atual = tamanho_anterior
        processo_consultado = f'{classe_processo} {processo}'
        # ELEMENTOS para implementação da barra de progresso
        progresso = (lista_a_ser_consultada.index(processo) + 1) / len(lista_a_ser_consultada) * 100
        percentual = int(progresso * 100) / 100
        if callback_progresso is not None:
            callback_progresso(percentual)
        barra = int(progresso)
        traço = 100 - barra
        # Implementa pausas regulares no laço de repetição
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
                    iteracoes_de_pausa_executadas += 1
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
            
            # Fechar e abrir o navegador a cada 750 consultas, para renovar a sessão do navegador e reduzir a chances de erros
            if iteracoes_executadas > 0 and iteracoes_executadas % 750 == 0:
                print(f"{("=" * 100)}\nReiniciando navegador, para limpar a sessão e reduzir chances de erro")
                # Fechar navegador
                navegador.quit()
                #Espera 15 segundos
                sleep(15)
                #Definir navegador a ser usado
                navegador = webdriver.Chrome()
                #Definir endereço a ser acessado pelo navegador
                url = 'https://portal.stf.jus.br/'
                #Abrir navegador e acessar o endereço indicado
                navegador.get(url)
                #Maximizar janela do navegador
                navegador.maximize_window()
                print(f"Navegador reiniciado. Continuando...\n{("=" * 100)}")

        # DENTRO DO LACÇO DE REPETIÇÃO
        # MANTÉM APENAS os 30 útlimos snapshots de log (para evitar ter muitos arquivos na pasta)
        ModuloSTFSelenium.reduzir_aquivos_temporarios (caminho_log_snapshots,15)
        try: # Bloco para retomar a consulta caso a conexão caia ou o servidor bloqueie temporariamente o IP
            try:
            #Chamar a função "pesquisar_por_classe_e_número" do ModuloSTFSelenium
                ModuloSTFSelenium.pesquisar_por_classe_e_número(navegador, classe_processo, processo)
                try:
                    #Pegar o código do incidente, chamando a função "encontrar_elemento" do ModuloSTFSelenium
                    sleep(2)
                    código_do_incidente = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Código_incidente']).get_attribute('value')
                except (TimeoutException, NoSuchElementException):
                    #Verificar se o site exibe a informação de que o processo não foi encontrado
                    número_inexistente = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Número_inexistente'])
                    #Verifica se a classe processual consultada é "ARE" ou "RE" e se for:
                    if classe_processo in ['ARE', 'RE']:
                        #Exibe na tela do terminal uma mensagem de que inexiste "ARE" ou "RE" com o número consultado
                        print(f'{("-" * 100)}\nEXECUÇÃO do programa EM ANDAMENTO.\nNÃO FECHAR a janela do TERMINAL.\nCom o terminal maximizado, pressione Ctrl+C para interromper de forma segura.\n')  # Separador visual
                        print('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + ' %\n\n') # Barra de progresso
                        print(f'Inexiste {classe_processo} nº {processo}...')                            
                        print(f'{iteracoes_executadas + 1} nºs de processo consultados.\n')
                        lista_provisória_are.append(processo) # Acrescenta o apenas o número do processo consultado na variávle auxiliar do tipo lista.
                        if lista_provisória_are.count(processo) == 2: # Verifica se o número do processo aparece duas vezes na variável auxiliar do tipo lista.
                            classe_e_numeros_inexistentes.append(f'ARE ou RE {processo}') # Se sim, acrescenta a "ARE ou RE" e o número do processo na variável "classe_e_numero_inexistentes"
                            lista_provisória_are =[] # Esvazia a lista auxiliar, em ordem a poupar processamento na próxima contagem
                        # Verifica o tamanho atual da lista de "classe_e_numeros_inexistentes"
                        tamanho_atual = len(classe_e_numeros_inexistentes)
                    #Grava arquivo de log provisório
                        ModuloSTFSelenium.gravar_log_provisório(inicio,
                                                                iteracoes_executadas,
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
                                                                retomadas_apos_erro)
                        #Zera o contador de erros consecutivos
                        n_erros_consecutivos = 0
                        print(f'Gravação de log provisório.\n{("-" * 100)}\n')  # Mensagem com separador visual
                    #Senão
                    else:
                        #Exibe na tela a mensagem de que inexiste o processo com a classe e o número consultados
                        print(f'{("-" * 100)}\nEXECUÇÃO do programa EM ANDAMENTO.\nNÃO FECHAR a janela do TERMINAL.\nCom o terminal maximizado, pressione Ctrl+C para interromper de forma segura.\n')  # Separador visual
                        print('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + ' %\n\n') # Barra de progresso
                        print(f'Inexiste {processo_consultado}...')
                        iteracoes_executadas += 1 # Incrementa em 1 o valor da variável "iteracoes_executadas"
                        print(f'{iteracoes_executadas + 1} nºs de processo consultados.\n')
                        #Acrescenta à lista de processos inexistentes a classe e o número do processo
                        classe_e_numeros_inexistentes.append(processo_consultado)
                        #Remover números inexistentes duplicados da lista, sem alterar a ordem dos itens da lista.
                        classe_e_numeros_inexistentes = list(dict.fromkeys(classe_e_numeros_inexistentes))
                        # Verifica o tamanho atual da lista de "classe_e_numeros_inexistentes"
                        tamanho_atual = len(classe_e_numeros_inexistentes)
                        #Grava arquivo de log provisório
                        ModuloSTFSelenium.gravar_log_provisório(inicio,
                                                                iteracoes_executadas,
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
                                                                retomadas_apos_erro)
                        print(f'Gravação de log provisório.\n{("-" * 100)}\n')  # Mensagem com separador visual
                        continue # Deixa de executar o restante do código do laço de iteração, reiniciando a iteração a partir do próximo número de processo.
                #Pegar o modo de tramitação
                try:                
                    modo_tramitação = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo eletrônico']).text
                except (TimeoutException, NoSuchElementException):
                    modo_tramitação = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo físico']).text
                #Pegar dados sobre a publicidade
                try:
                    publicidade = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo_público']).text
                except (TimeoutException, NoSuchElementException):
                    publicidade = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Segredo_de_justiça']).text
                try:
                    #CAPTURAR PRIORIDADES NA TRAMITAÇÃO
                    #Encontrar elementos
                    indicadores_prioridades = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Tipo_de_Prioridade'])
                    #Pegar textos dos elementos
                    lista_de_prioridades = ModuloSTFSelenium.extrair_texto_de_vários_elementos(indicadores_prioridades)
                except (TimeoutException, NoSuchElementException):
                    lista_de_prioridades = []
                # Verificar se é tema de repercussão geral, caso a classe seja ARE ou RE
                if classe_processo in ['ARE', 'RE']:
                    try:
                        paradigma_rep_geral = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Repercussao_geral']).text
                    except:
                        paradigma_rep_geral = 'Não é paradigma'

            except (TimeoutException, NoSuchElementException):
                #Verificar se classe é "ARE"
                if classe_processo == 'ARE':
                    #Se for ARE, mudar a classe para "RE"
                    classe_processo = 'RE'
                    #Chamar a função "pesquisar_por_classe_e_número" do ModuloSTFSelenium
                    ModuloSTFSelenium.pesquisar_por_classe_e_número(navegador, classe_processo, processo)
                    try:
                        sleep(2)
                        #Pegar o código do incidente, chamando a função "encontrar_elemento" do ModuloSTFSelenium
                        código_do_incidente = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Código_incidente']).get_attribute('value')
                    except (TimeoutException, NoSuchElementException):
                        #Verificar se o site exibe a informação de que o processo não foi encontrado
                        número_inexistente = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Número_inexistente'])
                        #Verifica se a classe processual consultada é "ARE" ou "RE" e se for:
                        if classe_processo in ['ARE', 'RE']:
                            #Exibe na tela do terminal uma mensagem de que inexiste "ARE" ou "RE" com o número consultado
                            print(f'{("-" * 100)}\nEXECUÇÃO do programa EM ANDAMENTO.\nNÃO FECHAR a janela do TERMINAL.\nCom o terminal maximizado, pressione Ctrl+C para interromper de forma segura.\n')
                            print('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + ' %\n\n') # Barra de progresso
                            print(f'Inexiste {classe_processo} nº {processo}...')                                
                            print(f'{iteracoes_executadas + 1} nºs de processo consultados.\n')
                            iteracoes_executadas += 1 # Incrementa em 1 o valor da variável "iteracoes_executadas"
                            lista_provisória_are.append(processo) # Acrescenta o apenas o número do processo consultado na variávle auxiliar do tipo lista.
                            if lista_provisória_are.count(processo) == 2: # Verifica se o número do processo aparece duas vezes na variável auxiliar do tipo lista.
                                classe_e_numeros_inexistentes.append(f'ARE ou RE {processo}') # Se sim, acrescenta a "ARE ou RE" e o número do processo na variável "classe_e_numero_inexistentes"
                                lista_provisória_are =[] # Esvazia a lista auxiliar, em ordem a poupar processamento na próxima contagem
                            tamanho_atual = len(classe_e_numeros_inexistentes)
                            #Grava arquivo de log provisório
                            ModuloSTFSelenium.gravar_log_provisório(inicio,
                                                                iteracoes_executadas,
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
                                                                retomadas_apos_erro)
                            #Zera o contador de erros consecutivos
                            n_erros_consecutivos = 0
                            print(f'Gravação de log provisório.\n{("-" * 100)}\n')  # Mensagem com separador visual
                            continue # Deixa de executar o restante do código do laço de iteração, reiniciando a iteração a partir do próximo número de processo.
                    #Pegar o modo de tramitação
                    try:                
                        modo_tramitação = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo eletrônico']).text
                    except (TimeoutException, NoSuchElementException):
                        modo_tramitação = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo físico']).text
                    #Pegar dados sobre a publicidade
                    try:
                        publicidade = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo_público']).text
                    except (TimeoutException, NoSuchElementException):
                        publicidade = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Segredo_de_justiça']).text
                    try:
                        #CAPTURAR PRIORIDADES NA TRAMITAÇÃO
                        #Encontrar elementos
                        indicadores_prioridades = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Tipo_de_Prioridade'])
                        #Pegar textos dos elementos
                        lista_de_prioridades = ModuloSTFSelenium.extrair_texto_de_vários_elementos(indicadores_prioridades)
                    except (TimeoutException, NoSuchElementException):
                        lista_de_prioridades = []
                    # Verificar se é tema de repercussão geral
                    try:
                        paradigma_rep_geral = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Repercussao_geral']).text
                    except:
                        paradigma_rep_geral = 'Não'
                elif classe_processo == 'RE':
                    #Mudar classe para "ARE"
                    classe_processo = 'ARE'
                    #Chamar a função "pesquisar_por_classe_e_número" do ModuloSTFSelenium
                    ModuloSTFSelenium.pesquisar_por_classe_e_número(navegador, classe_processo, processo)
                    try:
                        sleep(2)
                        #Pegar o código do incidente, chamando a função "encontrar_elemento" do ModuloSTFSelenium
                        código_do_incidente = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Código_incidente']).get_attribute('value')
                    except (TimeoutException, NoSuchElementException):
                        #Verificar se o site exibe a informação de que o processo não foi encontrado
                        número_inexistente = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Número_inexistente'])
                        #Verifica se a classe processual consultada é "ARE" ou "RE" e se for:
                        if classe_processo in ['ARE', 'RE']:
                            #Exibe na tela do terminal uma mensagem de que inexiste "ARE" ou "RE" com o número consultado
                            print(f'{("-" * 100)}\nEXECUÇÃO do programa EM ANDAMENTO.\nNÃO FECHAR a janela do TERMINAL.\nCom o terminal maximizado, pressione Ctrl+C para interromper de forma segura.\n')  # Separador visual
                            print('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + ' %\n\n') # Barra de progresso
                            print(f'Inexiste {classe_processo} nº {processo}...')
                            print(f'{iteracoes_executadas + 1} nºs de processo consultados.\n')
                            iteracoes_executadas += 1 # Incrementa em 1 o valor da variável "iteracoes_executadas"                                
                            lista_provisória_are.append(processo) # Acrescenta o apenas o número do processo consultado na variávle auxiliar do tipo lista.
                            if lista_provisória_are.count(processo) == 2: # Verifica se o número do processo aparece duas vezes na variável auxiliar do tipo lista.
                                classe_e_numeros_inexistentes.append(f'ARE ou RE {processo}') # Se sim, acrescenta a "ARE ou RE" e o número do processo na variável "classe_e_numero_inexistentes"
                                lista_provisória_are =[] # Esvazia a lista auxiliar, em ordem a poupar processamento na próxima contagem
                            tamanho_atual = len(classe_e_numeros_inexistentes)
                        #Grava arquivo de log provisório
                            ModuloSTFSelenium.gravar_log_provisório(inicio,
                                                                iteracoes_executadas,
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
                                                                retomadas_apos_erro)
                            #Zera o contador de erros consecutivos
                            n_erros_consecutivos = 0
                            print(f'Gravação de log provisório.\n{("-" * 100)}\n')  # Mensagem com separador visual
                            continue # Deixa de executar o restante do código do laço de iteração, reiniciando a iteração a partir do próximo número de processo.
                    #Pegar o modo de tramitação
                    try:                
                        modo_tramitação = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo eletrônico']).text
                    except (TimeoutException, NoSuchElementException):
                        modo_tramitação = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo físico']).text
                    #Pegar dados sobre a publicidade
                    try:
                        publicidade = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Processo_público']).text
                    except (TimeoutException, NoSuchElementException):
                        publicidade = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Segredo_de_justiça']).text
                    try:
                        #CAPTURAR PRIORIDADES NA TRAMITAÇÃO
                        #Encontrar elementos
                        indicadores_prioridades = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Tipo_de_Prioridade'])
                        #Pegar textos dos elementos
                        lista_de_prioridades = ModuloSTFSelenium.extrair_texto_de_vários_elementos(indicadores_prioridades)
                    except (TimeoutException, NoSuchElementException):
                        lista_de_prioridades = []
                    # Verificar se é tema de repercussão geral
                    try:
                        paradigma_rep_geral = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Repercussao_geral']).text
                    except:
                        paradigma_rep_geral = 'Não'
            try:
                #Pegar os dados do número único do processo
                número_único = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Número_único']).text
                #Extrai apenas o número
                número_único = número_único[número_único.find(': ')+2:]
            except (TimeoutException, NoSuchElementException):
                número_único = 'Não há'
            try:
                órgão_de_origem = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Órgão_de_origem']).text
            except (TimeoutException, NoSuchElementException):
                órgão_de_origem = 'A competência é originária ou não há órgão de origem'
            uf_de_origem = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['UF_origem']).text
            # Encontrar todos os elementos para extração dos dados do relator
            try:
                dados_relator = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Relator'])
                # Montar uma lista de textos contendo os textos de cada um dos elementos encontrados
                lista_dados_relator = ModuloSTFSelenium.extrair_texto_de_vários_elementos(dados_relator)
            except (TimeoutException, NoSuchElementException):
                lista_dados_relator = []    
            # Criar variável vazia para armazenar o relator
            relator = 'Nâo há'
            # Criar variável vazia para armazenar o redator p/ o acórdão
            redator_p_acórdão = 'Não há'
            # Criar váriável vazia para armazenar o relator do último incidente
            relator_último_incidente = 'Não há recurso interno'
            # Criar variável vazia para armazenar o último incidente
            último_incidente = 'Não há'
            if len(lista_dados_relator) != 0:
                # Percorrer cada elemento da listra de testox contendo os textos dos elementos encontrados
                for elemento in lista_dados_relator:
                    # Definir critério de pesquisa para extrair o relator da lista
                    buscar_relator = 'Relator(a):'
                    #Definir critério de pesquisa para extrair o redator p/ acórdão da lista
                    buscar_redator_p_acórdão = 'Redator(a) do acórdão:'
                    #Definir critério de pesquisa para extrair o relator do último incidente da lista
                    buscar_relator_último_incidente = 'Relator(a) do último incidente:'        
                    #Verificar se o critério de pesquisa do relator está dentro do elemento analisado na iteração
                    if buscar_relator in elemento:
                        #Se estiver, amarazena o argumento encontrado na variável correspondente
                        relator = elemento
                        #Deixar apenas o nome do Minsitro na varável
                        relator = relator[relator.find(':')+2:].strip()
                        # Se a variável relator não contiver nada
                        if len(relator) == 0:
                            # O valor da variável será "Não há"
                            relator = 'Não há'
                    #Verificar se o critério de pesquisa do redator p/ o acórdão está dentro do elemento analisado na iteração
                    if buscar_redator_p_acórdão in elemento:
                        # Se estiver, armazenar o argumento encontrado na variável correspondente
                        redator_p_acórdão = elemento
                        #Deixar apenas o nome do Minsitro na varável
                        redator_p_acórdão = redator_p_acórdão[redator_p_acórdão.find(':')+2:].strip()
                        #Verificar se o critério de pesquisa do relator está dentro do elemento analisado na iteração
                    if buscar_relator_último_incidente in elemento:
                        # Se estiver, armazenar o argumento encontrado na variável correspondente
                        relator_último_incidente = elemento
                        #Extrair relator do último incidente
                        relator_último_incidente = relator_último_incidente[relator_último_incidente.find(':')+1:relator_último_incidente.rfind('(')-1].strip()
                        #Extrair último incidente
                        último_incidente = elemento[elemento.rfind('(')+1:elemento.rfind(')')]
            else:
                None
            
            """ Se o usuário optar por essa pausa, o scrit fará um intervalo de aleatório de 2 a 8 segundos quande existir processo com o número consultado."""
            if pausa_no_meio_do_laço_de_repetição.lower() == 'sim':  # Funcionalidade útil no caso o servidor vir a deixar de atender as requisições com frequência.
                tempo = random.randint(2 , 8)
                iteracoes_de_pausa_executadas += 1
                tempo_total_de_pausa += tempo
                horas_pausa = (int(tempo_total_de_pausa//3600)) # Calcula a quantidade de horas inteiras de execução
                minutos_pausa = int((tempo_total_de_pausa % 3600) //60) # Calcula os minutos inteiros, a partir da fração de hora desprezada na primeira conta
                segundos_pausa = int(tempo_total_de_pausa % 60) # Calcula os segundos, a partir da fração desprezada de minutos da segunda conta
                string_pausas_duração = f'{horas_pausa}h:{minutos_pausa}m:{segundos_pausa}s' # Cria um texto com o formado "0h:0m:0s" para exibir o tempo de execução do programa
                print(f'{("*" * 33)} Fazendo INVERVALO de {tempo} segundos. {("*" * 33)}')
                sleep(tempo)
            else:
                None        
            #Pegar andamentos
            sleep(0.2) # Aguarda 0,2 segundo
            #Chamar a função encontrar_elemento() do módulo para encontrar o elemento correspondente
            elemento_andamentos = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Andamentos'])
            #Pegar, em formato de string, o código html da página relativamente aos andametos
            sleep(0.2) # Aguarda 0,2 segundo
            parser = elemento_andamentos.get_attribute('innerHTML')
            sleep(0.5) # Aguarda 0,5 segundo
            #Na string "parser", pegar os índices inciais de cada um dos adamentos, chamando do módulo a função encontrar_índices()
            índices_iniciais_andamentos = ModuloSTFSelenium.encontrar_indices(parser, '<div class="andamento-item">')
            #Chamando do módulo a função texto_andamentos(), montar uma lista contendo todos os andamentos
            lista_de_andamentos = ModuloSTFSelenium.textos_andamentos(índices_iniciais_andamentos, parser)
            #Contar a quantidade de andamentos existente na lista
            qtde_andamentos = len(lista_de_andamentos)
            #Inverter a lista
            lista_de_andamentos.reverse()
            if len(lista_de_andamentos) == 0 and tamanho_atual == tamanho_anterior:
                sleep(30) # Aguarda 30 segundos
                #Executa novamente as instruções para pegar os andamentos  
                sleep(0.2) # Aguarda 0,2 segundo
                #Chamar a função encontrar_elemento() do módulo para encontrar o elemento correspondente
                elemento_andamentos = ModuloSTFSelenium.encontrar_elemento(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Andamentos'])
                #Pegar, em formato de string, o código html da página relativamente aos andametos
                sleep(0.2) # Aguarda 0,2 segundo
                parser = elemento_andamentos.get_attribute('innerHTML')
                sleep(.5) # Aguarda 0,5 segundo
                #Na string "parser", pegar os índices inciais de cada um dos adamentos, chamando do módulo a função encontrar_índices()
                índices_iniciais_andamentos = ModuloSTFSelenium.encontrar_indices(parser, '<div class="andamento-item">')
                #Chamando do módulo a função texto_andamentos(), montar uma lista contendo todos os andamentos
                lista_de_andamentos = ModuloSTFSelenium.textos_andamentos(índices_iniciais_andamentos, parser)
                #Contar a quantidade de andamentos existente na lista
                qtde_andamentos = len(lista_de_andamentos)
                #Inverter a lista
                lista_de_andamentos.reverse()
            #Transformar a lista em uma string
            string_lista_andamentos = '\n'.join(lista_de_andamentos)
            #Armazenar todos os andamentos para posterior gravação em arquivo com extensão .txt
            todos_os_andamentos = '\n'.join(lista_de_andamentos)
            #Verificar o se o tamanho da string é tem mais de 32766 caracteres:
            if len(string_lista_andamentos) > 32766:
                #Se tiver, capturar os ultimos 32767 caracteres, em razão da liminitação de gravação de dados em arquivo do Excel
                string_lista_andamentos = string_lista_andamentos[len(string_lista_andamentos)-32767:]
            #PEGAR ASSUNTOS
            try:
                #Clicar na aba correspondente
                ModuloSTFSelenium.clicar_em(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Aba_assunto'])
                assuntos = ModuloSTFSelenium.encontrar_todos_os_elementos(navegador, ModuloSTFSelenium.xpathes_dados_buscados['Assunto'])
                #Extrair texto de todos os elementos e colocar em uma lista
                lista_de_assuntos = ModuloSTFSelenium.extrair_texto_de_vários_elementos(assuntos)
            except (TimeoutException, NoSuchElementException):
                lista_de_assuntos = []
            #PEGAR AS PARTES
            atributos_e_nomes_dos_sujeitos = ModuloSTFSelenium.pegar_partes(navegador)
            #Listar sujeitos ativos
            p_ativo = ModuloSTFSelenium.separar_sujeitos_e_procuradores(atributos_e_nomes_dos_sujeitos)[0]
            #Listar representantes processuais do polo ativo
            rep_proc_p_ativo = ModuloSTFSelenium.separar_sujeitos_e_procuradores(atributos_e_nomes_dos_sujeitos)[1]
            #Listar sujeitos passivos
            p_passivo = ModuloSTFSelenium.separar_sujeitos_e_procuradores(atributos_e_nomes_dos_sujeitos)[2]
            #Listar representatnes processuais do polo ativo
            rep_proc_p_passivo = ModuloSTFSelenium.separar_sujeitos_e_procuradores(atributos_e_nomes_dos_sujeitos)[3]
            #Listar terceiros
            terceiros = ModuloSTFSelenium.separar_sujeitos_e_procuradores(atributos_e_nomes_dos_sujeitos)[4]
            #Listar representeantes processuais de terceiros
            rep_proc_terc = ModuloSTFSelenium.separar_sujeitos_e_procuradores(atributos_e_nomes_dos_sujeitos)[5]

            #PEGAR DESPACHOS DE DEVOLUÇÃO E DECISÕES
            lista_de_documentos = ModuloSTFSelenium.despachos_de_devolução_e_decisões(lista_de_andamentos)
            qtde_de_documentos = len(lista_de_documentos)
            #PEGAR OUTROS DOCUMENTOS
            lista_dos_outros_documentos = ModuloSTFSelenium.outros_documentos(lista_de_andamentos)
            #Grava dados extraídos um arquivo com extensão .txt
            with open (rf'{caminho_gravação_de_dados}\{classe_processo} {processo}.txt', 'w', encoding="utf-8") as file:
                file.write(f'{classe_processo} {processo}/{uf_de_origem}\n\n')
                file.write(f'Classe: {classe_processo}\n')
                file.write(f'Número: {processo}\n')
                file.write(f'Número único: {número_único}\n')
                file.write(f'Órgão de origem: {órgão_de_origem}\n')
                file.write(f'Origem: {uf_de_origem}\n')
                file.write(f'Modo de tramitação: {modo_tramitação}\n')
                file.write(f'Publicidade: {publicidade}\n')
                if lista_de_prioridades == []:
                    file.write(f'Critérios de prioridade: Nenhum\n')
                else:
                    file.write('Critérios de prioridade:\n\t\t\t'+'\n\t\t\t'.join(lista_de_prioridades)+'\n')
                file.write(f'Relator: {relator}\n')
                file.write(f'Redator para o acórdão: {redator_p_acórdão}\n')
                file.write(f'Relator do último incidente: {relator_último_incidente}\n')
                file.write(f'Último incidente: {último_incidente}\n')
                file.write('Assuntos:\n\t'+'\n\t'.join(lista_de_assuntos)+'\n')
                file.write('\nPartes:\n'+'\n'.join(atributos_e_nomes_dos_sujeitos)+'\n\n')
                file.write(f'Andamentos:\n{todos_os_andamentos}\n\n')
                file.write("Links das decisões:\n"+'\n'.join(lista_de_documentos)+'\n\n')
                file.write("Link's dos outros documentos disponíveis:\n"+'\n'.join(lista_dos_outros_documentos)+'\n\n')
                file.write(f'Link para consulta: \n\thttps://portal.stf.jus.br/processos/detalhe.asp?incidente={código_do_incidente}\n\n')
                file.write(f'\n\nDia e hora da extração: {datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%y %H:%M:%S")}')
                file.flush()
            #GRAVAR DADOS extraídos um arquivo com extensão .json
            #DEFINE dicionário para os dados extraídos.
            data = {
            "classe": classe_processo,
            "numero": processo,
            "incidente": código_do_incidente,
            "numero_unico":número_único,
            "orgao_de_origem": órgão_de_origem,
            "uf_de_origem": uf_de_origem,
            "modo_tramitacao": modo_tramitação,
            "publicidade": publicidade,
            "prioridades": lista_de_prioridades,
            "paradigma_rep_geral": paradigma_rep_geral if classe_processo in ["ARE", "RE"] else "Não se aplica",
            "relator": relator,
            "redator_acordao": redator_p_acórdão,
            "ultimo_incidente": último_incidente,
            "relator_ultimo_incidente": relator_último_incidente,
            "assuntos": lista_de_assuntos,
            "partes": atributos_e_nomes_dos_sujeitos,
            "p_ativo": p_ativo,
            "rep_proc_ativo": rep_proc_p_ativo,
            "p_passivo": p_passivo,
            "rep_proc_passivo": rep_proc_p_passivo,
            "terceiros": terceiros,
            "rep_proc_terc": rep_proc_terc,
            "andamentos": lista_de_andamentos,
            "docs_decisoes": lista_de_documentos,
            "outros_docs": lista_dos_outros_documentos,
            "data_extracao": f'{datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%y")}'
            }
            #Criar um arquivo ".json" e grava dados extraídos
            with open(rf'{caminho_gravação_de_dados}\{classe_processo} {processo}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            #EXIBIR MENSAGENS de alerta ao usuário
            print(f'{("-" * 100)}\nEXECUÇÃO do programa EM ANDAMENTO.\nNÃO FECHAR a janela do TERMINAL.\nCom o terminal maximizado, pressione Ctrl+C para interromper de forma segura.\n')  # Separador visual
            print('Progresso:\n\n'+ '[ '+('|' * (barra))+('-' * traço)+' ]    ' + str(percentual) + ' %\n\n') # Barra de progresso
            # Incrementa em 1 o número de iterações executadas.
            print(f"Dados extraídos do processo {classe_processo} nº {processo} com sucesso!!!\n{iteracoes_executadas +1} processos consultados.\n")
            iteracoes_executadas += 1
            print(f"Arquivos '*.txt' e '*.json' gravados com sucesso.")  # Mensagem com separador visual
            #Acrescente a classe e o número consultados à lista de extrações bem sucedidas!
            classe_e_numero_dados_extraidos.append(f'{classe_processo} {processo}')
            #Grava arquivo de log provisório e armazena o horário na variável "data_e_hora_fim"
            ModuloSTFSelenium.gravar_log_provisório(inicio,
                                                                iteracoes_executadas,
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
                                                                retomadas_apos_erro)
            #Zera o contador de erros consecutivos
            n_erros_consecutivos = 0
            print(f'Gravação de log provisório.\n{("-" * 100)}\n')  # Mensagem com separador visual
        except (TimeoutException, NoSuchElementException) as erro_capturado:
            # Incrementa a variável erros_ocorridos em 1
            erros_ocorridos += 1
            n_erros_consecutivos += 1
            if n_erros_consecutivos >= 4: #Se ocorrerm três erros consecutivos
                horas_pausa = (int(tempo_total_de_pausa//3600)) # Calcula a quantidade de horas inteiras de execução
                minutos_pausa = int((tempo_total_de_pausa % 3600) //60) # Calcula os minutos inteiros, a partir da fração de hora desprezada na primeira conta
                segundos_pausa = int(tempo_total_de_pausa % 60) # Calcula os segundos, a partir da fração desprezada de minutos da segunda conta
                string_pausas_duração = f"{horas_pausa:02d}h:{minutos_pausa:02d}m:{segundos_pausa}s" # Cria um texto com o formado "0h:0m:0s" para exibir o tempo de execução do programa
                # Define o nome do arquivo de log de erro, para fins de comparação antes de gerar o log final.
                base_nome_erro = f'log_ERRO_NA_EXTRAÇÃO {datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")}.txt'
                # Grava log de erro
                ModuloSTFSelenium.gravar_log_de_erro(inicio,
                                                    iteracoes_executadas,
                                                    caminho_logs_definitivos,
                                                    pesquisar_por, processo,
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
                                                    retomadas_apos_erro)
                # Encerrar o laço de repetição
                break
            else:
                # Fechar navegador
                navegador.quit()
                # Incrementar o tempo total de pausa com a pausa forçada por bloqueio do IP ou queda da internet
                tempo_total_de_pausa += ModuloSTFSelenium.pausar_e_retomar(classe_processo, processo)
                # Incrementar o contador de iteracoes de pausa
                iteracoes_de_pausa_executadas += 1
                # Increementar o contador de retomadas após erro.
                retomadas_apos_erro += 1
                #Definir navegador a ser usado
                navegador = webdriver.Chrome()
                #Definir endereço a ser acessado pelo navegador
                url = 'https://portal.stf.jus.br/'
                #Abrir navegador e acessar o endereço indicado
                navegador.get(url)
                #Maximizar janela do navegador
                navegador.maximize_window()
                continue
        
        except (ReadTimeoutError, urllib3.exceptions.ReadTimeoutError, TimeoutException) as timeout_error:
            print(f"Timeout detectado: {timeout_error}")
            retomadas_apos_erro += 1
            n_erros_consecutivos += 1
            
            # Reiniciar navegador
            try:
                navegador.quit()
            except:
                pass
            
            sleep(15)  # Pausa antes de reiniciar
            navegador = webdriver.Chrome()
            navegador.get(url)
            navegador.maximize_window()
            
            print("Navegador reiniciado. Continuando...")
            continue  # Tenta o mesmo processo novamente

        except KeyboardInterrupt:
            print(f"\n{'='*100}\n")
            print(f"Execução do programa interrompida pelo usuário.\n")
            #Gravar arquivo de log
            logs_snap = []
            data_e_hora_fim = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss") # Redefinir variável "data_e_hora_fim"
            base_nome_interrucao_usuario = f"log_INTERRUPCAO_PELO_USUARIO_{data_e_hora_fim}.txt"
            for arquivo in os.listdir(caminho_log_snapshots):
                if arquivo.endswith('.txt'):
                    logs_snap.append(arquivo)
            if len(logs_snap) > 0:
                nome_base = f'{logs_snap[len(logs_snap)-1]}'
                with open(rf'{caminho_log_snapshots}\{nome_base}', "r", encoding="utf-8") as log_file: # Ler o conteúdo do arquivo de log provisório
                    mensagem_log = log_file.read() # Armazenar o conteúdo do arquivo log provisório na variável "mensagem_log"
                with open (rf'{caminho_logs_definitivos}\{base_nome_interrucao_usuario}', "w", encoding="utf-8") as log_final: # Criar o arquivo de log final
                    log_final.write(f"Execução do programa interrompida pelo usuário.\n")
                    log_final.write(f'Último processo cuja extração foi bem sucedida: {classe_e_numero_dados_extraidos[len(classe_e_numero_dados_extraidos)-1] if len(classe_e_numero_dados_extraidos) > 0 else '__'}\n\n')
                    log_final.write(mensagem_log) # Gravar o contúdo da variável "mengsagem_log" no arquivo
                    log_final.flush() # Certificar que o arquivo foi gravado
                print(f'Gravado log final.\nConsulte o arquivo de log.')  # Mensagem com separador visual
            else:
                print(f"""Arquivo de log não gravado!!!
                    \rCódigo interrompido antes da gravação do primeiro log temporário.
                    \rNÃO HÁ arquivo de log para ser consultado""")
                print(f'Fim da execução do script.')
                print(f"\n{'='*100}\n")
            # Fechar o navegador
                try:
                    navegador.quit()
                except Exception:
                    pass
            break # Encerra o laço de repetição        
        except Exception as erro_capturado:
                # Define o nome do arquivo de log de erro, para fins de comparação antes de gerar o log final.
                base_nome_erro = f'log_ERRO_NA_EXTRAÇÃO {datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")}.txt'
                # Grava log de erro
                ModuloSTFSelenium.gravar_log_de_erro(inicio,
                                                            iteracoes_executadas,
                                                            caminho_logs_definitivos,
                                                            pesquisar_por, processo,
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
                                                            retomadas_apos_erro)
                # Fechar o navegador
                try:
                    navegador.quit()
                except Exception:
                    pass

                break #Encerra o laço de repetição
                
    # GERAR LOG DEFINITIVO
    # Verifica se não foi gerado um arquivo de log de erro ou de interrupção pelo usuário
    if not os.path.exists(rf'{caminho_logs_definitivos}\{base_nome_erro}') and not os.path.exists(rf'{caminho_logs_definitivos}\{base_nome_interrucao_usuario}.txt'): 
        data_e_hora_fim = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss") # Redefinir variável "data_e_hora_fim"
        logs_snap = []
        for arquivo in os.listdir(caminho_log_snapshots):
            if arquivo.endswith('.txt'):
                logs_snap.append(arquivo)
        nome_base = f'{logs_snap[len(logs_snap)-1]}'
        with open(rf'{caminho_log_snapshots}\{nome_base}', "r", encoding="utf-8") as log_file: # Ler o conteúdo do arquivo de log provisório
            mensagem_log = log_file.read() # Armazenar o conteúdo do arquivo log provisório na variável "mensagem_log"
        with open (rf'{caminho_logs_definitivos}\log_EXTRAÇÃO_BEM_SUCEDIDA {data_e_hora_fim}.txt', "w", encoding="utf-8") as log_final: # Criar o arquivo de log final
            log_final.write(mensagem_log) # Gravar o contúdo da variável "mengsagem_log" no arquivo
            log_final.flush() # Certificar que o arquivo foi gravado
    print(f'Gravado log final.\n{("-" * 100)}\n')  # Mensagem com separador visual
    print(f'Fim da execução do script.\nConsulte o arquivo de log.\n{("-" * 100)}\n')
    #Fechar o navegador
    try:
        navegador.quit()
    except Exception:
        pass