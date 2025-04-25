from tkinter import *
from tkinter import Tk, StringVar, ttk, messagebox, Menu
import view as vw
import calcular_mps as calc
import login
import cad_estrutura_protheus as cad_es


class CalulosProMP:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.espessura_MP = ''
        self.entrys = []
        self.dados_calculo = []
        self.dados_adiconais = []

        # self.usuario = 'ENIO' # comentar usuário se habilitar login
        # self.criar_containers() # deixar comentado para habilitar login
        self.criar_tela_login() # deixar descomentado para habilitar login


    def criar_tela_login(self):
        lbl_usuario = self.criar_labels(root, 'USUÁRIO:', [190], 200)
        lbl_SENHA = self.criar_labels(root, 'SENHA:', [190], 250)
        self.usuario = self.criar_entrys(root, None,380, 200, 25, 'normal')
        self.senha = self.criar_entrys(root, None, 380, 250, 25, 'normal', '*')
        btn_logar = self.criar_botoes(root, self.fazer_login, 'Entrar', 380, 300, 20)
        btn_cadastrar = self.criar_botoes(root, self.cadastrar_usuario, 'Cadastrar Usuário',
                                          380, 350, 20)


    def fazer_login(self):
        if self.usuario.get().lstrip() == '' or self.senha.get().lstrip() == '':
            messagebox.showerror('Aviso', 'Preencha os dados corretamente"')
        elif login.validar_login(self.usuario.get().upper(), self.senha.get()):
            self.criar_containers()
            root.title(f'CÁLCULO PPCP - Usuário: {self.usuario.get().upper()}')
        else:
            messagebox.showerror('Login', 'Usuário ou senha incorretos!')


    def cadastrar_usuario(self):
        if self.usuario.get().lstrip() != "" and self.senha.get().lstrip() != "":
            cad = login.cadastrar_usuario(self.usuario.get().upper(), self.senha.get())
            messagebox.showinfo('Aviso', cad[1]) if cad[1] == "Usuário cadastrado com sucesso." \
                else messagebox.showerror('Aviso', cad[1])
        else:
            messagebox.showerror('Aviso', 'Preencha os dados corretamente!')


    def criar_containers(self):
        # Criação dos containers
        altura_containers = [60, 180, 210, 240]  # Largura padrão 1043

        self.containers = [Frame(root, width=1043, height=alt, relief="flat")
                           for alt in altura_containers]

        # Posicionar os containers na tela
        [cont.grid(row=i, column=0, pady=1, padx=0) for i, cont in enumerate(self.containers)]

        # Labels Container_0
        text_lbls_container_0 = ["CAT. PRODUTO", "UNID. MEDIDA", "TIPO PRODUTO"]
        # Acionar a função para criar as Labels
        p_x_c0 = (280, 3)  # valores para calcular o distanciamento entre Labels (posição x do container_0)
        p_y_c0 = 19  # (posição y do container_0)
        [self.criar_labels(self.containers[0], lbl, [i * p_x_c0[0] + p_x_c0[1]], p_y_c0) for i, lbl in
         enumerate(text_lbls_container_0)]

        # OptionMenu categoria Armazena o item selecionado no option_menu de categorias
        self.var_categoria = StringVar(root)
        # Puxar categorias no BD
        lista_categorias = [i[0] for i in vw.ver_form('categoria_produtos')]
        # Chamar a função para criar o OptionMenu de categorias
        self.criar_opt_list(self.containers[0], self.var_categoria, lista_categorias, self.selec_categoria, 170, 15)
        # Iniciar pelo primeiro item da lista_categorias
        self.categoria = lista_categorias[0]

        # OptionMenu unidade
        self.var_unidade = StringVar(root)
        lista_unidades = ['PC', 'MT', 'M2']
        # Chamar a função para criar o OptionMenu de unidades
        self.criar_opt_list(self.containers[0], self.var_unidade, lista_unidades, self.selec_unidade, 450, 15)
        # Iniciar pelo primeiro item da lista_unidades
        self.unidade = lista_unidades[0]

        # Labels dos títulos dos containers
        lbl_titulos = {'DIMENSIONAIS :': (self.containers[1], [30], 0, 'w'),
                       'PROCESSOS :': (self.containers[2], [40], 0, 'w'),
                       'RESULTADOS :': (self.containers[3], [10], 3, 'center'),
                       'INFORME O PA :': (self.containers[3], [380], 3, 'center')
                       }
        # Chamar a função para criar as labels dos títulos
        [self.criar_labels(lbl[1][0], lbl[0], lbl[1][1], lbl[1][2], lbl[1][3]) for lbl in lbl_titulos.items()]

        # OptionMenu Opçao de exibição dos resultados no container_3
        self.var_exib_resultado = StringVar(root)
        lista_opcao_resultado = ['RESUMIDO', 'COMPLETO']
        self.criar_opt_list(self.containers[3], self.var_exib_resultado, lista_opcao_resultado,
                            self.selec_opcao_resultado, 150, 0)

        # Botões do container_3
        botoes = {'CALCULAR': (self.containers[3], self.calcular, 290, 0),
                  'SALVAR': (self.containers[3], self.salvar_codigo, 675, 0),
                  'CAD.PROTHEUS': (self.containers[3], self.formulario_cadastros, 780, 0)
                  }
        # Chamar a função para criação dos botões do container_3
        [self.criar_botoes(btn[1][0], btn[1][1], btn[0], btn[1][2], btn[1][3]) for btn in botoes.items()]

        # chamar função para criar a entry para cadastro do codigo_produto
        self.entry_codigo = self.criar_entrys(self.containers[3], 'codigo_pa', 520, 2)
        self.gerar_menu()


    def gerar_menu(self):
        menubar = Menu(root)
        filemenu = Menu(menubar)

        menubar.add_cascade(label="Arquivo", menu=filemenu)
        filemenu.add_command(label="Logout", command=self.deslogar)
        filemenu.add_command(label="Fechar", command= self.fechar)

        root.config(menu=menubar)


    def criar_labels(self, container, text_lbls, pos_x, pos_y, alihamento='e', larg=20):
        # cria a label e posiciona no container informado
        lbl = Label(container,text=text_lbls, font=self.fontePadrao, width=larg, anchor=alihamento)
        lbl.place(x=pos_x[0], y=pos_y)


    def criar_opt_list(self, container, var_opt, lista_opcoes, command, p_x, p_y, w=130):
        # criar a OptionMenus e posiciona nos containers informados
        lista_opcoes.insert(0, lista_opcoes[0])
        if container:
            self.opt_categoria = ttk.OptionMenu(container, var_opt, *lista_opcoes, command=command)
            self.opt_categoria.place(x=p_x, y=p_y, height = 30, width=w)
        else:
            self.opt_categoria()


        command(lista_opcoes[0])


    def criar_entrys(self, container=None, nome=None, pos_x=0, pos_y=0, larg=25, state='normal', show=None):
        """Cria um campo Entry e o posiciona no container informado."""
        entry = Entry(container, width=larg, justify='left', relief="solid", name=nome, state=state, show=show)
        entry.place(x=pos_x, y=pos_y, height=22)
        return entry


    def criar_checkbox(self, opcao):
        """Cria os checkboxs dos processos correspondente a categoria do produto no container informado."""
        processos = vw.filtrar_linha('processos_produtivos','CATEGORIA', opcao)

        # Apaga os textos dos checkbox a cada seleção de categoria
        self.limpar_checkbox()

        # Variável checkbox processos
        self.v_processos = dict([(p,IntVar()) for p in processos])
        # Checkbox processos
        self.ch_processos = [Checkbutton(self.containers[2], text=cb, variable=self.v_processos[cb],anchor='se')
                             for cb in processos[1:]]

        # Colocar os Checkbuttons na tela,
        pos_x, pos_y = 60, 60
        for i, c in enumerate(self.ch_processos):
            c.place(x=pos_x, y=pos_y)
            pos_x += 200
            if (i + 1) % 4 == 0:  # Muda de linha a cada 4 elementos
                pos_x = 60
                pos_y += 30


    def criar_botoes(self, container, comando, texto, pos_x, pos_y, larg=13):
        # criar a Botoões e posicionar nos containers informados
        texto = texto.replace("De","+").replace("Ate","+")
        button = Button(container, command=comando, text=texto, width=larg)
        button.place(x=pos_x, y=pos_y)


    def fechar(self):
        # Encerrar programa
        root.destroy()


    def deslogar(self):
        # Encerrar sessão e retornar para tela de login
        [self.containers[i].grid_forget() for i in range(0,4)]
        self.senha.delete(0, 'end')
        self.usuario.delete(0,'end')
        self.usuario.focus_set()
        root.title(f'CÁLCULO PPCP')


    def limpar_checkbox(self):
        # Posições verticais das labels
        posicoes_y = [60, 90, 120, 150]

        for pos_y in posicoes_y:
            Label(self.containers[2], text=" " * 190, font=self.fontePadrao).place(x=60, y=pos_y)


    def selec_categoria(self, opcao):
        # Seleciona a categoria e pela seleção chama a função para criar o OptionMenu tp_produtos
        self.categoria = opcao
        lista_tp_produtos = [i[1:] for i in vw.ver_form('categoria_produtos') if i[0] == self.categoria][0]
        self.var_tp_produto = StringVar(root)
        self.criar_opt_list(self.containers[0], self.var_tp_produto, lista_tp_produtos, self.selec_tp_produto, 740, 15)
        self.tipo_produto = lista_tp_produtos[0]
        self.criar_checkbox(opcao)
        self.limpar_inputs()

        return opcao


    def selec_tp_produto(self, opcao):
        # retorna o tipo de produto selecionado no OptionMenu
        # chamar a função para puxar os dados_entrada correpondente ao tp_produto
        self.selec_dados_entrada(opcao)
        self.dados_calculo = {'categoria': self.categoria, 'tipo_produto': opcao}
        # determinar valor e desabilitar entry de acordo com tipo_produto selecionado
        self.desabilitar_entry('disabled', '700') if opcao == 'TNT' else self.desabilitar_entry('normal', '')

        return opcao


    def selec_unidade(self, opcao):
        # retorna a unidade de medida selecionada no OptionMenu
        return opcao


    def selec_opcao_resultado(self, opcao):
        # retorna a opção de resultado selecionada no OptionMenu
        entrys = [i for i in self.entrys if i.get()]
        self.calcular() if len(entrys) > 0 else False
        return opcao


    def selec_dados_entrada(self, opcao):
        """Seleciona os dados de entrada com base no tipo de produto escolhido."""
        # Posições (x, y) das labels no container_1
        pos_lbls_c1 = [(100, 50), (100, 80), (100, 110), (450, 50), (450, 80), (450, 110), (450, 140)]

        # Limpar labels e entrys existentes no container_1
        self.limpar_labels_entrada(pos_lbls_c1)
        self.limpar_entrys_entrada()

        # Buscar nomes dos campos das medidas de entrada no banco de dados
        self.dados_entrada = vw.ver_form('medidas_entrada')
        entradas = [i for i in self.dados_entrada if i[0] == self.categoria and i[1] == opcao][0]

        # Criar labels no container_1
        for i, txt in enumerate(entradas[2:]):
            self.criar_labels(self.containers[1], f'{txt} :', [pos_lbls_c1[i][0]], pos_lbls_c1[i][1])

        # Criar entrys no container_1 e armazená-las na lista self.entrys
        for i, v in enumerate(entradas[2:]):
            nome = v.replace(' ', '_').replace('Ç', 'C').replace('.', '').replace('/', '_').lower()
            entry = self.criar_entrys(self.containers[1], nome, pos_lbls_c1[i][0] + 180, pos_lbls_c1[i][1])
            self.entrys.append(entry)


    def limpar_entrys_entrada(self):
        """Remove todas as Entry criadas na tela."""
        for entry in self.entrys:
            entry.destroy()
        self.entrys.clear()
        self.treev_resultado(self.containers[3], [],[],[])


    def desabilitar_entry(self, state, valor):
        self.entrys[4].insert(0, valor) if valor != "" else self.entrys[4].delete(0,'end')
        self.entrys[4]['state'] = state


    def limpar_labels_entrada(self, pos_lbls_c1):
        # limpar as Labels a cada seleção de tp_produto
        [self.criar_labels(self.containers[1], "", [i[0]], i[1]) for i in pos_lbls_c1]


    def calcular(self):
        ## realizar os cálculos para cada produto
        proc_validos = [i[0] for i in self.v_processos.items() if i[1].get() == 1]
        self.dados_calculo['processos'] = proc_validos

        # armazenar o nome das entrys do container_1 que não estiverem preenchidos corretamente
        en_falsas = [entry.winfo_name().upper().replace("_"," ")
                     for entry in self.entrys if not entry.get().strip()]# or entry.get().isnumeric() == False]

        # informar ao usuário as entrys preenchidas incorretamente, se não houver seguir para o cálculo
        if len(en_falsas) > 0:
            messagebox.showerror("Erro", "VERIFICAR O(S) CAMPO(S):\n\n" + "\n".join(en_falsas))
        elif len(proc_validos) == 0:
            messagebox.showerror("Erro", "Selecione os processos!")
        else:
            for i in self.entrys:

                self.dados_calculo[i.winfo_name()] = i.get().replace(",",".")
            self.dados_calculo['tp_resultado'] = self.var_exib_resultado.get()

            dados_filtrados = {
                k.replace("bobina", "placa"): float(v) if isinstance(v, str) and v.replace('.', '', 1).isdigit() else v
                for k, v in self.dados_calculo.items()
            }

            try:
                executar = calc.Calculos(**dados_filtrados)
                calculo = executar.calculo_mps_final
                self.calcl_final = calculo[0]
                # pegar os ids do roteiro
                self.ids_roteiro = calculo[1]
            except:
                messagebox.showerror('ERRO', 'Erro ao calcular, dados imcompatívels com'
                                             'as MPs cadastradas no banco de dados!')


            try:
                self.calcl_final = self.formatar_cod_processos(self.calcl_final)

                # parâmetros para exibição do resultado na interface principal
                colunas = ['CÓD. PROCESSO', 'PROCESSO', 'TEMPO', 'CÓD. MP', 'MP', 'QTD. MP', 'CUSTO', 'RENDIMENTO']
                tam_colunas = [80, 180, 55, 130, 130, 100, 70, 70]
                # chamar função para exibição dos resultados na interface principal
                self.treev_resultado(self.containers[3], self.calcl_final, colunas, tam_colunas)
            except:
                return

    def salvar_codigo(self):

        # try:
        import gravar_calculo

        # dados do roteiro para preenchimento da máscara (
        dados_desc_roteiro = [self.usuario.get().upper(), self.entrys[3].get(), self.entrys[4].get(), self.entrys[2].get(),
                              self.entrys[-1].get(), self.var_tp_produto.get(), self.entrys[-1].get(),
                              self.var_unidade.get(), self.calcl_final[0][-1].split(" / ")[0]]

        if self.validar_codigo_PA():
            gravar = gravar_calculo.Calculos_Processos(self.calcl_final, self.var_unidade.get(),
                                                       self.entry_codigo.get(), self.ids_roteiro,
                                                       dados_desc_roteiro)
            gravar.gravar_dados_estrutura()
            messagebox.showinfo('Concluído', 'Cálculo gravado com sucesso!')
        else:
            messagebox.showerror('ERRO','INFORME UM CÓDIGO VÁLIDO\n\n'
                                        'Exemplo: PA01.1.0001')
        # except:
        #     pass


    def limpar_inputs(self):
        # limpar os dados digitados nas entrys
        [i.delete(0,'end') for i in self.entrys]


    def validar_codigo_PA(self):
        codigo = self.entry_codigo.get()
        if len(codigo) == 11:
            if codigo[0:2] != 'PA' or codigo[4] != '.' or codigo[6] != '.':
                return False
            else:
                return True
        else:
            return False


    def formatar_cod_processos(self, calc_final):
        # eliminar o último caracter de cada código para exibição na treev
        for i in calc_final:
            i[0] = i[0][:-1]
            i[2] = f'{float(i[2]):.6f}'
            try:
                i[5] = f'{i[5]:.6f}'
            except:
                pass
        return calc_final


    def formulario_cadastros(self):
        # abrir formulário de códigos cadastrados
        self.form_window = Toplevel()
        self.form_window.title(f"Códigos Cadastrados")
        self.form_window.geometry("670x300")


        # Criar Labels e entrys do self.form_window padrão_dicionários '''dic = {texto/nome:[p_x, p_y, width]}'''
        dic_labels_form = {'Buscar Codigo:':[0,10, 15], 'Mudar Status: ':[350, 10, 15],
                           'DO PA:':[170,50,8], 'ATÉ PA:':[360,50,8]}
        dic_entrys_form = {'buscar:':[ 130, 10, 12, 'normal'], 'de:':[240, 50, 12, 'disabled'],
                           'ate:':[430, 50, 12, 'disabled']}

        # chamar a função para criar opt_list para definição do status do cadastro
        v_status = StringVar(root)
        self.criar_opt_list(self.form_window, v_status, [" ", "S", "N"],
                            self.status_cadastro, 490, 7, 50 )
        # chamar a função para criar opt_list para selecionar tipo de cadastro (estrurua ou roteiro)
        self.v_tp_cadastro = StringVar(root)
        self.criar_opt_list(self.form_window, self.v_tp_cadastro, ["Selec. tipo cadastro","Cadastrar Estrutura",
                                                                   "Cadastrar Roteiro"],
                            self.tp_cadastro, 14, 47, 150) #[14, 50, 17]

        # Chamar função para criar labels do self.form_window
        [self.criar_labels(self.form_window, lb[0], [lb[1][0]], lb[1][1], larg=lb[1][2]) for lb in dic_labels_form.items()]
        # Chamar função para criar entrys do self.form_window
        self.entrys_form = [self.criar_entrys(self.form_window, en[0], en[1][0], en[1][1],
                                              en[1][2], en[1][3]) for en in dic_entrys_form.items()]
        # Parâmetros dos botões do self.form_window
        lista_botoes = {'Buscar':[self.buscar_codigo, 210, 8, 7] , 'Cad. Protheus':[self.cad_protheus, 550, 48, 13],
                        'De':[self.add_do_codigo, 320, 48, 3], 'Ate':[self.add_ate_codigo, 510, 48, 3],
                        'Excluir':[self.excluir_registro, 280, 8, 7]}
        # Chamar função para criar os botões do self.form_window
        self.btn_form = [self.criar_botoes(self.form_window, btn[1][0], btn[0], btn[1][1],
                                           btn[1][2], btn[1][3]) for btn in lista_botoes.items()]

        self.exibir_cadastrados()


    def tp_cadastro(self, opcao):
        return opcao


    def status_cadastro(self, opcao):
        # Mudar o status do registro para cadastrado (S/N) no banco de dados para liberar o cadastro no Protheus
        try:
            cod_produto = None if opcao == " " else self.linha_selecionada[0]

            if cod_produto:
                status = {'S':'"S" - Item já cadastrado no Protheus', 'N':'"N" - Item não cadastrado no Protheus'}

                if vw.verificar_usuario(self.usuario.get().upper(), self.linha_selecionada[0]):

                    vw.atualizar_tabela('Estrutura', 'CADASTRADO', 'CODIGO', opcao, cod_produto)
                    self.exibir_cadastrados()
                    messagebox.showinfo('Concluído', f'Status do item {cod_produto} '
                                                     f'alterado para:\n {status[opcao]}')
                else:
                    messagebox.showerror('Bloqueado', 'Usuário sem permissão para alteração desse item!')
        except:
            pass

    def exibir_cadastrados(self):
        # Exibir os códigos cadastrados na treev da form_window
        # Parâmetros para exibição dos PAs cadastrads no self.form_window
        self.colunas_form = vw.nome_colunas('estrutura')#[:-2]
        self.produtos_form = vw.ver_form('estrutura')#[:-2]
        self.tam_col_form = [30, 20, 120, 30, 50, 50, 50,50]
        # Chamar a função para exibir os produtos cadastrados no self.form_window
        self.treev_resultado(self.form_window, self.produtos_form, self.colunas_form, self.tam_col_form,
                             15, 100, 180, 640)


    def buscar_codigo(self):
        # Filtrar item na tabela estrutura
        if self.entrys_form[0].get() != "":
            lista_filtro = vw.filtrar_linha('estrutura', 'CODIGO', self.entrys_form[0].get().upper())
            # lista_filtro = self.ordenar_lista(lista_filtro)
            self.treev_resultado(self.form_window, [lista_filtro], self.colunas_form, self.tam_col_form,
                             15, 100, 180, 630)
        else:
            # Campo buscar vazio reexibe a lista com todos PAs cadastrados
            self.exibir_cadastrados()


    def excluir_registro(self):
        try:
            codigo = self.linha_selecionada[0]
            if self.linha_selecionada[0]:
                if vw.verificar_usuario(self.usuario.get().upper(), codigo):
                    conf = messagebox.askyesno('Confirmar', f'Confirma a exclusão do {codigo}?')
                    vw.deletar_form('estrutura', 'codigo', [codigo]) if conf else False
                    self.exibir_cadastrados()
                else:
                    messagebox.showerror('Bloqueado', 'Usuário sem permissão para exclusão desse registro!')
        except:
            messagebox.showinfo('Aviso', 'Selecione o registro a ser excluído!')


    def add_do_codigo(self):
        try:
            if self.linha_selecionada[0]:
                self.entrys_form[1]['state'] = 'normal'
                self.entrys_form[2]['state'] = 'normal'
                self.entrys_form[2].delete(0,'end')
                self.entrys_form[1].delete(0,'end')
                self.entrys_form[1].insert(0, self.linha_selecionada[0])
                self.entrys_form[1]['state'] = 'disabled'
                self.entrys_form[2]['state'] = 'disabled'
        except:
            pass


    def add_ate_codigo(self):
        if self.entrys_form[1].get():
            if self.linha_selecionada[0] >= self.entrys_form[1].get():
                self.entrys_form[2]['state'] = 'normal'
                self.entrys_form[2].delete(0, 'end')
                self.entrys_form[2].insert(0, self.linha_selecionada[0])
                self.entrys_form[2]['state'] = 'disabled'
            else:
                messagebox.showinfo('Atenção', 'O Código final não pode ser menor que o Código inicial!')


    def cad_protheus(self):
        # Pegar os código (inicial e final) e fazer a filtragem no banco de dados
        if self.entrys_form[1].get() and self.entrys_form[2].get():
            lista_produtos = vw.filtrar_conjunto('ESTRUTURA', 'CODIGO',
                                self.entrys_form[1].get(), self.entrys_form[2].get())

            # manter na lista somente os códigos que ainda não estejam cadastrados no Protheus
            self.lista_produtos = [lista for lista in lista_produtos if lista[3] == 'N']

            if len(self.lista_produtos) > 0:
                conf = messagebox.askyesno('Aviso', f'Abra o Protheus no módulo '
                                                    f'"{self.v_tp_cadastro.get().split(" ")[1].upper()}",'
                                                    'o processo iniciará automaticamente.')
                if conf:
                    # obter o nome do módulo e converter para o nome da função correspondente
                        ## cadastrar_estrutura ou cadastrar_roteiro
                    modulo = self.v_tp_cadastro.get().lower().replace(' ', '_')
                    # chamar a função a partir do nome do módulo
                    try:
                        getattr(self, modulo)()
                    except:
                        messagebox.showinfo('Aviso', 'Selecione o tipo de cadastro ("Cadastro Estrutura, '
                                                     'Cadastro Roteiro')
                else:
                    return
            else:
                messagebox.showinfo('Aviso', 'Código(s) selecionado(s) possuem status "S" de já '
                                             'cadastrado(s)!')
        else:
            messagebox.showinfo('AVISO', 'Adicione os códigos nos campos "DO PA" e "ATÉ PA:')


    def cadastrar_estrutura(self):
        # Função para cadastramento da Estrutura no Protheus
        try:
            [cad_es.cadastrar_estrutura(i) for i in self.lista_produtos]
            messagebox.showinfo('Finalizado', 'Cadastro realizado com sucesso no Protheus')
        except:
            messagebox.showerror('Erro','Não foi possível concluir o cadastro no Protheus!')
            return


    def cadastrar_roteiro(self):
        # Função para cadastramento do Roteiro no Protheus
        try:
            import cad_roteiro
            produtos = [[i[0], i[-2].split("/")] for i in self.lista_produtos]
            cad_roteiro.abrir_roteiro(produtos)
            messagebox.showinfo('Finalizado', 'Cadastro realizado com sucesso no Protheus')
        except:
            messagebox.showerror('Erro','Não foi possível concluir o cadastro no Protheus!')
            return


    def treev_resultado(self, container, lista_resultados, colunas, tam_colunas,
                        pos_x=15, pos_y=30, alt=150, larg=860):
        # Configurações iniciais
        alinhamento = "center"

        # Criar Treeview com barras de rolagem
        # Alteramos o selectmode para 'browse' para permitir seleção de uma linha
        tree = ttk.Treeview(container, selectmode="browse", columns=colunas, show="headings")
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.place(x=pos_x, y=pos_y, height=alt, width=larg)

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        vsb.place(x=larg+10, y=pos_y, height=alt, width=25)

        # Configurar cabeçalhos e colunas
        for col, largura in zip(colunas, tam_colunas):
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=largura, anchor=alinhamento)

        # Inserir os resultados na Treeview
        for item in lista_resultados:
            tree.insert('', 'end', values=item)

        # Função para capturar a linha selecionada
        def item_selecionado(event):
            # Obtém os itens selecionados (nesse caso, apenas um)
            for item_id in tree.selection():
                item = tree.item(item_id)
                self.linha_selecionada = item['values']

        # Vincula o evento de seleção à função criada
        tree.bind("<<TreeviewSelect>>", item_selecionado)

        # Retorne a treeview se precisar usá-la fora da função
        return tree


# Criando a Janela
root = Tk()
root.title(f'CÁLCULO PPCP')
root.geometry('900x650')
CalulosProMP(root)
root.mainloop()