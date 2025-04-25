import pyautogui as pyg
import time
import view as vw
import validar_screen as scr


def cadastrar_estrutura(lista_itens):
    dic_produto = formatar_itens(lista_itens)
    tempo_tab = 1.2
    pyg.FAILSAFE = True

    scr.verificar_screen("tela_estrutura_nv.jpg")
    pyg.hotkey("Alt", "i")
    scr.verificar_screen("tela_cadastro_estrutura_atu.jpg")

    escrita_tempo(dic_produto['codigo'], 0.1)  # código
    pyg.press("tab", interval=0.5)

    # verificar se retorna mensagem de item já cadastrado
    scr.verificar_screen_timeout('estrutura_ja_cadastrada.jpg', dic_produto['codigo'],timeout=2)

    escrita_tempo(dic_produto['qtd_base'], 0.1)  # quantidade base
    pyg.press("tab", interval=0.2)
    pyg.press("enter", interval=tempo_tab)

    for componente in dic_produto['componentes']:
        escrita_tempo(componente[0].replace(" ", ""), 0.2)  # cod_componente
        pyg.press('enter', interval=tempo_tab)
        pyg.press('Right', interval=tempo_tab)
        pyg.press('Right', interval=0.2)
        pyg.press('enter', interval=0.2)
        escrita_tempo(componente[2][0:7], tempo_tab)  # qtd_componente
        pyg.press('enter', interval=tempo_tab)
        pyg.press('down', interval=tempo_tab)

    pyg.click(x=dic_produto['pos_mouse'][0], y=dic_produto['pos_mouse'][1])
    scr.verificar_screen("conf_rev_estrutura.jpg")
    pyg.press('enter', interval=0.2)
    scr.verificar_screen("conf_selec_revisao.jpg")
    pyg.press('tab', interval=0.2)
    pyg.press('enter', interval=0.2)
    scr.verificar_screen('conf_roteiro.jpg')
    pyg.press('enter', interval=tempo_tab)
    vw.atualizar_tabela('Estrutura', 'CADASTRADO', 'CODIGO', 'S', dic_produto['codigo'])


def escrita_tempo(texto, tempo):
    return pyg.write(texto), time.sleep(tempo)


def formatar_itens(lista_itens):
    dic_itens = {'qtd_base': lista_itens[1].split(".")[0], 'codigo': lista_itens[0], 'pos_mouse': (1311, 119)                 }
    estrutura = lista_itens[2].split("/")
    componentes = []
    ini = 0
    fin = 3



    for item in estrutura:
        componentes.append(estrutura[ini:fin]) if len(estrutura[ini:fin]) > 0 else False
        ini +=3
        fin +=3

    dic_itens['componentes'] = componentes

    return dic_itens






