import requests
import json
import pandas as pd
import os
import datetime
import ftfy


caminho_dados_extrator = r'C:\Users\e_ref\OneDrive\Documentos\Teste'
caminho_gravacao_dados = r'C:\Users\e_ref\OneDrive\Documentos\Teste\API'
chave_publica = None

dicionario_consulta = {
'orgão': ['Tribunal Regional Federal da 1ª Região',
'Tribunal Regional Federal da 2ª Região',
'Tribunal Regional Federal da 3ª Região',
'Tribunal Regional Federal da 4ª Região',
'Tribunal Regional Federal da 5ª Região',
'Tribunal Regional Federal da 6ª Região',
'Tribunal Superior do Trabalho',
'Tribunal Regional do Trabalho da 1ª Região',
'Tribunal Regional do Trabalho da 2ª Região',
'Tribunal Regional do Trabalho da 3ª Região',
'Tribunal Regional do Trabalho da 4ª Região',
'Tribunal Regional do Trabalho da 5ª Região',
'Tribunal Regional do Trabalho da 6ª Região',
'Tribunal Regional do Trabalho da 7ª Região',
'Tribunal Regional do Trabalho da 8ª Região',
'Tribunal Regional do Trabalho da 9ª Região',
'Tribunal Regional do Trabalho da 10ª Região',
'Tribunal Regional do Trabalho da 11ª Região',
'Tribunal Regional do Trabalho da 12ª Região',
'Tribunal Regional do Trabalho da 13ª Região',
'Tribunal Regional do Trabalho da 14ª Região',
'Tribunal Regional do Trabalho da 15ª Região',
'Tribunal Regional do Trabalho da 16ª Região',
'Tribunal Regional do Trabalho da 17ª Região',
'Tribunal Regional do Trabalho da 18ª Região',
'Tribunal Regional do Trabalho da 19ª Região',
'Tribunal Regional do Trabalho da 20ª Região',
'Tribunal Regional do Trabalho da 21ª Região',
'Tribunal Regional do Trabalho da 22ª Região',
'Tribunal Regional do Trabalho da 23ª Região',
'Tribunal Regional do Trabalho da 24ª Região',
'Tribunal Superior Eleitoral',
'Tribunal Regional Eleitoral do Acre',
'Tribunal Regional Eleitoral de Alagoas',
'Tribunal Regional Eleitoral do Amapá',
'Tribunal Regional Eleitoral do Amazonas',
'Tribunal Regional Eleitoral da Bahia',
'Tribunal Regional Eleitoral do Ceará',
'Tribunal Regional Eleitoral do Distrito Federal e Territórios',
'Tribunal Regional Eleitoral do Espírito Santo',
'Tribunal Regional Eleitoral de Goiás',
'Tribunal Regional Eleitoral do Maranhão',
'Tribunal Regional Eleitoral do Mato Grosso',
'Tribunal Regional Eleitoral do Mato Grosso de Sul',
'Tribunal Regional Eleitoral de Minas Gerais',
'Tribunal Regional Eleitoral do Pará',
'Tribunal Regional Eleitoral da Paraíba',
'Tribunal Regional Eleitoral do Paraná',
'Tribunal Regional Eleitoral de Pernambuco',
'Tribunal Regional Eleitoral do Piauí',
'Tribunal Regional Eleitoral do Rio de Janeiro',
'Tribunal Regional Eleitoral do Rio Grande do Norte',
'Tribunal Regional Eleitoral do Rio Grande do Sul',
'Tribunal Regional Eleitoral de Rondônia',
'Tribunal Regional Eleitoral de Roraima',
'Tribunal Regional Eleitoral de Santa Catarina',
'Tribunal Regional Eleitoral de Sergipe',
'Tribunal Regional Eleitoral de São Paulo',
'Tribunal Regional Eleitoral do Tocantins',
'Superior Tribunal Militar',
'Tribunal de Justiça do Acre',
'Tribunal de Justiça de Alagoas',
'Tribunal de Justiça do Amapá',
'Tribunal de Justiça do Amazonas',
'Tribunal de Justiça da Bahia',
'Tribunal de Justiça do Ceará',
'Tribunal de Justiça do Distrito Federal e Territórios',
'Tribunal de Justiça do Espírito Santo',
'Tribunal de Justiça de Goiás',
'Tribunal de Justiça do Maranhão',
'Tribunal de Justiça do Mato Grosso',
'Tribunal de Justiça do Mato Grosso de Sul',
'Tribunal de Justiça de Minas Gerais',
'Tribunal de Justiça do Pará',
'Tribunal de Justiça da Paraíba',
'Tribunal de Justiça do Paraná',
'Tribunal de Justiça de Pernambuco',
'Tribunal de Justiça do Piauí',
'Tribunal de Justiça do Rio de Janeiro',
'Tribunal de Justiça do Rio Grande do Norte',
'Tribunal de Justiça do Rio Grande do Sul',
'Tribunal de Justiça de Rondônia',
'Tribunal de Justiça de Roraima',
'Tribunal de Justiça de Santa Catarina',
'Tribunal de Justiça de Sergipe',
'Tribunal de Justiça de São Paulo',
'Tribunal de Justiça do Tocantins'],
'codigos': ['401',
'402',
'403',
'404',
'405',
'406',
'500',
'501',
'502',
'503',
'504',
'505',
'506',
'507',
'508',
'509',
'510',
'511',
'512',
'513',
'514',
'515',
'516',
'517',
'518',
'519',
'520',
'521',
'522',
'523',
'524',
'600',
'601',
'602',
'603',
'604',
'605',
'606',
'607',
'608',
'609',
'610',
'611',
'612',
'613',
'614',
'615',
'616',
'617',
'618',
'619',
'620',
'621',
'622',
'623',
'624',
'625',
'626',
'627',
'700',
'801',
'802',
'803',
'804',
'805',
'806',
'807',
'808',
'809',
'810',
'811',
'812',
'813',
'814',
'815',
'816',
'817',
'818',
'819',
'820',
'821',
'822',
'823',
'824',
'825',
'826',
'827'],
'endpoint': ['https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trf2/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trf3/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trf4/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trf5/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trf6/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tst/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt1/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt2/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt3/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt4/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt5/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt6/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt7/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt8/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt9/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt10/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt11/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt12/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt13/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt14/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt15/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt16/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt17/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt18/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt19/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt20/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt21/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt22/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt23/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_trt24/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tse/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ac/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-al/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ap/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-am/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ba/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ce/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-dft/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-es/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-go/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ma/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-mt/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ms/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-mg/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pa/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pb/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pr/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pe/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-pi/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rj/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rn/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rs/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-ro/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-rr/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-sc/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-se/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-sp/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tre-to/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_stm/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjac/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjal/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjap/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjam/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjba/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjce/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjdft/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjes/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjgo/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjma/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjmt/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjms/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjpa/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjpb/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjpr/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjpe/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjpi/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjrn/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjrs/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjro/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjrr/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjsc/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjse/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjsp/_search',
'https://api-publica.datajud.cnj.jus.br/api_publica_tjto/_search']
}

