from datetime import datetime
import view as vw

class Calculos_Processos:
    def __init__(self, dados_calculo, unidade_medida, codigo, ids_roteiro, dados_roteiro):
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.lista_final = [codigo, "N", self.data]
        self.dados_calculo = dados_calculo
        self.unidade_medida = unidade_medida
        self.ids_roteiro = ids_roteiro
        self.dados_roteiro = dados_roteiro


    def gravar_dados_estrutura(self):
        dados = self.formatar_dados_estrutura()
        vw.inserir_form('estrutura', [self.lista_final])



    def formatar_dados_estrutura(self):
        componentes = []
        dic_un = {'PC':0, 'MT':1}

        self.lista_final.insert(1, self.dados_calculo[dic_un[self.unidade_medida]][-1].split("/")[0].strip())
        self.lista_final.insert(3, self.dados_calculo[dic_un[self.unidade_medida]][-2].replace(" ",""))

        # Editar/unificar dados dos componentes
        for i, dado in enumerate(self.dados_calculo):
            if i <= 1:
                for d in dado[:-2]:
                    componentes.append(d)
            else:
                for d in dado:
                    componentes.append(d)

        componentes =  '/'.join(componentes).replace("////","/")
        dados = '--'.join(self.dados_roteiro)

        # inserir os componentes editados na posição de índice 2 da lista
        self.lista_final.insert(2, componentes)
        self.lista_final.append(self.ids_roteiro)
        self.lista_final.append(dados)


