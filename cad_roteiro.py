from datetime import datetime
import re
import pyautogui as pyg
import time
import view as vw
from tkinter import messagebox
import validar_screen as scr


data_e_hora_atuais = datetime.now()
data_ref = f'{data_e_hora_atuais.strftime("%d/%m/%y")}'


def escrita_tempo(acao, tempo):
    # Utiliza a função de escrita com o intervalo de tempo determinado para cada caso
    return  pyg.write(acao), time.sleep(tempo)


def editar_cod_processo(codigo):
    # converte o código do processo para str com 6 casas decimais
    cod_editado = f'{"0"*(6-(len(codigo)))}{codigo}'
    return cod_editado

def cadastrar_protheus(codigo, info_engenharia, dimensionais):

    scr.verificar_screen("barra_roteiro.jpg") # Confirmar se a tela de cadastro de roteiro está aberta
    pyg.click(x=772, y=124)
    time.sleep(1)
    pyg.hotkey("Alt", "i") # Abrir novo formulário de cadastro de roteiro
    scr.verificar_screen("barra_cad_roteiro.jpg") # Confirmar se o novo formulário de cadastro de roteiro está aberto
    escrita_tempo('01', 0.5) # preenche 1º campo com valor padrão "01" no formulário
    escrita_tempo(codigo, 0.5) # preecnhe o campo código no formulário

    pyg.press("tab", interval=0.3) # transfere para a primeira linha do roteiro

    # confirmar se o código já tem roteiro cadastrado no protheus
    scr.verificar_screen_timeout('roteiro_ja_cadastrado.jpg', codigo, timeout=2)

    for i, id in enumerate(info_engenharia):
        dados_roteiro = vw.filtrar_linha('Roteiro', 'ID', id) # puxar dados de cada processo
        escrita_tempo(str(i+1), 0.5) # incluir a sequência do processo (crescente)
        pyg.press("tab", interval=0.3) # pular para a célula do código do processo
        cod_processo = editar_cod_processo(dados_roteiro[1]) # formatar o código do processo
        pyg.press("enter", interval=0.3) # entra na célula para escrever o código do processo
        escrita_tempo(cod_processo, 0.3) # escreve o codigo do processo
        pyg.press("enter", interval=0.3) # abre o formulário de info_engenharia
        escrita_tempo(editar_descricao(dados_roteiro[3], dimensionais), 0.5) # escreve as instruções no forulário info_engenharia
        pyg.press("tab", interval=0.3) # posicionar no botão Ok
        pyg.press("enter", interval=0.3) # apertar o botão ok
        pyg.press("Right", interval=0.1) # posicionar na célula lote padrão
        escrita_tempo("0", 0.3) # preencher célula lote padrão
        pyg.press("enter", interval=0.3) # alternar para célula tempo padrão
        escrita_tempo("1", 1) # preencher célula tempo padrão
        pyg.press("enter", interval=0.3) # sair da célula tempo padrão
        pyg.press("Down", interval=0.3) # descer para próxima linha

    pyg.press("Down", interval=0.4) # descer uma linha em branco
    pyg.click(x=1306, y=124) # clicar no botão confirmar
    scr.verificar_screen("conf_roteiro.jpg") # verificar tela de confirmação
    pyg.press("enter", interval=4) # confirmar cadastro


def abrir_roteiro(produtos):
    # Abrir os dados do roteiro no banco de dados


    for produto in produtos:
        codigo = produto[0]
        info_engenharia =  produto[1]
        # ordenar sequencia de processos
        info_engenharia.sort()
        # puxar os dados do produto
        dados_produto = vw.filtrar_linha('Estrutura', 'CODIGO', codigo)
        # criar a lista dos dimensionais
        dimensionais = dados_produto[-1].split("--")
        # substituir o ultimo elemento pelo valor correspondente (em MT ou em PÇ)
        dimensionais[-1] = dados_produto[1]

        cadastrar_protheus(codigo, info_engenharia, dimensionais)


def buscar_fm(fm):
    # pegar o código da Fórmula pela sua descrição (somente para categoria "Impregnados")
    try:
        formula = vw.filtrar_linha('calculo_MPS', 'CHAVE', fm)
        return f'{formula[1]} ({fm})'
    except:
        pass


def editar_descricao(texto, dimensionais):
    """
    Substitui as palavras no texto com base no dicionário de valores.
    :param texto: str - Texto contendo palavras a substituir.
    :param valores: dict - Dicionário com palavras a substituir e seus respectivos valores.
    :return: str - Texto com as substituições feitas.
    """
    un_txt = 'PÇS' if float(dimensionais[6]) > 1 else 'PÇ'

    valores = {
        '$ASS': dimensionais[0], '$DATA': data_ref, 'C$': dimensionais[1], 'L$': dimensionais[2],
        'EF$': dimensionais[3], 'E$': dimensionais[3], '$DEN': str(float(dimensionais[4])-10.0).split('.')[0],
        '$FM': buscar_fm(dimensionais[5]), '$PCBLK': f'{dimensionais[6]} {un_txt}', '$UNI': dimensionais[7],
        '$RENDIMENTO': dimensionais[8]
    }

    padrao = re.compile(r'\$?[A-Za-z0-9]+\$?')  # Captura palavras que contêm $

    def substituir(match):
        chave = match.group()
        return valores.get(chave, chave)  # Substitui pela chave no dicionário, se existir

    return padrao.sub(substituir, texto.replace('( ', '(').replace(' )', ')'))



# abrir_roteiro([['PA90.2.0754', ['4G', '6C', '8A']], ['PA90.2.0755', ['4G', '6C', '8A']]])