dicionario_orgaos_sem_api = {'orgaos': ['Orgao nao identificado',
                                    'Supremo Tribunal Federal',
                                    'Conselho da Justiça Federal',
                                    'Superior Tribunal de Justiça',
                                    'Turma Nacional de Uniformização dos Juizados Especiais Federais',
                                    'Auditoria Militar',
                                    'Auditoria Militar',
                                    'Auditoria Militar'],
                            'codigos': ['001',
                                        '100',
                                        '200',
                                        '300',
                                        '490',
                                        '913',
                                        '921',
                                        '926']
                            }

def validar_chave_api(chave_publica: str) -> bool:
    """
    Valida a chave pública da API DataJud testando-a em múltiplos endpoints.
    
    RETORNA IMEDIATAMENTE TRUE se a chave for aceita em qualquer endpoint.
    SÓ TESTA OS PRÓXIMOS se houver falha/timeout no anterior.
    
    Retorna False apenas se TODOS os endpoints retornarem 401/403 ou erro de rede.
    """
    
    # Corpo mínimo de busca com número impossível (não queremos hits, só validar auth)
    payload = json.dumps({
        "query": {
            "match": {
                "numeroProcesso": "00000000000000000000"
            }
        }
    })

    # Mesmo formato de cabeçalho usado em executar_consulta_api
    headers_base = {
        "Authorization": chave_publica,
        "Content-Type": "application/json",
    }

    # Contadores para o relatório final (só mostrado se falhar)
    erro_autenticacao_count = 0  # 401/403
    erro_http_generico_count = 0  # 400, 500 etc
    erro_rede_count = 0  # timeout, conexão recusada
    
    endpoints_testados = 0
    
    print("\nValidando chave pública em múltiplos endpoints...")
    
    for idx, endpoint in enumerate(dicionario_consulta["endpoint"], 1):
        
        try:
            print(f"[{idx}/{len(dicionario_consulta['endpoint'])}] Testando {endpoint}...", end=" ", flush=True)
            
            resp = requests.post(
                endpoint, 
                headers=headers_base, 
                data=payload, 
                timeout=20
            )
            
            endpoints_testados += 1
            
            # ✓ SUCESSO - Retorna imediatamente!
            if 200 <= resp.status_code < 300:
                print("✓ Válida!\n")
                return True
            
            # ❌ Chave inválida / não autorizada para este endpoint
            if resp.status_code in (401, 403):
                print(f"❌ Rejeitada (HTTP {resp.status_code})")
                erro_autenticacao_count += 1
                continue  # Tenta próximo endpoint
            
            # ⚠ Outros erros HTTP (400, 500, 503 etc.)
            print(f"⚠ HTTP {resp.status_code}")
            erro_http_generico_count += 1
            continue  # Tenta próximo endpoint
            
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError, requests.RequestException) as e:
            print(f"⚠ Erro de rede")
            erro_rede_count += 1
            continue  # Tenta próximo endpoint
    
    # Se chegou aqui, NENHUM endpoint retornou sucesso (2xx)
    print("\n" + "="*70)
    print("VALIDAÇÃO FALHOU - RELATÓRIO:")
    print("="*70)
    print(f"Endpoints testados:             {endpoints_testados}")
    print(f"  ❌ Chave rejeitada (401/403): {erro_autenticacao_count}")
    print(f"  ⚠ Erro HTTP genérico:         {erro_http_generico_count}")
    print(f"  ⚠ Erro de rede/timeout:       {erro_rede_count}")
    print("="*70 + "\n")
    
    return False


