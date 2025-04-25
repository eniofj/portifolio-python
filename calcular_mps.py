import view as vw
from collections import defaultdict
import math
import calcular_processos  as calc

class Calculos:
    def __init__(self, categoria='', tipo_produto='', processos=None, comprimento_pc=0, largura_pc=0,
                 espessura_pc=0, comprimento_placa=0, largura_placa=0, espessura_base=0, qtde_pc_batida=1,
                 larg_tampao=0, larg_corte_blank=0, densidade_mínima=0, densidade_máxima=0, tp_resultado='RESUMIDO'):

        self.categoria = categoria
        self.tipo_produto = tipo_produto
        self.compr_peca = comprimento_pc
        self.larg_peca = largura_pc
        self.esp_peca = espessura_pc if tipo_produto != 'PLACUSTIC PERFILADO' else espessura_pc + espessura_base
        self.compr_blank = comprimento_placa
        self.larg_blank = largura_placa
        self.base_peca = espessura_base
        self.qtd_peca_batida = qtde_pc_batida
        self.larg_tampao = larg_tampao
        self.larg_corte_blank = larg_corte_blank
        self.dens_min = densidade_mínima
        self.dens_max = densidade_máxima
        self.tipo_resultado = tp_resultado
        self.lista_materias_primas = []
        self.processos = processos if processos is not None else []
        self.rendimento = getattr(self, f"rendimento_{self.categoria.lower()}", lambda: "Método não encontrado")()
        self.calculo_mps_final = self.calcular_custo_mp()
        self.qtd_acoplagem = 0
        self.qtd_blank = 1


    def calcular_rendimento(self, larg_blank, larg_peca, perca=0, compr_blank=1, compr_peca=1):
        # calcula o rendimento de peças e/ou barras pelo dimensional do blank
        rendimento = ((larg_blank - perca) / larg_peca) * (compr_blank / compr_peca)
        rendimento = math.trunc(rendimento) if self.categoria != 'PERFIFLEX' else rendimento
        rendimento_mts = rendimento * self.compr_peca * 0.001

        return  [rendimento, rendimento_mts]


    def rendimento_perfiflex(self):
        # Calcula o rendimento para tipo_produto "PERFIFLEX"

        # Chamar função para calcular largura_barra_blank
        larg_barra_blank = self.larg_barra_blank_perfiflex()
        # Definir a perca
        perca = self.larg_peca if self.tipo_produto == 'TAMPAO' else 20
        # Calcular rendimento em barras_blank (pegar resultado em peça somente)
        rendimento = self.calcular_rendimento(self.larg_blank, larg_barra_blank, perca)[0]
        # Calcula o número de barras inteiras que cabem na placa
        qtd_pecas_inteiras = rendimento // 1 * self.qtd_peca_batida
        # Calcula a sobra da placa após cortar as barras inteiras
        larg_sobra = rendimento % 1 * larg_barra_blank
        # Define o múltiplicador (mult = 2 se inferior acima de 1 pç/batida, senão mult = 1)
        mult = 2 if self.qtd_peca_batida > 1 and self.tipo_produto == 'INFERIOR' else 1
        # calcula o rendimento de peças da sobra da placa
        rend_sobra = larg_sobra / (larg_barra_blank / self.qtd_peca_batida * mult) // 1 * mult
        # adiciona o resultado do rend_sobra à quantidade final de peças
        qtd_pecas_inteiras += rend_sobra
        qtd_mts = qtd_pecas_inteiras * self.compr_peca * 0.001
        # chamar a função para calcular as MPs complementares
        self.calc_produtos_intermediarios(qtd_pecas_inteiras)
        # calcular a quantidade total de blanks
        self.qtd_blank = math.ceil(qtd_pecas_inteiras / self.qtd_peca_batida)

        return qtd_pecas_inteiras, qtd_mts


    def larg_barra_blank_perfiflex(self):
        # calcula a largura_barra_blank para itens da categoria PERFIFLEX
        if self.tipo_produto == "INFERIOR" and self.qtd_peca_batida > 1:
            return (self.base_peca * 2 + self.larg_peca) * self.qtd_peca_batida / 2
        if self.tipo_produto == "BARRA":
            return self.larg_peca
        if self.tipo_produto == "TAMPAO":
            return self.larg_tampao
        if self.tipo_produto == "ZIPADO":
            return self.larg_corte_blank
        if (self.tipo_produto == "SUPERIOR" or self.tipo_produto == "INFERIOR") and self.qtd_peca_batida == 1:
            return self.larg_peca + self.base_peca
        else:
            return (self.larg_peca + self.base_peca )* self.qtd_peca_batida


    def calc_ade_perfiflex(self, QTD_MULT_MP, rendimento):
        qtd_adesivagem = QTD_MULT_MP *( self.esp_peca/ 1000) * (self.compr_peca / 1000) *rendimento
        return qtd_adesivagem



    def rendimento_fitas(self):
        # calcula o rendimento para tipo_produto "FITAS"
        rendimento = self.calcular_rendimento(self.larg_blank, self.larg_peca, 60)
        # chamar a finção para calcular as MPs complementares
        self.calc_produtos_intermediarios(rendimento[1])

        return rendimento


    def rendimento_impregnados(self):
        # calcula o rendimento para tipo_produto "IMPREGNADOS"
        rendimento = self.calcular_rendimento(self.larg_blank, self.larg_peca, compr_blank=self.compr_blank,
                                                 compr_peca=self.compr_peca)
        # chamar a finção para calcular as MPs complementares
        self.calc_produtos_intermediarios(rendimento[0])
        # calcular mp complementar para fórmulas impregnantes
        self.calc_formulas_impregantes()

        return rendimento


    def rendimento_espumas(self):
        # calcula o rendimento para tipo_produto "ESPUMAS"
        rendimento = self.calcular_rendimento(self.larg_blank, self.larg_peca, compr_blank=self.compr_blank,
                                              compr_peca=self.compr_peca)
        rendimento[0] = rendimento[0] * 2 if self.tipo_produto == 'PLACUSTIC PERFILADO' else rendimento[0]
        # calcular unidade MP para espuma com viscomix
        self.calc_mp_unidade('MT')
        # chamar a finção para calcular as MPs complementares
        self.calc_produtos_intermediarios(rendimento[0])

        return rendimento


    def calc_mp_unidade(self, opcao=None):
        # Calcula a quantidade de PI (MP complementar) pela unidade de medida
        dic_tp_produto = {'M2_LAT_PC':(self.compr_peca + self.larg_peca) * 2 * self.esp_peca / 1000000,
                          'M2_PC':self.compr_peca * self.larg_peca / 1000000,
                          'M2':self.compr_blank * self.larg_blank / 1000000,
                          'M3':self.compr_blank * self.larg_blank * self.esp_peca / 1000000000,
                          'MT':self.compr_blank / 1000,
                          'MT_div_2':self.compr_blank / 1000 / 2,
                          'UN':1}

        return dic_tp_produto[opcao] if opcao else dic_tp_produto


    def calc_produtos_intermediarios(self, rendimento):
        # Calcula a quanitdade de PI (MP complementar) a partir do processo produtivo correspondente
        for i in self.processos:
            # Filtrar os registros correspondentes ao processo informado

            PI = vw.filtrar_linha('calculo_MPS', 'CHAVE', i)
            if i in PI:
                # calcular a quantidade de PI se o registro for encontrado no BD
                if i not in ('ADESIVAGEM BASE', 'ADESIVAGEM TRAPEZIO'):
                    if PI[5] == 'RENDIMENTO':
                            qtd_PI = rendimento
                    else:
                        qtd_PI = PI[4] * self.calc_mp_unidade(PI[5])
                else:
                    qtd_PI = self.calc_ade_perfiflex(PI[4], rendimento)

                # calcular a custo do PI se o registro for encontrado no BD
                custo_PI = PI[3] * qtd_PI
                # incluir resultado(s) na lista de produtos intermediários
                self.lista_materias_primas.append([PI[1], PI[2], qtd_PI, custo_PI])
                # incluir mp_base na lista de mps

        self.calc_mp_base(rendimento)

    def calc_formulas_impregantes(self):
        peso = self.calc_peso_impregnacao()[2]
        formula = vw.filtrar_linha('calculo_MPS', 'CHAVE', self.tipo_produto)
        self.lista_materias_primas.append([formula[1], formula[2], peso, peso * formula[3]])


    def calc_peso_impregnacao(self):
        constante_espuma = self.compr_blank * self.larg_blank * self.esp_peca/ 1000000
        peso_secoMin = constante_espuma * self.dens_min
        peso_secoMax = constante_espuma * self.dens_max
        peso_umidoMin = peso_secoMin * 3.04  # 3.04 = constante padrão
        peso_umidoMax = peso_secoMax * 3.04  # 3.04 = constante padrão
        peso_espuma = constante_espuma / 1000 * 18  # 18 = densidade da espuma
        peso_espuma = peso_espuma + (peso_espuma * 0.3) if 'TRATAMENTO' in self.processos else peso_espuma
        total_FM = (peso_umidoMax / 1000) - peso_espuma
        total_FM = total_FM + (total_FM * 0.80) if self.tipo_produto == 'FM4.9.04.34' else total_FM
        # nome_fm = [n for n in dic_fm.keys() if n == self.tipo][0]

        return peso_umidoMin, peso_umidoMax, total_FM


    def calc_mp_base(self, rendimento):
        # calcular mp_base para categorias ESPUMAS e IMPREGNADOS
        if self.categoria in ('ESPUMAS', 'IMPREGNADOS'):
            tp_mp = [['BLOCO_PU_D16', None] if self.esp_peca != 10.0 else ['PU_10', None]]

        # calcular mp_base para categoria FITAS
        elif self.categoria == 'FITAS':
            tp_mp = self.selec_mp_fita()[0]

        # calcular mp_base para categoria PERFIFLEX
        else:
            tp_mp = self.combinar_pee_espessuras()

        # Puxar dados da mp_base no BD
        mp_base = [vw.filtrar_linha('calculo_MPS', 'CHAVE', i[0]) for i in tp_mp]

        # multiplicar m2 PEE conforme quantidade de camadas
        if "PEE" in tp_mp[0][0]:
            # pegar dados da lista mp_base
            for i,v in enumerate(mp_base):
                # multiplicar com a qtd camadas informada na lista tp_mp
                v[4] *= tp_mp[i][1]


        # Incluir MPS_base na lista_materias_primas (alguns tipos de produtos podem ter mais de 1 mp_base)
        for i in mp_base:
            # calcular a quantidade de MP
            qtd_mp = i[4] * self.calc_mp_unidade(i[5]) if i[5] != 'RENDIMENTO' else i[4] * rendimento
            # calcular a custo da MP
            custo_mp = i[3] * qtd_mp

            self.lista_materias_primas.append([i[1], i[2], qtd_mp, custo_mp])


    def selec_mp_fita(self):
        # verificar a espessura e calcular a quantidade da MP_principal para tipo_produto FITAS
        dic_mp_fita = {'F.FACIL':self.combinar_pee_espessuras(),
                       'PEE':self.combinar_pee_espessuras(),
                       'EVA':[[f'EVA{self.esp_peca}', self.calc_mp_unidade('M2')]],
                       'TNT':[['TNT1.0', self.calc_mp_unidade('MT_div_2')]],
                       'TECHFOAM':[[f'TECHFOAM{self.esp_peca}', self.calc_mp_unidade('M2')]]}

        return [dic_mp_fita[self.tipo_produto]]


    def combinar_pee_espessuras(self):
        espessuras = [10.0, 3.0]  # Prioridade para a maior espessura

        # Verifica se alguma das espessuras é múltipla exata e prioriza a maior
        for e in espessuras:
            if self.esp_peca % e == 0:
                calculo = [[f"PEE{e}", int(self.esp_peca / e)]]
                self.qtd_acoplagem = int(self.esp_peca / e) - 1
                return calculo

        # Caso contrário, calcula a melhor combinação
        qtd_pee10, restante = divmod(self.esp_peca, 10.0)
        calculo = ([[f"PEE10.0", int(qtd_pee10)]] + [[f"PEE3.0", int(restante / 3.0)]]
                   if restante % 3.0 == 0 else [["PEE3.0", int(round(self.esp_peca / 3.0))]])

        # Calcular a quantidade de acoplagem
        self.qtd_acoplagem = sum([i[1] for i in calculo]) - 1

        return calculo


    def calcular_custo_mp(self):
        # unificar PIs de mesmo código e somar resultados
        dados_unificados = defaultdict(lambda: [None, 0, 0])

        for chave, descricao, valor1, valor2 in self.lista_materias_primas:
            if dados_unificados[chave][0] is None:
                dados_unificados[chave][0] = descricao.split()[0]
            dados_unificados[chave][1] += valor1
            dados_unificados[chave][2] += valor2

        lista_mps_editada = [[chave, *valores] for chave, valores in dados_unificados.items()]
        soma_valor_total = sum(valores[2] for valores in dados_unificados.values())
        custo_final= {'PC':soma_valor_total / self.rendimento[0],
                      'MT':soma_valor_total / self.rendimento[1]}

        resultado = self.editar_resultado(lista_mps_editada, custo_final)
        return resultado


    def editar_resultado(self, lista_mps_editada, custo_final):
        # editar resultado final para exibição na interface
        processos = self.calc_tp_processos()

        lista_mps = [i[:-1] for i in lista_mps_editada]
        lista_mps[0].append(f"R$ {custo_final['PC']:.2f} / PÇ")
        lista_mps[0].append(f"{self.rendimento[0]:.2f} / PÇS")

        if len(lista_mps)>=2:
            lista_mps[1].append(f"R$ {custo_final['MT']:.2f} / MT")
        else:
            lista_mps.append(["", "", "", f"R$ {custo_final['MT']:.2f} / MT"])
        lista_mps[1].append(f"{self.rendimento[1]:.2f} / MTS")

        lista_final = []


        for i, proc in enumerate(processos[0]):
            try:
                lista_final.append(proc + lista_mps[i])
            except:
                lista_final.append(proc)

        ## formatar a quantidade das MPs para :.6f

        return lista_final, processos[1]


    def calc_tp_processos(self):
        self.qtd_blank = 1 if self.categoria != 'PERFIFLEX' else self.qtd_blank
        self.qtd_acoplagem = 1 if self.categoria not in ('PERFIFLEX', 'FITAS') else self.qtd_acoplagem

        executar = calc.Calculos_Processos(self.categoria,self.processos, self.calc_mp_unidade(),
                                           self.tipo_resultado, self.qtd_acoplagem, self.compr_blank,
                                           self.esp_peca, self.rendimento[0], self.qtd_blank)

        tempo_processos = executar.abrir_processos()

        return tempo_processos






