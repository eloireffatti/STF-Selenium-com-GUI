import os
import json
from time import sleep
import pandas as pd
import datetime
import ModuloSTFSelenium

caminho_dados_extrator = None
caminho_dados_api = None
caminho_saida = None
nome_arquivo_xlsx = None
nome_arquivo_json = None

def executar_consolidacao(callback_progresso=None):
    global caminho_dados_extrator, caminho_dados_api, caminho_saida
    global nome_arquivo_xlsx, nome_arquivo_json

    if not caminho_dados_extrator or not caminho_dados_api or not caminho_saida:
        raise ValueError("Diretórios não foram configurados antes da execução.")
    if not nome_arquivo_xlsx or not nome_arquivo_json:
        raise ValueError("Nomes de arquivos de saída não foram configurados.")
    # 1) Conta o total de arquivos para a barra de progresso
    arquivos_json = [a for a in os.listdir(caminho_dados_extrator) if a.endswith(".json")]
    total_arquivos = len(arquivos_json)

    # 2) inicializa percent_global
    percent_global = 0
    if callback_progresso:
        callback_progresso(percent_global, 100)

        contador = 0
    dados_compilados = {'classe': [],
                    'numero': [],
                    'incidente': [],
                    'numero_unico': [],
                    'orgao_de_origem': [],
                    'uf_de_origem': [],
                    'classe_na_origem': [],
                    'orgao_julgador_na_origem': [],
                    'modo_tramitacao': [],
                    'publicidade': [],
                    'prioridades': [],
                    'paradigma_rep_geral': [],
                    'relator': [],
                    'redator_acordao': [],
                    'ultimo_incidente': [],
                    'relator_ultimo_incidente': [],
                    'assuntos': [],
                    'assuntos_na_origem': [],
                    'partes': [],
                    'p_ativo': [],
                    'qtde_p_ativo': [],
                    'rep_proc_ativo': [],
                    'qtde_rep_proc_ativo': [],
                    'p_passivo': [],
                    'qtde_p_passivo': [],
                    'rep_proc_passivo': [],
                    'qtde_rep_proc_passivo': [],
                    'terceiros': [],
                    'qtde_terceiros': [],
                    'rep_proc_terc': [],
                    'qtde_rep_proc_terc': [],
                    'andamentos': [],
                    'qtde_andamentos': [],
                    'docs_decisoes': [],
                    'qtde_docs_decisoes': [],
                    'outros_docs': [],
                    'qtde_outros_docs': [],
                    'status_tramitacao': [],
                    'inicio_tramitacao': [],
                    'fim_tramitacao': [],
                    'tramitacao_dias': [],
                    'recursos_internos': [],
                    'qtde_rec_internos': [],
                    'atos_sob_presidencia': [],
                    'dec_inici_presidência': [],
                    'reforma_pres': [],
                    'qtde_reforma_pres': [],
                    'detalh_reforma_pres': [],
                    'orgao_reformador_pres': [],
                    'atos_sob_relator': [],
                    'dec_inic_relator': [],
                    'reforma_rel': [],
                    'qtde_reforma_rel': [],
                    'detalh_reforma_rel': [],
                    'orgao_reformador_rel': [],
                    'julgamentos_virtuais': [],
                    'qtde_julgamentos_virtuais': [],
                    'pedidos_de_destaque': [],
                    'quem_pediu_destaque': [],
                    'pedidos_de_vista': [],
                    'quem_pediu_vista': [],
                    'data_extracao': []
                    }

    lista_de_chaves = list(dict.fromkeys(dados_compilados))
    lista_de_chaves_api = ['classe_stf',
                        'numero_stf',
                        'processo',
                        'fonte', 'classe',
                        'sistema',
                        'modo_tramitacao',
                        'tribunal',
                        'grau',
                        'orgao_julgador',
                        'nivel_sigilo',
                        'assuntos',
                        'andamentos',
                        'data_e_hora_da_extração']

    """ETAPA 1 - Essas ações são importantes para que os dados consolidados sejam extraídos segundo a ordem de autuação dos processos e de acordo com a ordem alfabética dos nomes dos
    arquivos "*.json" ou conforme a ordenação dos arquivos por dada de criação dos próprios arquivos"""
    #CRIA UMA LISTA com os número de processo em ordem crescente orientar a extração ordenada dos dados
    lista_de_processos = []
    # Itera sobre cada um dos arquivos os arquivos contidos no diretório
    # OBSERRVAÇÃO: a o uso da função enumerate permite acessar tamém o número de índice da lista, para que seja montada BARRA DE PROGRESSÃO do processo
    for indice, arquivo in enumerate(os.listdir(caminho_dados_extrator)):
        # Verifica se o o arquivo tem a extensão "*.json" e, se tiver executa a linha seguinte
        if arquivo.endswith('.json'):
            # Abre o arquivo para leitura
            with open (rf'{caminho_dados_extrator}\{arquivo}', 'r', encoding='utf-8') as objeto:
                # Armazena o dicionário contido no arquvo da variável dados
                dados = json.load(objeto)
            # Acrescenta à variável do tipo lista "lista_de_processos" o número contido na chave 'numero' do dicionário contido no arquivo
            lista_de_processos.append(int(dados['numero']))
            
            # # Exibe na tela do prompt uma mensagem para que o usuário sabia que ação está sendo executada pelo script
            print(f"\rColetando número do processo no arquivo {arquivo}", end="")
            
        if callback_progresso:
            percent_global = 25 * (indice + 1) / total_arquivos
            callback_progresso(percent_global, 100)
                
    # Outra mensagem para o usuário
    print("\n\nOrganizando lista de processos.\n")
    # Pausa de 2 segundos para informar o usuário que a lista será reorganizada
    sleep(2)
    #organiza a lista em ordem crescente
    lista_de_processos.sort()
    # Remove eventuais números duplicados, caso hava mais de um arquivo "*.son" por procesos.
    lista_de_processos = list(dict.fromkeys(lista_de_processos))

    # Cria uma lista de processos em formato string
    lista_de_processos_em_formato_string = []
    # itera sobre a lista de processos
    for item in lista_de_processos:
        # Converte o valor de cada item de número inteitor para string e adiciona à lista em formato string
        lista_de_processos_em_formato_string.append(str(item))
    
    total_proc = len(lista_de_processos_em_formato_string)

    # Usando compreensão de lista, cria uma lista dos arquivos com extensão "*.json" do diretório
    lista_de_arquivos = [arq for arq in os.listdir(caminho_dados_extrator) if arq.endswith('.json')]

    """ETAPA 2 - Abrir cada arquivo na ordem numérica crescente de processos, copiar os dados para o dicionário\
    que armazenará os dados para gravação em planilha"""
    # Para cada número de processo, realiza a busca do arquivo correspondente:
    for indice, num_processual in enumerate(lista_de_processos_em_formato_string):
        # - Cria uma variável chamada 'arquivos_a_ser_aberto', cujo valor é definido da seguinte forma
        # - Usa uma expressão generator junto com a função next():
        #   - (arquivo for arquivo in lista_de_arquivos if num_processual in arquivo)
        #     → Cria um iterador que retorna cada arquivo de 'lista_de_arquivos'
        #       cujo nome contém o número do processo atual
        #   - next(..., None)
        #     → Retorna o primeiro arquivo que casa, ou None se nenhum combinar
        arquivo_a_ser_aberto = next((nome_do_arquivo for nome_do_arquivo in lista_de_arquivos if num_processual in nome_do_arquivo), None)
        print(f"\rCompilando dados do arquivo {arquivo_a_ser_aberto}", end="")
        # Verifica se encontrou algum arquivo correspondente (não é None)
        if arquivo_a_ser_aberto:
            # Se encontrou, imprime o nome do arquivo no terminal
            with open (rf'{caminho_dados_extrator}\{arquivo_a_ser_aberto}', 'r', encoding="utf-8") as arquivo:
                dicionario = json.load(arquivo)

                for chave in lista_de_chaves:
                    try:
                        if isinstance(dicionario[chave], list):
                            dados_compilados[chave].append('\n'.join(dicionario[chave]))
                        else:
                            dados_compilados[chave].append(dicionario[chave])        
                    except KeyError:
                        pass

                dados_compilados['qtde_p_ativo'].append(len(dicionario['p_ativo']))
                dados_compilados['qtde_rep_proc_ativo'].append(len(dicionario['rep_proc_ativo']))
                dados_compilados['qtde_p_passivo'].append(len(dicionario['p_passivo']))
                dados_compilados['qtde_rep_proc_passivo'].append(len(dicionario['rep_proc_passivo']))
                dados_compilados['qtde_terceiros'].append(len(dicionario['terceiros']))
                dados_compilados['qtde_rep_proc_terc'].append(len(dicionario['rep_proc_terc']))
                dados_compilados['qtde_andamentos'].append(len(dicionario['andamentos']))
                dados_compilados['qtde_docs_decisoes'].append(len(dicionario['docs_decisoes']))
                dados_compilados['qtde_outros_docs'].append(len(dicionario['outros_docs']))

            with open (rf'{caminho_dados_api}\{arquivo_a_ser_aberto}', 'r', encoding="utf-8") as arquivo:
                dados_api = json.load(arquivo)
                dados_compilados['classe_na_origem'].append(dados_api['classe'])
                dados_compilados['orgao_julgador_na_origem'].append(dados_api['orgao_julgador'])
                dados_compilados['assuntos_na_origem'].append(dados_api['assuntos'])

    if callback_progresso and total_proc > 0:
        percent_global = 25 + 25 * (indice + 1) / total_proc  # 25–50
        callback_progresso(percent_global, 100)

    print(f"\n\nVerificando status de tramitação\n")

    processos_findos = 0
    proc_em_tramitacao = 0
    renovar_consulta = []
    total_and = len(dados_compilados['andamentos'])

    for _, andamentos in enumerate(dados_compilados['andamentos']):
        print(f"Verifcando status de tramitação do {dados_compilados['classe'][_]} {dados_compilados['numero'][_]}", end="\r")
        andamentos = andamentos.split('\n')
        andamentos.reverse()
        status = None
        dia_protocolo = None
        dia_fim = None
        tempo_tramitacao = None
        idx_fim_tramit = []
        marcadores_fim_tramitação = ["Baixa ao arquivo do STF, Guia nº #",
                                    "Baixa definitiva dos autos, Guia nº #",
                                    "Remessa externa dos autos, Guia nº #",
                                    "Recebimento externo dos autos #",                                
                                    "Processo findo #"]
        menor_idx_fim_tramt = None
        # Armazena em uma lista os índices dos marcadores de fim de tramitação
        for andamento in [x.upper() for x in andamentos]:
            for marcador in [x.upper() for x in marcadores_fim_tramitação]:
                if marcador in andamento:
                    idx_fim_tramit.append([x.upper() for x in andamentos].index(andamento))

        try:
            menor_idx_fim_tramt = min(idx_fim_tramit)
        except ValueError:
            menor_idx_fim_tramt = None
        
        # Verifica se há andamentos
        if len(andamentos) == 0 or (len(andamentos) == 1 and andamentos[0].strip() == ''):
            dados_compilados['status_tramitacao'].append(None)
            dados_compilados['tramitacao_dias'].append(None)
            continue

        # Pegar data do protocolo
        for andamento in andamentos:
            if "Protocolado #" in andamento or "Protocolado #".upper() in andamento:   
                data_protocolo = andamento[:10].strip()
                try:
                    dia_protocolo = datetime.datetime.strptime(data_protocolo, "%d/%m/%Y").date()
                except:
                    pass
            break

        # 2. Se não encontrou, usa a data do primeiro andamento da lista
        if not dia_protocolo and len(andamentos) > 0:
            primeiro_andamento = andamentos[-1]  # lembrando que a lista foi invertida
            data_primeiro = primeiro_andamento[:10].strip()
            try:
                dia_protocolo = datetime.datetime.strptime(data_primeiro, "%d/%m/%Y").date()
            except:
                pass

        # PASSA A ANALISAR os marcadores de fim de tramitação a partir do recebimento externo dos autos
        # 1. Baixa com trânsito em julgado
        if status == None and menor_idx_fim_tramt != None:
            if 'Baixa definitiva dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Baixa definitiva dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_baixa_transito = ['Baixa definitiva dos autos, Guia nº #', 'Transitado(a) em julgado #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_baixa_transito]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Baixa com trânsito em julgado"
                # Pegar data da baixa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 2. Baixa com devolução pela Rep 
        if status == None and menor_idx_fim_tramt != None:
            if 'Baixa definitiva dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Baixa definitiva dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_baixa_transito = ['Baixa definitiva dos autos, Guia nº #', 'devol']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_baixa_transito]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução pela Rep geral"
                # Pegar data da baixa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
        
        # 3. Baixa com cancelamento da autuação
        if status == None and menor_idx_fim_tramt != None:
            if 'Baixa definitiva dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Baixa definitiva dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_baixa_transito = ['Baixa definitiva dos autos, Guia nº #', 'Cancelamento de autuação #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_baixa_transito]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Autuação cancelada"
                # Pegar data da baixa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
        
        # 4. Devolução pela Rep Geral
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Agravo provido e determinada a devolução pelo regime da repercussão geral #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução pela Rep Geral"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
                
        # 5. Devolução pela Rep Geral
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Determinada a devolução pelo regime da repercussão geral #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução pela Rep Geral"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 6. Devolução pela Rep Geral
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Reconsidero e devolvo pelo regime da repercussão geral #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução pela Rep Geral"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 7. Devolução pela Rep Geral
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Determinada a devolução em razão de representativo da controvérsia #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução em razão de representativo da controvérsia"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
        
        # 8. Devolução indeterminada
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Determinada a devolução #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução indeterminada"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        #9. Devolução em razão de representativo da controvérsia
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Determinada a devolução em razão de representativo da controvérsia #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução - representativod a controvérsia"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 10. Devolução por impossibilidade de processamento
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Devolução por impossibilidade de processamento']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução por impossibilidade de processamento"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
        
        # 11. Devolução por remessa indevida
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_remessa_devolucao = ['Remessa externa dos autos, Guia nº #','Determino a baixa dos autos - remessa indevida #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_remessa_devolucao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Devolução por remessa indevida"
                # Pegar data da remessa
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 12. Autuação cancelada
        if status == None and menor_idx_fim_tramt != None:
            if 'Processo findo #' in andamentos[menor_idx_fim_tramt] or 'Processo findo #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_cancelamento_autacao = ['Processo findo #','Cancelamento de autuação #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_cancelamento_autacao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Autuação cancelada"
                # Pegar data do fim
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 13. Autuação retificada
        if status == None and menor_idx_fim_tramt != None:
            if 'Processo findo #' in andamentos[menor_idx_fim_tramt] or 'Processo findo #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_retificacao_autacao = ['Processo findo #','Retificação de autuação #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_retificacao_autacao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Autuação retificada"
                # Pegar data do fim
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 14. Reautuado
        if status == None and menor_idx_fim_tramt != None:
            if 'Processo findo #' in andamentos[menor_idx_fim_tramt] or 'Processo findo #'.upper() in andamentos[menor_idx_fim_tramt]:
                indicadores_reautuacao = ['Processo findo #','Reautuado #']
                todos_encontrados = True
                for indicador in [x.upper() for x in indicadores_reautuacao]:
                    encontrado = any(indicador in andamento for andamento in [x.upper() for x in andamentos])
                    if not encontrado:
                        todos_encontrados = False
                        break
                if todos_encontrados:
                    status = "Reautuado"
                # Pegar data do fim
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()

        # 15. Em tramitação
        if status == None and menor_idx_fim_tramt != None:
            if 'Recebimento externo dos autos' in andamentos[menor_idx_fim_tramt] or 'Recebimento externo dos autos'.upper() in andamentos[menor_idx_fim_tramt]:
                status = "Em tramitação"
        else:
            if status == None:
                indicadores_finalizacao = [
                    "Baixa ao arquivo do STF, Guia nº #",
                    "Baixa definitiva dos autos, Guia nº #",
                    "Remessa externa dos autos, Guia nº #", 
                    "Processo findo #"
                ]
                
                # Verifica se NENHUM indicador está presente em QUALQUER andamento
                tem_indicador_finalizacao = any(
                    any(indicador.upper() in andamento.upper() for indicador in indicadores_finalizacao) 
                    for andamento in andamentos
                )
                
                if not tem_indicador_finalizacao:
                    status = "Em tramitação"

        # 16. Baixa por motivo diverso
        if status == None and menor_idx_fim_tramt != None:
            if 'Baixa definitiva dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Baixa definitiva dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                for andamento in andamentos:
                    if "Baixa definitiva dos autos, Guia nº #" in andamento or "Baixa definitiva dos autos, Guia nº #".upper() in andamento:
                        status = "Baixa definitiva - motivo diverso"
                        break
                # Pegar data do fim            
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
        
        # 17. Remessa externa por motivo diverso
        if status == None and menor_idx_fim_tramt != None:
            if 'Remessa externa dos autos, Guia nº #' in andamentos[menor_idx_fim_tramt] or 'Remessa externa dos autos, Guia nº #'.upper() in andamentos[menor_idx_fim_tramt]:
                for andamento in andamentos:
                    if "Remessa externa dos autos, Guia nº #" in andamento or "Remessa externa dos autos, Guia nº #".upper() in andamento:
                        status = "Remessa externa - motivo diverso"
                        break
                # Pegar data do fim
                for andamento in andamentos:
                    if "Remessa externa dos autos, Guia nº #" in andamento or "Remessa externa dos autos, Guia nº #".upper() in andamento:
                        criterio = "Remessa externa dos autos, Guia nº #"
                        if criterio in andamento or criterio.upper() in andamento:
                            data_remessa = andamento[:andamento.find(' -')].strip()
                            dia_fim = datetime.datetime.strptime(data_remessa, "%d/%m/%Y").date()
                            break
            
        # 18. Processo findo por motivo diverso
        if status == None and menor_idx_fim_tramt != None:
            if 'Processo findo #' in andamentos[menor_idx_fim_tramt] or 'Processo findo #'.upper() in andamentos[menor_idx_fim_tramt]:
                for andamento in andamentos:
                    if "Processo findo #" in andamento or "Processo findo #".upper() in andamento:
                        status = "Processo findo - motivo diverso"
                        break
                # Pegar data do fim
                data_baixa = andamentos[menor_idx_fim_tramt][:andamentos[menor_idx_fim_tramt].find(' -')].strip()
                dia_fim = datetime.datetime.strptime(data_baixa, "%d/%m/%Y").date()
        
        if status != '':
            if isinstance(dia_fim, datetime.date) and isinstance(dia_protocolo, datetime.date):
                tempo_tramitacao = dia_fim - dia_protocolo
                tempo_tramitacao = tempo_tramitacao.days

            else:
                tempo_tramitacao = None
                # print("Data de fim ou de protocolo ausentes ou inválidas para calcular tempo de tramitação.")

        dados_compilados['status_tramitacao'].append(status)
        dados_compilados['inicio_tramitacao'].append(dia_protocolo)
        dados_compilados['fim_tramitacao'].append(dia_fim)
        dados_compilados['tramitacao_dias'].append(tempo_tramitacao)

        if callback_progresso and total_and > 0:
            percent_global = 50 + 10 * (_ + 1) / total_and  # 50–60
            callback_progresso(percent_global, 100)

    print("\n\nBuscar recursos internos\n")

    for idx, andamentos in enumerate(dados_compilados['andamentos']):
        print(f"Buscando recursos internos no {dados_compilados['classe'][idx]} {dados_compilados['numero'][idx]}", end="\r")
        andamentos = andamentos.split('\n')
        recursos_internos = ModuloSTFSelenium.busca_recursos_internos(andamentos)
        dados_compilados['recursos_internos'].append('\n'.join(recursos_internos))
        dados_compilados['qtde_rec_internos'].append(len(recursos_internos))

        if callback_progresso and total_and > 0:
            percent_global = 60 + 10 * (idx + 1) / total_and  # 60–70
            callback_progresso(percent_global, 100)

    print("\n\nAnalisar decisões da Presidência\n")

    for idx, andamentos in enumerate(dados_compilados['andamentos']):
        print(f"Analisando decisões da Presidência no {dados_compilados['classe'][idx]} {dados_compilados['numero'][idx]}", end="\r")
        andamentos = andamentos.split('\n')
        atos_sob_presidencia = ModuloSTFSelenium.eventos_presidência_e_relator(andamentos)[0]
        dados_compilados['atos_sob_presidencia'].append('\n'.join(atos_sob_presidencia))
        dados_compilados['dec_inici_presidência'].append(atos_sob_presidencia[0] if atos_sob_presidencia else "")
        analise_reforma_pres = ModuloSTFSelenium.analise_decisoes_presidencia(andamentos)
        dados_compilados['reforma_pres'].append(analise_reforma_pres[0])
        dados_compilados['qtde_reforma_pres'].append(len(analise_reforma_pres[1]))
        dados_compilados['detalh_reforma_pres'].append('\n'.join(analise_reforma_pres[1]) if analise_reforma_pres else "")
        dados_compilados['orgao_reformador_pres'].append('\n'.join(analise_reforma_pres[2]) if analise_reforma_pres else "")
        
        if callback_progresso and total_and > 0:
            percent_global = 60 + 10 * (idx + 1) / total_and  # 60–70
            callback_progresso(percent_global, 100)

    print("\n\nAnalisar decisões do Min. Relator\n")

    for idx, andamentos in enumerate(dados_compilados['andamentos']):
        print(f"Analisando decisões do Min. Relator no {dados_compilados['classe'][idx]} {dados_compilados['numero'][idx]}", end= "\r")
        andamentos = andamentos.split('\n')
        atos_sob_relator = ModuloSTFSelenium.eventos_presidência_e_relator(andamentos)[1]
        dados_compilados['atos_sob_relator'].append('\n'.join(atos_sob_relator))
        dados_compilados['dec_inic_relator'].append(atos_sob_relator[0] if atos_sob_relator else "")
        analise_reforma_rel = ModuloSTFSelenium.analise_decisoes_relator(andamentos)
        dados_compilados['reforma_rel'].append(analise_reforma_rel[0])
        dados_compilados['qtde_reforma_rel'].append(len(analise_reforma_rel[1]))
        dados_compilados['detalh_reforma_rel'].append('\n'.join(analise_reforma_rel[1]) if analise_reforma_rel else "")
        dados_compilados['orgao_reformador_rel'].append('\n'.join(analise_reforma_rel[2]) if analise_reforma_rel else "")
        dados_compilados['julgamentos_virtuais'].append('\n'.join(ModuloSTFSelenium.capturar_julgamentos_virtuais(andamentos)))
        dados_compilados['qtde_julgamentos_virtuais'].append(len(ModuloSTFSelenium.capturar_julgamentos_virtuais(andamentos)))

        if callback_progresso and total_and > 0:
            percent_global = 75 + 5 * (idx + 1) / total_and  # 75–80
            callback_progresso(percent_global, 100)

    print('\n\nBuscar por destaques em julgamentos virtuais\n')

    dados_compilados['pedidos_de_destaque'] = [''] * len(dados_compilados['andamentos'])
    dados_compilados['quem_pediu_destaque'] = [''] * len(dados_compilados['andamentos'])
    dados_compilados['pedidos_de_vista'] = [''] * len(dados_compilados['andamentos'])
    dados_compilados['quem_pediu_vista'] = [''] * len(dados_compilados['andamentos'])

    
    for idx, andamentos in enumerate(dados_compilados['andamentos']):
        print(f"Buscando destaques em julgamentos virtuais do {dados_compilados['classe'][idx]} {dados_compilados['numero'][idx]}", end="\r")
        andamentos = andamentos.split('\n')
        destaques = ModuloSTFSelenium.pedidos_de_destaque(andamentos)
        if not destaques:
            destaques = [("", "")]
        lista_destaques = []
        pediram_destaque = []
        for destaque, quem_pediu in destaques:
            lista_destaques.append(destaque)
            pediram_destaque.append(quem_pediu)   
        dados_compilados['pedidos_de_destaque'][idx] = '\n'.join(lista_destaques)
        dados_compilados['quem_pediu_destaque'][idx] = '\n'.join(pediram_destaque)
        if callback_progresso and total_and > 0:
            percent_global = 80 + 5 * (idx + 1) / total_and  # 80–85
            callback_progresso(percent_global, 100)

    print('\n\nVerificar pedidos de vista\n')

    for idx, andamentos in enumerate(dados_compilados['andamentos']):
        print(f"Buscando pedidos de vista do {dados_compilados['classe'][idx]} {dados_compilados['numero'][idx]}", end="\r")
        andamentos = andamentos.split('\n')
        pedidos_de_vista = ModuloSTFSelenium.pedidos_de_vista(andamentos)
        if not pedidos_de_vista:
            pedidos_de_vista = [("", "")]
        lista_vista = []
        pediram_vista = []
        for destaque, quem_pediu in pedidos_de_vista:
            lista_vista.append(destaque)
            pediram_vista.append(quem_pediu)   
        dados_compilados['pedidos_de_vista'][idx] = '\n'.join(lista_vista)
        dados_compilados['quem_pediu_vista'][idx] = '\n'.join(pediram_vista)
        if callback_progresso and total_and > 0:
            percent_global = 85 + 5 * (idx + 1) / total_and  # 85–90
            callback_progresso(percent_global, 100)

    dicionario_para_json = dados_compilados

    dicionario_para_json = ModuloSTFSelenium.converter_datas_para_string(dicionario_para_json)

    # Salvar o dicionário em arquivo JSON
    print("\n\nGravando arquviov'dados_compilados.json'.\n")
    if callback_progresso:
        callback_progresso(92, 100)

    with open(os.path.join(caminho_saida, nome_arquivo_json), "w", encoding="utf-8") as f:
        json.dump(dicionario_para_json, f, ensure_ascii=False, indent=2)
    
        # Adaptar tamanho da string de cada chave para gravar em Excel
    print("\nAdaptando tamanho das strings para o limite de caracteres por célula no Excel.")
    if callback_progresso:
        callback_progresso(96, 100)

    for chave in lista_de_chaves:
        if isinstance(dados_compilados[chave], str):
            for string in enumerate(dados_compilados[chave]):
                if len(string) > 32767:
                    string_adaptada = string[len(string) - 32767:]

    """Gravar dados em arquivo *.xlsx"""

    print(f"\n\nGravando planilha\n")
    df = pd.DataFrame.from_dict(dados_compilados, orient='index')
    df = df.transpose()
    # Ordenar o DataFrame pela coluna 'numero' convertendo os valores para numéricos, tratando erros de conversão como NaN, e mantendo a ordem original para valores não convertíveis
    df = df.sort_values(by='numero', ascending=True, key=lambda x: pd.to_numeric(x, errors='coerce')).reset_index(drop=True)
    df.to_excel(os.path.join(caminho_saida, nome_arquivo_xlsx), index=False)
    print(f"Planilha gravada com sucesso!!!")

    if callback_progresso:
        callback_progresso(100, 100)

            
    for _, status in enumerate(dados_compilados['status_tramitacao']):
        if status =='Em tramitação':
            renovar_consulta.append(dados_compilados['numero'][_])
          
    print(f"Recursos findos: {str(len(dados_compilados['andamentos'])-processos_findos)}")
    print(f"Recursos ainda em tramitação: {len(renovar_consulta)}")
    print(f'Listagem dos recursos ainda em tramitação: {", ".join([str(x) for x in renovar_consulta])}')
