import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import glob, os
import traceback
from datetime import datetime
import sys

class LogRedirector:
    """Redireciona prints para um callback (registrar_log)."""
    def __init__(self, write_callback):
        self.write_callback = write_callback
    
    def write(self, text):
        text = text.strip()
        if text:
            self.write_callback(text)
    
    def flush(self):
        pass


class STFExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Extrator STF - Interface Gráfica")
        self.root.geometry("900x750")
        
        # Variáveis de controle
        self.executando_stf = False
        self.executando_api = False
        self.executando_plan = False
        self.thread_execucao = None
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba 1: STF_Selenium
        self.frame_stf = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_stf, text="Extração STF")
        self._criar_aba_stf()
        
        # Aba 2: API DataJud
        self.frame_api = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_api, text="Consulta DataJud")
        self._criar_aba_api()
        
        # Aba 3: Planilha com Dados da API
        self.frame_plan = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_plan, text="Consolidar Dados")
        self._criar_aba_plan()
    
    # ==================== ABA 1: STF_SELENIUM ====================
    
    def _criar_aba_stf(self):
        """Cria a interface para o módulo STF_Selenium_v3."""
        root = self.frame_stf
        
        # Classe pesquisada
        tk.Label(root, text="Classe Pesquisada:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.classe_entry = ttk.Combobox(
            root,
            values=[
                "AC","ACO","ADC","ADI","ADO","ADPF","AI","AImp","AO","AOE","AP","AR","ARE","AS",
                "CC","Cm","EI","EL","Ext","HC","HD","IF","Inq","MI","MS","Pet","PPE","PSV","Rcl",
                "RE","RHC","RHD","RMI","RMS","RvC","SIRDR","SL","SS","STA","STP","TPA"
            ]
        )
        self.classe_entry.set("")
        self.classe_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Tipo de pesquisa
        tk.Label(root, text="Pesquisar por:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.tipovar = tk.StringVar(value="intervalo")
        ttk.Radiobutton(
            root, text="Intervalo",
            variable=self.tipovar, value="intervalo",
            command=self.atualizar_interface_stf
        ).grid(row=1, column=1, sticky="w", padx=10)
        ttk.Radiobutton(
            root, text="Lista",
            variable=self.tipovar, value="lista",
            command=self.atualizar_interface_stf
        ).grid(row=1, column=2, sticky="w", padx=10)
        
        # Intervalo
        tk.Label(root, text="Número inicial:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.numinicial = tk.Entry(root)
        self.numinicial.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        tk.Label(root, text="Número final:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.numfinal = tk.Entry(root)
        self.numfinal.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Lista de processos
        tk.Label(root, text="Lista de processos:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.listaentry = tk.Entry(root, width=50)
        self.listaentry.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Diretórios
        tk.Label(root, text="Diretório de dados:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.dirdados = tk.Entry(root, width=50)
        self.dirdados.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_dados_stf).grid(row=5, column=2, padx=5, pady=5)
        
        tk.Label(root, text="Diretório de logs:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.dirlogs = tk.Entry(root, width=50)
        self.dirlogs.grid(row=6, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_logs_stf).grid(row=6, column=2, padx=5, pady=5)
        
        # Pausas maiores
        tk.Label(root, text="Pausas maiores:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.pausasmaiores = tk.StringVar(value="Nao")
        ttk.Radiobutton(
            root, text="Sim",
            variable=self.pausasmaiores, value="Sim"
        ).grid(row=7, column=1, sticky="w", padx=10)
        ttk.Radiobutton(
            root, text="Não",
            variable=self.pausasmaiores, value="Nao"
        ).grid(row=7, column=2, sticky="w", padx=10)
        
        # Botão iniciar
        self.startbtn_stf = ttk.Button(root, text="Iniciar Extração STF", command=self.iniciar_stf)
        self.startbtn_stf.grid(row=8, column=0, columnspan=3, pady=15)
        
        # Barra de progresso
        self.progress_stf = ttk.Progressbar(root, length=500, mode="determinate")
        self.progress_stf.grid(row=9, column=0, columnspan=3, pady=5, sticky="ew", padx=10)
        
        # Área de log
        tk.Label(root, text="Log de Execução:").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.logarea_stf = tk.Text(root, height=12, wrap=tk.WORD)
        self.logarea_stf.grid(row=10, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.logarea_stf.yview)
        scrollbar.grid(row=10, column=3, sticky="ns", pady=5)
        self.logarea_stf.config(yscrollcommand=scrollbar.set)
        
        root.grid_rowconfigure(10, weight=1)
        root.grid_columnconfigure(1, weight=1)
    
    # ==================== ABA 2: API_DATAJUD ====================
    
    def _criar_aba_api(self):
        """Cria a interface para o módulo API_DataJud_v3."""
        root = self.frame_api
        
        # Diretório de dados do extrator
        tk.Label(root, text="Diretório de dados do extrator:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.dir_dados_extrator_api = tk.Entry(root, width=50)
        self.dir_dados_extrator_api.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_dados_extrator_api).grid(row=0, column=2, padx=5, pady=5)
        
        # Diretório de gravação de dados
        tk.Label(root, text="Diretório para gravar dados:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.dir_gravacao_api = tk.Entry(root, width=50)
        self.dir_gravacao_api.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_gravacao_api).grid(row=1, column=2, padx=5, pady=5)
        
        # Chave pública (padrão)
        tk.Label(root, text="Chave Pública API:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.chave_api = tk.Entry(root, width=50)
        self.chave_api.insert(0, 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==')
        self.chave_api.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Botão iniciar
        self.startbtn_api = ttk.Button(root, text="Iniciar Consulta DataJud", command=self.iniciar_api)
        self.startbtn_api.grid(row=3, column=0, columnspan=3, pady=15)
        
        # Área de log
        tk.Label(root, text="Log de Execução:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.logarea_api = tk.Text(root, height=15, wrap=tk.WORD)
        self.logarea_api.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.logarea_api.yview)
        scrollbar.grid(row=5, column=3, sticky="ns", pady=5)
        self.logarea_api.config(yscrollcommand=scrollbar.set)
        
        root.grid_rowconfigure(5, weight=1)
        root.grid_columnconfigure(1, weight=1)
    
    # ==================== ABA 3: PLANEJADOR COM DADOS DA API ====================
    
    def _criar_aba_plan(self):
        """Cria a interface para o módulo Mon_Plan_c_dados_API."""
        root = self.frame_plan
        
        # Diretório de dados do extrator
        tk.Label(root, text="Diretório de dados do extrator:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.dir_dados_extrator_plan = tk.Entry(root, width=50)
        self.dir_dados_extrator_plan.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_dados_extrator_plan).grid(row=0, column=2, padx=5, pady=5)
        
        # Diretório de dados da API
        tk.Label(root, text="Diretório de dados da API:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.dir_dados_api_plan = tk.Entry(root, width=50)
        self.dir_dados_api_plan.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_dados_api_plan).grid(row=1, column=2, padx=5, pady=5)
        
        # Diretório para gravação da planilha
        tk.Label(root, text="Diretório para gravar planilha:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.dir_saida_plan = tk.Entry(root, width=50)
        self.dir_saida_plan.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        ttk.Button(root, text="Selecionar", command=self.selecionar_saida_plan).grid(row=2, column=2, padx=5, pady=5)
        
        # Nome da planilha de saída
        tk.Label(root, text="Nome do arquivo *.xlsx de saída:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.nome_arquivo_plan = tk.Entry(root, width=50)
        self.nome_arquivo_plan.insert(0, "dados_compilados.xlsx")
        self.nome_arquivo_plan.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

        # Nome do Json de saída
        tk.Label(root, text="Nome do arquivo *.json de saída:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.nome_arquivo_json = tk.Entry(root, width=50)
        self.nome_arquivo_json.insert(0, "dados_compilados.json")
        self.nome_arquivo_json.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

        # Botão iniciar
        self.startbtn_plan = ttk.Button(root, text="Iniciar Consolidação de Dados", command=self.iniciar_plan)
        self.startbtn_plan.grid(row=5, column=0, columnspan=3, pady=15)
        
        # Barra de progresso
        self.progress_plan = ttk.Progressbar(root, length=500, mode="determinate")
        self.progress_plan.grid(row=6, column=0, columnspan=3, pady=(2, 0), sticky="ew", padx=10)
        
        # Área de log
        tk.Label(root, text="Log de Execução:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.logarea_plan = tk.Text(root, height=12, wrap=tk.WORD)
        self.logarea_plan.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.logarea_plan.yview)
        scrollbar.grid(row=7, column=3, sticky="ns", pady=5)
        self.logarea_plan.config(yscrollcommand=scrollbar.set)
        
        root.grid_rowconfigure(7, weight=1)
        root.grid_columnconfigure(1, weight=1)
    
    # ==================== MÉTODOS STF ====================
    
    def atualizar_interface_stf(self):
        """Atualiza visibilidade dos campos conforme tipo de pesquisa."""
        tipo = self.tipovar.get()
        if tipo == "intervalo":
            self.numinicial.config(state=tk.NORMAL)
            self.numfinal.config(state=tk.NORMAL)
            self.listaentry.config(state=tk.DISABLED)
        else:
            self.numinicial.config(state=tk.DISABLED)
            self.numfinal.config(state=tk.DISABLED)
            self.listaentry.config(state=tk.NORMAL)
    
    def selecionar_dados_stf(self):
        pasta = filedialog.askdirectory(title="Selecione diretório de dados")
        if pasta:
            self.dirdados.delete(0, tk.END)
            self.dirdados.insert(0, pasta)
    
    def selecionar_logs_stf(self):
        pasta = filedialog.askdirectory(title="Selecione diretório de logs")
        if pasta:
            self.dirlogs.delete(0, tk.END)
            self.dirlogs.insert(0, pasta)
    
    def iniciar_stf(self):
        """Valida os dados e inicia a extração em uma thread."""
        if self.executando_stf:
            messagebox.showwarning("Atenção", "Uma extração STF já está em andamento!")
            return
        
        # Validações
        classe = self.classe_entry.get()
        if not classe:
            messagebox.showerror("Erro", "Selecione uma classe processual!")
            return
        
        tipopesquisa = self.tipovar.get()
        
        if tipopesquisa == "intervalo":
            try:
                numini = int(self.numinicial.get())
                numfim = int(self.numfinal.get())
                if numini >= numfim:
                    messagebox.showerror("Erro", "Número inicial deve ser menor que número final!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Digite números válidos no intervalo!")
                return
            listaproc = None
        else:
            entradalista = self.listaentry.get().strip()
            if not entradalista:
                messagebox.showerror("Erro", "Digite a lista de processos!")
                return
            try:
                listaproc = [int(x.strip()) for x in entradalista.split(",")]
            except ValueError:
                messagebox.showerror("Erro", "A lista deve conter apenas números separados por vírgula!")
                return
            numini = None
            numfim = None
        
        # Validar diretórios
        dirdados = self.dirdados.get()
        dirlogs = self.dirlogs.get()
        if not dirdados or not dirlogs:
            messagebox.showerror("Erro", "Selecione ambos os diretórios!")
            return
        
        pausasmaiores = self.pausasmaiores.get().lower()
        
        # Iniciar thread
        self.executando_stf = True
        self.startbtn_stf.config(state=tk.DISABLED)
        self.logarea_stf.delete(1.0, tk.END)
        self.progress_stf["value"] = 0
        
        self.thread_execucao = threading.Thread(
            target=self.executar_stf,
            args=(classe, tipopesquisa, numini, numfim, listaproc, dirdados, dirlogs, pausasmaiores),
            daemon=True
        )
        self.thread_execucao.start()
    
    def atualizar_progresso_stf(self, percentual):
        try:
            self.progress_stf["value"] = percentual
            self.root.update_idletasks()
        except Exception:
            pass
    
    def executar_stf(self, classe, tipopesquisa, numini, numfim, listaproc, dirdados, dirlogs, pausasmaiores):
        """Executa a extração STF."""
        old_stdout = sys.stdout
        try:
            sys.stdout = LogRedirector(lambda msg: self.registrar_log_stf(msg))
            
            import STF_Selenium_v3
            
            self.registrar_log_stf("Iniciando extração STF...")
            self.registrar_log_stf(f"Classe: {classe} | Tipo: {tipopesquisa}")
            if tipopesquisa == "intervalo":
                self.registrar_log_stf(f"Intervalo: {numini} a {numfim}")
            else:
                self.registrar_log_stf(f"Lista com {len(listaproc)} processos")
            self.registrar_log_stf(f"Diretório de dados: {dirdados}")
            self.registrar_log_stf(f"Diretório de logs: {dirlogs}")
            self.registrar_log_stf("=" * 60)
            
            STF_Selenium_v3.executar_extracao_STF(
                classe_pesquisada=classe,
                pesquisar_por=tipopesquisa,
                núm_inicial=numini,
                núm_final=numfim,
                lista_de_processos=listaproc,
                caminho_gravação_de_dados=dirdados,
                caminho_logs_definitivos=dirlogs,
                caminho_log_snapshots=None,
                pausa_no_meio_do_laço_de_repetição=pausasmaiores,
                callback_progresso=self.atualizar_progresso_stf
            )            
     
            self.progress_stf["value"] = 100
            conteudo_log = self.logarea_stf.get("1.0", tk.END)
            if "ERRO NA EXTRAÇÃO DOS DADOS!!!" in conteudo_log:
                messagebox.showerror(
                    "✗ Erro!",
                    "Houve um erro fatal na extração STF e o código foi interrompido prematuramente."
                    "CONSULTE a área de log na interface grávifica ou os arquivos de log."
                )
            else:
                self.registrar_log_stf("✓ Extração STF concluída com sucesso!")
                messagebox.showinfo("Sucesso", "Extração STF finalizada com sucesso!")
            
        except Exception as e:
            self.registrar_log_stf(f"✗ Erro durante extração: {e}")
            self.registrar_log_stf(traceback.format_exc())
            messagebox.showerror("Erro", f"Erro na extração:\n{e}")
        
        finally:
            try:
                sys.stdout = old_stdout
            except Exception:
                pass
            self.executando_stf = False
            self.startbtn_stf.config(state=tk.NORMAL)
    
    def registrar_log_stf(self, mensagem):
        """Registra mensagem na área de log STF."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logarea_stf.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.logarea_stf.see(tk.END)
        self.root.update_idletasks()
    
    # ==================== MÉTODOS API ====================
    
    def selecionar_dados_extrator_api(self):
        pasta = filedialog.askdirectory(title="Selecione diretório de dados do extrator")
        if pasta:
            self.dir_dados_extrator_api.delete(0, tk.END)
            self.dir_dados_extrator_api.insert(0, pasta)
    
    def selecionar_gravacao_api(self):
        pasta = filedialog.askdirectory(title="Selecione diretório para gravar dados")
        if pasta:
            self.dir_gravacao_api.delete(0, tk.END)
            self.dir_gravacao_api.insert(0, pasta)
    
    def iniciar_api(self):
        """Valida e inicia consulta à API DataJud."""
        if self.executando_api:
            messagebox.showwarning("Atenção", "Uma consulta DataJud já está em andamento!")
            return
        
        dir_extrator = self.dir_dados_extrator_api.get()
        dir_gravacao = self.dir_gravacao_api.get()
        chave_api = self.chave_api.get()
        
        if not dir_extrator or not dir_gravacao:
            messagebox.showerror("Erro", "Selecione ambos os diretórios!")
            return
        
        if not chave_api:
            messagebox.showerror("Erro", "Informe a chave pública da API!")
            return
        
        self.executando_api = True
        self.startbtn_api.config(state=tk.DISABLED)
        self.logarea_api.delete(1.0, tk.END)
        
        self.thread_execucao = threading.Thread(
            target=self.executar_api,
            args=(dir_extrator, dir_gravacao, chave_api),
            daemon=True
        )
        self.thread_execucao.start()    
  
    def executar_api(self, dir_extrator, dir_gravacao, chave_api):
        """Executa consulta à API DataJud."""
        
        import API_DataJud_v3

        old_stdout = sys.stdout
        try:
            sys.stdout = LogRedirector(lambda msg: self.registrar_log_api(msg))
            
            # 1) Validar chave ANTES de iniciar qualquer consulta
            self.registrar_log_api("Validando chave pública da API DataJud...\n")
            if not API_DataJud_v3.validar_chave_api(chave_api):
                self.registrar_log_api("Chave pública da API inválida ou não autorizada. Verifique a chave informada.\n")
                messagebox.showerror(
                    "Erro na API DataJud",
                    "Chave pública da API inválida ou não autorizada.\n"
                    "Consulte a chave atual no site do CNJ."
                )
                return  # aborta sem exibir 'Não há dados disponíveis'

            self.registrar_log_api("Chave válida. Iniciando consultas DataJud...\n")
            
            
            
            # Modificar variáveis do módulo com os caminhos fornecidos
            API_DataJud_v3.caminho_dados_extrator = dir_extrator
            API_DataJud_v3.caminho_gravacao_dados = dir_gravacao
            API_DataJud_v3.chave_publica = chave_api
            API_DataJud_v3.executar_consulta_api()
            
            self.registrar_log_api("Iniciando consulta à API DataJud...")
            self.registrar_log_api(f"Diretório de dados do extrator: {dir_extrator}")
            self.registrar_log_api(f"Diretório para gravação: {dir_gravacao}")
            self.registrar_log_api("=" * 60)
            
            # O módulo API_DataJud_v3 já executa seu código principal ao ser importado
            # Aqui ele rodará com os caminhos atualizados
            
            self.registrar_log_api("✓ Consulta DataJud concluída com sucesso!")
            messagebox.showinfo("Sucesso", "Consulta DataJud finalizada com sucesso!")
            
        except Exception as e:
            self.registrar_log_api(f"✗ Erro durante consulta: {e}")
            self.registrar_log_api(traceback.format_exc())
            messagebox.showerror("Erro", f"Erro na consulta:\n{e}")
        
        finally:
            try:
                sys.stdout = old_stdout
            except Exception:
                pass
            self.executando_api = False
            self.startbtn_api.config(state=tk.NORMAL)
    
    def registrar_log_api(self, mensagem):
        """Registra mensagem na área de log API."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logarea_api.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.logarea_api.see(tk.END)
        self.root.update_idletasks()
    
    # ==================== MÉTODOS CONSOLIDADOR ====================
    
    def selecionar_dados_extrator_plan(self):
        pasta = filedialog.askdirectory(title="Selecione diretório de dados do extrator")
        if pasta:
            self.dir_dados_extrator_plan.delete(0, tk.END)
            self.dir_dados_extrator_plan.insert(0, pasta)
    
    def selecionar_dados_api_plan(self):
        pasta = filedialog.askdirectory(title="Selecione diretório de dados da API")
        if pasta:
            self.dir_dados_api_plan.delete(0, tk.END)
            self.dir_dados_api_plan.insert(0, pasta)
    
    def selecionar_saida_plan(self):
        pasta = filedialog.askdirectory(title="Selecione diretório para gravar planilha")
        if pasta:
            self.dir_saida_plan.delete(0, tk.END)
            self.dir_saida_plan.insert(0, pasta)
    
    def iniciar_plan(self):
        """Valida e inicia consolidação de dados."""
        if self.executando_plan:
            messagebox.showwarning("Atenção", "Uma consolidação já está em andamento!")
            return
        
        dir_extrator = self.dir_dados_extrator_plan.get()
        dir_api = self.dir_dados_api_plan.get()
        dir_saida = self.dir_saida_plan.get()
        nome_arquivo_plan = self.nome_arquivo_plan.get()
        nome_arquivo_json = self.nome_arquivo_json.get()
        
        if not dir_extrator or not dir_api or not dir_saida:
            messagebox.showerror("Erro", "Selecione todos os diretórios!")
            return
        
        if not nome_arquivo_plan or not nome_arquivo_json:
            messagebox.showerror("Erro", "Informe o nome do arquivo de saída!")
            return
        
        self.executando_plan = True
        self.startbtn_plan.config(state=tk.DISABLED)
        self.logarea_plan.delete(1.0, tk.END)
        self.progress_plan["value"] = 0
        
        self.thread_execucao = threading.Thread(
            target=self.executar_plan,
            args=(dir_extrator, dir_api, dir_saida, nome_arquivo_plan, nome_arquivo_json),
            daemon=True
        )
        self.thread_execucao.start()
    
    def atualizar_progresso_plan(self, atual, total):
        try:
            if total > 0:
                percentual = (atual / total) * 100
                self.progress_plan["value"] = percentual
            self.root.update_idletasks()
        except Exception:
            pass
    
    def executar_plan(self, dir_extrator, dir_api, dir_saida, nome_arquivo_plan, nome_arquivo_json):
        """Executa consolidação de dados."""
        old_stdout = sys.stdout
        try:
            sys.stdout = LogRedirector(lambda msg: self.registrar_log_plan(msg))
            
            import Mon_Plan_c_dados_API

            # Preenche as variáveis globais do módulo
            Mon_Plan_c_dados_API.caminho_dados_extrator = dir_extrator
            Mon_Plan_c_dados_API.caminho_dados_api      = dir_api       # <- conferir nome aqui
            Mon_Plan_c_dados_API.caminho_saida          = dir_saida
            Mon_Plan_c_dados_API.nome_arquivo_xlsx      = nome_arquivo_plan
            Mon_Plan_c_dados_API.nome_arquivo_json      = nome_arquivo_json

            Mon_Plan_c_dados_API.executar_consolidacao(
                callback_progresso=lambda atual, total: self.atualizar_progresso_plan(atual, total)
)

            self.registrar_log_plan("Iniciando consolidação de dados...")
            self.registrar_log_plan(f"Diretório de dados do extrator: {dir_extrator}")
            self.registrar_log_plan(f"Diretório de dados da API: {dir_api}")
            self.registrar_log_plan(f"Diretório de saída: {dir_saida}")
            self.registrar_log_plan(f"Arquivo de saída (xlsx): {nome_arquivo_plan}")
            self.registrar_log_plan(f"Arquivo de saída (json): {nome_arquivo_json}")
            self.registrar_log_plan("=" * 60)
            self.progress_plan["value"] = 100
            self.registrar_log_plan("✓ Consolidação de dados concluída com sucesso!")
            self.registrar_log_plan(f"Arquivo salvo em: {os.path.join(dir_saida, nome_arquivo_plan)}")
            self.registrar_log_plan(f"Arquivo salvo em: {os.path.join(dir_saida, nome_arquivo_json)}")
            messagebox.showinfo("Sucesso", "Consolidação de dados finalizada com sucesso!")
        except Exception as e:
            self.registrar_log_plan(f"✗ Erro durante consolidação: {e}")
            self.registrar_log_plan(traceback.format_exc())
            messagebox.showerror("Erro", f"Erro na consolidação:\n{e}")
        
        finally:
            try:
                sys.stdout = old_stdout
            except Exception:
                pass
            self.executando_plan = False
            self.startbtn_plan.config(state=tk.NORMAL)
    
    def registrar_log_plan(self, mensagem):
        """Registra mensagem na área de log do planejador."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logarea_plan.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.logarea_plan.see(tk.END)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = STFExtractorGUI(root)
    root.mainloop()