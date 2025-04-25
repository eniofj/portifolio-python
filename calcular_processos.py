import view as vw
from collections import defaultdict


class Calculos_Processos:
    def __init__(self, categoria,processos=None, dic_medidas={}, tipo_resultado='RESUMIDO', qtd_acop=1, compr_blank=0,
                 esp_peca=0, rendimento_pc=0, qtd_blanks=1):

        self.processos = processos
        self.tp_resultado = tipo_resultado
        self.dic_medidas = dic_medidas
        self.add_medidas = self.adicionar_medidas({'QTD_ACOP':qtd_acop, 'COMPR_BLANK':compr_blank/1000,
                                                   'ESP_PECA':esp_peca, 'RENDIMENTO_PC':rendimento_pc,
                                                   'QTD_BLANK':qtd_blanks})
        self.categoria = categoria



    def adicionar_medidas(self, dic_add_med):
        for i in dic_add_med.items():
            self.dic_medidas[i[0]] = i[1]

        return self.dic_medidas.items()


    def abrir_processos(self):
        # Puxar os temos no banco de dados
        tempos = [vw.tempos_processos(self.categoria, processo.replace(" ","_"))
                  for processo in self.processos]

        # chamar a função para cálculo dos tempos de processos
        calcular_tempos = self.calcular_tempos_processos(tempos)

        return calcular_tempos


    def calcular_tempos_processos(self, tempos):
        # filtrar e substituir os dados de cálculo de tempo para edição
        tempo_final = ([[tempo[0], tempo[1],
                         f'{self.dic_medidas[tempo[4]] * self.dic_medidas[tempo[5]] * tempo[6] /100}']
                       for tempo in tempos])

        # selecionar os processos que fazem parte do cálculo de energia elétrica
        energia = [i for i in tempo_final if i[0][7:-1].isnumeric()]
        # selecionar os processos que fazem parte do cálculo de mão de obra
        mao_obra = [i for i in tempo_final if i[0][7:-1].isnumeric() == False]
        # calcular o tempo total de mão de obra
        tempo_energia = sum([float(tp[2]) for tp in energia])
        # calcular o tempo total de energia elétrica
        tempo_mao_obra = (sum([float(tp[2]) for tp in mao_obra]) + tempo_energia) / 1.67

        # iniciar a lista final com os códigos e valores da soma de energia e mão de obra
        total_tempos = [['CF01.0.0003A', 'ENERGIA', f'{tempo_energia}'],
                        ['MOD1005001A', 'MAO OBRA', f'{tempo_mao_obra}']]

        # juntar as listas com os dados individuais de energia e mão de obra à lista final
        total_tempos += energia
        # chamar a função para editar a lista final conforme tipo de exibição ("RESUMIDA", "COMPLETA")
        tempo_editado = self.unificar_processos(total_tempos) if self.tp_resultado == 'RESUMIDO' else total_tempos + mao_obra
        tempo_editado = [[tp[0], tp[1], f'{float(tp[2])}'] for tp in tempo_editado]

        # pegar os ids dos roteiros correspondentes ao processo selecionado
        roteiro = [vw.filtrar_linha('Roteiro', 'NOME_PROCESSO', item[1].replace("_"," "))[0]
                   for item in tempo_final]

        # converter lista para string para armazenar no banco de dados
        ids_roteiro = "/".join(item.replace("_"," ") for item in roteiro)

        return tempo_editado, ids_roteiro


    def unificar_processos(self, total_tempos):
        agrupados = defaultdict(lambda: [None, None, 0.0, None])

        for codigo, descricao, valor in total_tempos:
            chave = codigo[:-1]  # Considera o código sem o último caractere
            agrupados[chave][0] = codigo  # Mantém o código original com o último caractere
            agrupados[chave][1] = descricao.split('_')[0]  # Pega o primeiro termo da descrição
            agrupados[chave][2] += float(valor)  # Soma os valores

        return [[v[0], v[1], v[2]] for v in agrupados.values()]
        