def executar_consulta_api():
    """Executa a consulta à API com variáveis globais."""
    global lista_numero_unico, lista_classes_stf, lista_num_stf
    global dicionario_consulta
    
    # Resetar listas
    lista_numero_unico = []
    lista_classes_stf = []
    lista_num_stf = []
    dados_extraidos = {} 
    lista_a_consultar = []
    lista_classe_stf =[]
    lista_numero_stf = []

    # Cria uma lista dos arquivos com dados extraídos da API DataJud
    arquivos_api = [arquivo for arquivo in os.listdir(caminho_gravacao_dados)]
    # Cria uma lista dos arquivos com dados extraídos do site do STF
    arquivos_extrator = [arquivo for arquivo in os.listdir(caminho_dados_extrator) if arquivo.endswith('.json')]
    # Cria uma lista dos arquivos de dados extraídos da API DataJud faltantes
    consultar = [processo for processo in arquivos_extrator if processo not in arquivos_api]
    # Cria uma lista  dos números dos processos que deveriam ter um arquivo na pasta de arquivos dos dados extraídos da API DataJud
    lista_numeros = [int(processo.split(' ')[-1].replace('.json','')) for processo in consultar]
    # Organiza a lista em ordem crescente
    lista_numeros.sort()
    # Transforma os númros da lista em string
    string_lista_num = [str(item) for item in lista_numeros]
    # Lista os arquivos contidos na pasta relativa aos dados extraídos do site do STF
    lista_de_arquivos = [arq for arq in os.listdir(caminho_dados_extrator) if arq.endswith('.json')]

    # Para cada número de processo, realiza a busca do arquivo correspondente:
    for indice, num_processual in enumerate(string_lista_num):
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
                dic_arq = json.load(arquivo)
                lista_a_consultar.append(dic_arq['numero_unico'])     
                lista_classe_stf.append(dic_arq['classe'])
                lista_numero_stf.append(dic_arq['numero'])

    lista_processos = [numero for numero in lista_a_consultar]

    print('\nIniciando consultas...\n\n')
    for idx, processo in enumerate(lista_processos):
        classe_stf = lista_classe_stf[idx]
        numero_stf = lista_numero_stf[idx]
        string_num_processo_para_consulta = processo.replace('.','').replace('-','')
        codigo = string_num_processo_para_consulta[13:16]
        print(f"{classe_stf} {numero_stf} - numero unico: {processo}")    
        if processo == "SEM NÚMERO ÚNICO":
            print("Impossível consultar sem numero unico")
            fonte = 'consulta impossivel, numero unico nao disponivel'
            classe = 'consulta impossivel, numero unico nao disponivel'
            sistema = 'consulta impossivel, numero unico nao disponivel'
            modo_tramitacao = 'consulta impossivel, numero unico nao disponivel'
            tribunal = 'consulta impossivel, numero unico nao disponivel'
            grau = 'consulta impossivel, numero unico nao disponivel'
            orgao_julgador = 'consulta impossivel, numero unico nao disponivel'
            nivel_sigilo = 'consulta impossivel, numero unico nao disponivel'
            assuntos =  'consulta impossivel, numero unico nao disponivel'
            andamentos = 'consulta impossivel, numero unico nao disponivel'
            data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
            with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
            print('Número único não disponível')
            print("GRAVANDO DADOS...\n")      
            continue
        try:
            indice = dicionario_consulta['codigos'].index(codigo)
        except ValueError:
            indice = dicionario_orgaos_sem_api['codigos'].index(codigo)
            fonte = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            classe = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            sistema = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            modo_tramitacao = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            tribunal = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            grau = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            orgao_julgador = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            nivel_sigilo = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            assuntos =  f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            andamentos = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
            data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
            with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
            print(f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API")
            print("GRAVANDO DADOS...\n")
            continue
        except ValueError:
            print("Orgão de origem não dispõe de API")
            fonte = "Orgão de origem não dispõe de API"
            classe = "Orgão de origem não dispõe de API"
            sistema = "Orgão de origem não dispõe de API"
            modo_tramitacao = "Orgão de origem não dispõe de API"
            tribunal = "Orgão de origem não dispõe de API"
            grau = "Orgão de origem não dispõe de API"
            orgao_julgador = "Orgão de origem não dispõe de API"
            nivel_sigilo = "Orgão de origem não dispõe de API"
            assuntos =  "Orgão de origem não dispõe de API"
            andamentos = "Orgão de origem não dispõe de API"
            data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
            with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
            print("Orgão de origem não dispõe de API")
            print("GRAVANDO DADOS...\n")
            continue
        endpoint_api = dicionario_consulta['endpoint'][indice]
        url = endpoint_api

        payload = json.dumps({
        "query": {
            "match": {
            "numeroProcesso": string_num_processo_para_consulta
            }
        }
        })
        headers = {
        'Authorization': chave_publica,
        'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            if response.encoding != response.apparent_encoding:
                response.encoding = response.apparent_encoding
            dicionario = json.loads(response.text)
        except requests.exceptions.ConnectTimeout:
            print(f"Falha de conexão ou timeout para o recurso: {url}")
            fonte = 'Erro de conexão com a API'
            classe = 'Erro de conexão com a API'
            sistema = 'Erro de conexão com a API'
            modo_tramitacao = 'Erro de conexão com a API'
            tribunal = 'Erro de conexão com a API'
            grau = 'Erro de conexão com a API'
            orgao_julgador = 'Erro de conexão com a API'
            nivel_sigilo = 'Erro de conexão com a API'
            assuntos = 'Erro de conexão com a API'
            andamentos = 'Erro de conexão com a API'
            data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
            with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
            print('Erro de conexão com a API')
            print("GRAVANDO DADOS...\n")
            continue   # → "continue" está no lugar certo
        except Exception as e:
            print(f"Erro ao acessar a API: {e}")
            continue
        try:
            if len(dicionario['hits']['hits']) > 0:
                hits = dicionario['hits']['hits'][0]
                fonte = hits['_index']
                classe = hits['_source']['classe']['nome']
                sistema = hits['_source']['sistema']['nome']
                modo_tramitacao = hits['_source']['formato']['nome']
                tribunal = hits['_source']['tribunal']
                grau = hits['_source']['grau']
                orgao_julgador = ftfy.fix_text(hits['_source']['orgaoJulgador']['nome'])
                nivel_sigilo = hits['_source']['nivelSigilo']
                assuntos =  hits['_source']['assuntos'][0]['nome']
                andamentos = []
                try:
                    for item in hits['_source']['movimentos']:
                        if 'complementosTabelados' in item:
                            andamento = f"{item['nome']} - {item['complementosTabelados'][0]['nome']} * {item['dataHora']}"
                        else:
                            andamento = f"{item['nome']} * {item['dataHora']}"
                        andamentos.append(andamento)
                except:
                    andamentos.append("Não estão disponíveis dados sobre andamentos")

            else:
                fonte = 'Não há dados disponíveis'
                classe = 'Não há dados disponíveis'
                sistema = 'Não há dados disponíveis'
                modo_tramitacao = 'Não há dados disponíveis'
                tribunal = 'Não há dados disponíveis'
                grau = 'Não há dados disponíveis'
                orgao_julgador = 'Não há dados disponíveis'
                nivel_sigilo = 'Não há dados disponíveis'
                assuntos =  'Não há dados disponíveis'
                andamentos = 'Não há dados disponíveis'
                data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
                #Criar um arquivo ".json" e grava dados
                with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                print('Não há dados disponíveis')
                print("GRAVANDO DADOS...\n")
                continue          
                
        except:
            print("Não há dados disponíveis")
            fonte = 'Não há dados disponíveis'
            classe = 'Não há dados disponíveis'
            sistema = 'Não há dados disponíveis'
            modo_tramitacao = 'Não há dados disponíveis'
            tribunal = 'Não há dados disponíveis'
            grau = 'Não há dados disponíveis'
            orgao_julgador = 'Não há dados disponíveis'
            nivel_sigilo = 'Não há dados disponíveis'
            assuntos =  'Não há dados disponíveis'
            andamentos = 'Não há dados disponíveis'
            data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            dados_extraidos = { 'classe_stf': classe_stf,
                            'numero_stf': numero_stf,
                            'processo': processo,
                            'fonte': fonte,
                            'classe': classe,
                            'sistema': sistema,
                            'modo_tramitacao': modo_tramitacao,
                            'tribunal': tribunal,
                            'grau': grau,
                            'orgao_julgador': orgao_julgador,
                            'nivel_sigilo': nivel_sigilo,
                            'assuntos': assuntos,
                            'andamentos': andamentos,
                            'data_e_hora_da_extração': data_e_hora_da_extração}
            #Criar um arquivo ".json" e grava dados
            with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
            print('Não há dados disponíveis')
            print("GRAVANDO DADOS...\n")   

        data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        dados_extraidos = { 'classe_stf': classe_stf,
                            'numero_stf': numero_stf,
                            'processo': processo,
                            'fonte': fonte,
                            'classe': classe,
                            'sistema': sistema,
                            'modo_tramitacao': modo_tramitacao,
                            'tribunal': tribunal,
                            'grau': grau,
                            'orgao_julgador': orgao_julgador,
                            'nivel_sigilo': nivel_sigilo,
                            'assuntos': assuntos,
                            'andamentos': andamentos,
                            'data_e_hora_da_extração': data_e_hora_da_extração}
        
        #Criar um arquivo ".json" e grava dados
        with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
            json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
        print("Consulta bem sucedida!")
        print("GRAVANDO DADOS EXTRAÍDOS...\n")

    lista_tupla = []
    lista_num_unico = []
    lista_classe_stf = []
    lista_num_stf = []

    for indice, arquivo in enumerate(os.listdir(caminho_gravacao_dados)):
        # Verifica se o o arquivo tem a extensão "*.json" e, se tiver executa a linha seguinte
        if arquivo.endswith(".json"):
            caminho_arq = rf"{caminho_gravacao_dados}\\{arquivo}"
            
            # pular arquivos vazios
            if os.path.getsize(caminho_arq) == 0:
                print(f"Arquivo JSON vazio ignorado: {arquivo}")
                continue
                # Abre o arquivo para leitura
            with open (rf'{caminho_gravacao_dados}\{arquivo}', 'r', encoding='utf-8') as objeto:
                # Armazena o dicionário contido no arquvo da variável dados
                dados_api = json.load(objeto)
                # Acrescenta à variável do tipo lista "lista_de_processos" o número contido na chave 'numero' do dicionário contido no arquivo
                if dados_api['classe'] == 'Erro de conexão com a API':
                    lista_num_unico.append((dados_api['processo']))
                    lista_classe_stf.append(dados_api['classe_stf'])
                    try:
                        lista_num_stf.append(dados_api['numero_stf'])
                    except KeyError:
                        lista_num_stf.append(dados_api['numero'])

    lista_tupla = list(zip(lista_num_unico, lista_classe_stf, lista_num_stf))
    # tupla1 = ('5021516-78.2020.8.24.0023', 'ARE', '1375534')
    # lista_tupla.insert(0, tupla1)
    while len(lista_tupla) > 0:
        print(f"\nÉ necessário renovar a consulta de {len(lista_tupla)} processos.\n")

        for item in lista_tupla:
            processo = item[0]
            classe_stf = item[1]
            numero_stf = item[2]
            string_num_processo_para_consulta = processo.replace('.','').replace('-','')
            codigo = string_num_processo_para_consulta[13:16]
            print(f"{classe_stf} {numero_stf} - numero unico: {processo}")    
            if processo == "SEM NÚMERO ÚNICO":
                print("Impossível consultar sem numero unico")
                fonte = 'consulta impossivel, numero unico nao disponivel'
                classe = 'consulta impossivel, numero unico nao disponivel'
                sistema = 'consulta impossivel, numero unico nao disponivel'
                modo_tramitacao = 'consulta impossivel, numero unico nao disponivel'
                tribunal = 'consulta impossivel, numero unico nao disponivel'
                grau = 'consulta impossivel, numero unico nao disponivel'
                orgao_julgador = 'consulta impossivel, numero unico nao disponivel'
                nivel_sigilo = 'consulta impossivel, numero unico nao disponivel'
                assuntos =  'consulta impossivel, numero unico nao disponivel'
                andamentos = 'consulta impossivel, numero unico nao disponivel'
                data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                dados_extraidos = { 'classe_stf': classe_stf,
                                    'numero_stf': numero_stf,
                                    'processo': processo,
                                    'fonte': fonte,
                                    'classe': classe,
                                    'sistema': sistema,
                                    'modo_tramitacao': modo_tramitacao,
                                    'tribunal': tribunal,
                                    'grau': grau,
                                    'orgao_julgador': orgao_julgador,
                                    'nivel_sigilo': nivel_sigilo,
                                    'assuntos': assuntos,
                                    'andamentos': andamentos,
                                    'data_e_hora_da_extração': data_e_hora_da_extração}
                with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                        json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                print('Número único não disponível')
                print("GRAVANDO DADOS...\n")      
                continue
            try:
                indice = dicionario_consulta['codigos'].index(codigo)
            except ValueError:
                indice = dicionario_orgaos_sem_api['codigos'].index(codigo)
                fonte = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                classe = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                sistema = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                modo_tramitacao = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                tribunal = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                grau = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                orgao_julgador = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                nivel_sigilo = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                assuntos =  f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                andamentos = f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API"
                data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                dados_extraidos = { 'classe_stf': classe_stf,
                                    'numero_stf': numero_stf,
                                    'processo': processo,
                                    'fonte': fonte,
                                    'classe': classe,
                                    'sistema': sistema,
                                    'modo_tramitacao': modo_tramitacao,
                                    'tribunal': tribunal,
                                    'grau': grau,
                                    'orgao_julgador': orgao_julgador,
                                    'nivel_sigilo': nivel_sigilo,
                                    'assuntos': assuntos,
                                    'andamentos': andamentos,
                                    'data_e_hora_da_extração': data_e_hora_da_extração}
                with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                print(f"{dicionario_orgaos_sem_api['orgaos'][indice]} sem API")
                print("GRAVANDO DADOS...\n")
                continue
            except ValueError:
                print("Orgão de origem não dispõe de API")
                fonte = "Orgão de origem não dispõe de API"
                classe = "Orgão de origem não dispõe de API"
                sistema = "Orgão de origem não dispõe de API"
                modo_tramitacao = "Orgão de origem não dispõe de API"
                tribunal = "Orgão de origem não dispõe de API"
                grau = "Orgão de origem não dispõe de API"
                orgao_julgador = "Orgão de origem não dispõe de API"
                nivel_sigilo = "Orgão de origem não dispõe de API"
                assuntos =  "Orgão de origem não dispõe de API"
                andamentos = "Orgão de origem não dispõe de API"
                data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                dados_extraidos = { 'classe_stf': classe_stf,
                                    'numero_stf': numero_stf,
                                    'processo': processo,
                                    'fonte': fonte,
                                    'classe': classe,
                                    'sistema': sistema,
                                    'modo_tramitacao': modo_tramitacao,
                                    'tribunal': tribunal,
                                    'grau': grau,
                                    'orgao_julgador': orgao_julgador,
                                    'nivel_sigilo': nivel_sigilo,
                                    'assuntos': assuntos,
                                    'andamentos': andamentos,
                                    'data_e_hora_da_extração': data_e_hora_da_extração}
                with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                print("Orgão de origem não dispõe de API")
                print("GRAVANDO DADOS...\n")
                continue
        
            endpoint_api = dicionario_consulta['endpoint'][indice]
            url = endpoint_api

            payload = json.dumps({
            "query": {
                "match": {
                "numeroProcesso": string_num_processo_para_consulta
                }
            }
            })
            headers = {
            'Authorization': chave_publica,
            'Content-Type': 'application/json'
            }

            try:
                response = requests.post(url, headers=headers, data=payload, timeout=10)
                if response.encoding != response.apparent_encoding:
                    response.encoding = response.apparent_encoding
                dicionario = json.loads(response.text)
            except requests.exceptions.ConnectTimeout:
                print(f"Falha de conexão ou timeout para o recurso: {url}")
                fonte = 'Erro de conexão com a API'
                classe = 'Erro de conexão com a API'
                sistema = 'Erro de conexão com a API'
                modo_tramitacao = 'Erro de conexão com a API'
                tribunal = 'Erro de conexão com a API'
                grau = 'Erro de conexão com a API'
                orgao_julgador = 'Erro de conexão com a API'
                nivel_sigilo = 'Erro de conexão com a API'
                assuntos = 'Erro de conexão com a API'
                andamentos = 'Erro de conexão com a API'
                data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                dados_extraidos = { 'classe_stf': classe_stf,
                                    'numero_stf': numero_stf,
                                    'processo': processo,
                                    'fonte': fonte,
                                    'classe': classe,
                                    'sistema': sistema,
                                    'modo_tramitacao': modo_tramitacao,
                                    'tribunal': tribunal,
                                    'grau': grau,
                                    'orgao_julgador': orgao_julgador,
                                    'nivel_sigilo': nivel_sigilo,
                                    'assuntos': assuntos,
                                    'andamentos': andamentos,
                                    'data_e_hora_da_extração': data_e_hora_da_extração}
                with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                print('Erro de conexão com a API')
                print("GRAVANDO DADOS...\n")
                continue   # → "continue" está no lugar certo
            except Exception as e:
                print(f"Erro ao acessar a API: {e}")
                continue

            try:
                if len(dicionario['hits']['hits']) > 0:
                    hits = dicionario['hits']['hits'][0]
                    fonte = hits['_index']
                    classe = hits['_source']['classe']['nome']
                    sistema = hits['_source']['sistema']['nome']
                    modo_tramitacao = hits['_source']['formato']['nome']
                    tribunal = hits['_source']['tribunal']
                    grau = hits['_source']['grau']
                    orgao_julgador = ftfy.fix_text(hits['_source']['orgaoJulgador']['nome'])
                    nivel_sigilo = hits['_source']['nivelSigilo']
                    assuntos =  hits['_source']['assuntos'][0]['nome']
                    andamentos = []
                    try:
                        for item in hits['_source']['movimentos']:
                            if 'complementosTabelados' in item:
                                andamento = f"{item['nome']} - {item['complementosTabelados'][0]['nome']} * {item['dataHora']}"
                            else:
                                andamento = f"{item['nome']} * {item['dataHora']}"
                            andamentos.append(andamento)
                    except:
                        andamentos.append("Não estão disponíveis dados sobre andamentos")

                else:
                    fonte = 'Não há dados disponíveis'
                    classe = 'Não há dados disponíveis'
                    sistema = 'Não há dados disponíveis'
                    modo_tramitacao = 'Não há dados disponíveis'
                    tribunal = 'Não há dados disponíveis'
                    grau = 'Não há dados disponíveis'
                    orgao_julgador = 'Não há dados disponíveis'
                    nivel_sigilo = 'Não há dados disponíveis'
                    assuntos =  'Não há dados disponíveis'
                    andamentos = 'Não há dados disponíveis'
                    data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                    dados_extraidos = { 'classe_stf': classe_stf,
                                    'numero_stf': numero_stf,
                                    'processo': processo,
                                    'fonte': fonte,
                                    'classe': classe,
                                    'sistema': sistema,
                                    'modo_tramitacao': modo_tramitacao,
                                    'tribunal': tribunal,
                                    'grau': grau,
                                    'orgao_julgador': orgao_julgador,
                                    'nivel_sigilo': nivel_sigilo,
                                    'assuntos': assuntos,
                                    'andamentos': andamentos,
                                    'data_e_hora_da_extração': data_e_hora_da_extração}
                    #Criar um arquivo ".json" e grava dados
                    with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                        json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                    print('Não há dados disponíveis')
                    print("GRAVANDO DADOS...\n")
                    continue
            except:
                print("Não há dados disponíveis")
                fonte = 'Não há dados disponíveis'
                classe = 'Não há dados disponíveis'
                sistema = 'Não há dados disponíveis'
                modo_tramitacao = 'Não há dados disponíveis'
                tribunal = 'Não há dados disponíveis'
                grau = 'Não há dados disponíveis'
                orgao_julgador = 'Não há dados disponíveis'
                nivel_sigilo = 'Não há dados disponíveis'
                assuntos =  'Não há dados disponíveis'
                andamentos = 'Não há dados disponíveis'
                data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
                #Criar um arquivo ".json" e grava dados
                with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
                print("GRAVANDO DADOS...\n")
        
            data_e_hora_da_extração = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            dados_extraidos = { 'classe_stf': classe_stf,
                                'numero_stf': numero_stf,
                                'processo': processo,
                                'fonte': fonte,
                                'classe': classe,
                                'sistema': sistema,
                                'modo_tramitacao': modo_tramitacao,
                                'tribunal': tribunal,
                                'grau': grau,
                                'orgao_julgador': orgao_julgador,
                                'nivel_sigilo': nivel_sigilo,
                                'assuntos': assuntos,
                                'andamentos': andamentos,
                                'data_e_hora_da_extração': data_e_hora_da_extração}
            
            #Criar um arquivo ".json" e grava dados
            with open(rf'{caminho_gravacao_dados}\{classe_stf} {numero_stf}.json', 'w', encoding='utf-8') as f:
                json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
            print("Consulta bem sucedida!")
            print("GRAVANDO DADOS EXTRAÍDOS...\n")

        lista_tupla = []
        lista_num_unico = []
        lista_classe_stf = []
        lista_num_stf = []
        for indice, arquivo in enumerate(os.listdir(caminho_gravacao_dados)):
            # Verifica se o o arquivo tem a extensão "*.json" e, se tiver executa a linha seguinte
            if arquivo.endswith('.json'):
                # Abre o arquivo para leitura
                with open (rf'{caminho_gravacao_dados}\{arquivo}', 'r', encoding='utf-8') as objeto:
                    # Armazena o dicionário contido no arquvo da variável dados
                    dados_api = json.load(objeto)
                    # Acrescenta à variável do tipo lista "lista_de_processos" o número contido na chave 'numero' do dicionário contido no arquivo
                    if dados_api['classe'] == 'Erro de conexão com a API':
                        lista_num_unico.append((dados_api['processo']))
                        lista_classe_stf.append(dados_api['classe_stf'])
                        try:
                            lista_num_stf.append(dados_api['numero_stf'])
                        except KeyError:
                            lista_num_stf.append(dados_api['numero'])

        lista_tupla = list(zip(lista_num_unico, lista_classe_stf, lista_num_stf))

    print("\nConsulta à API DataJud completa!!!\n")
if __name__ == "__main__":
    executar_consulta_api()