import sqlite3 as lite
import math
from tkinter import messagebox


# Criando conexão
con = lite.connect('calc_ppcp.db')


def ver_form(tb):
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {tb}")
        rows = cur.fetchall()

        # Filtra os campos com valores diferentes de vazio ou NaN
        lista_itens = [
            [item for item in row if item not in (""," ","NAN") and not (isinstance(item, float) and math.isnan(item))]
            for row in rows
        ]

    return lista_itens

# [print(i) for i in ver_form('Roteiro')]

def filtrar_linha(tb, coluna, valor):
    with con:
        cur = con.cursor()

        # Obter os nomes das colunas da tabela
        cur.execute(f"PRAGMA table_info({tb})")
        colunas = [info[1] for info in cur.fetchall()]

        # Verificar se a coluna informada existe na tabela
        if coluna not in colunas:
            raise ValueError(f"A coluna '{coluna}' não existe na tabela '{tb}'.")

        # Filtrar a linha com base no valor da coluna
        cur.execute(f"SELECT * FROM {tb} WHERE {coluna} = ?", (valor,))
        row = cur.fetchone()

        def replace(i):
            try:
                return i if tb =='calculo_MPS' else i.replace("_", " ")
            except:
                return i

        if row:
            # Remover valores inválidos da linha
            linha_filtrada = [
                replace(item) for item in row
                if item not in ("", " ", "NAN") and not (isinstance(item, float) and math.isnan(item))
            ]
            return linha_filtrada
        else:
            # Retornar uma mensagem vazia se nenhum registro for encontrado
            return []


def tempos_processos(categoria, processo):
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM 'tempos_processos' WHERE FAMILIA =? "
                    f"and NOME_PROCESSO=?", [categoria, processo])
        row = cur.fetchall()
        try:
            lista_itens = row[0]
        except:
            lista_itens = row

    return lista_itens


def nome_colunas(tabela):
   with con:
        cur = con.cursor()
        cur.execute(f"PRAGMA table_info([{tabela}]) ")
        colunas = cur.fetchall()
        lista_colunas = [nome[1] for nome in colunas]
   return  lista_colunas

# print(f'Nome colunas view: {nome_colunas("Roteiro")}')


def verificar_usuario(usuario, codigo):
    """"
    Verifica se o usuário que está modificando o registro é o mesmo que gravou o registro,
    caso negativo não poderá ser feita a alteração no registro já gravado.
    """
    # pegar dados do registro
    registro = filtrar_linha('Estrutura', 'CODIGO', codigo)
    # pegar usuario gravado no registro existente
    usuario_gravado = registro[-1].split("--")[0]
    # verificar se o usuário do novo registro é o mesmo já gravado
    if usuario == usuario_gravado:
        return True


def inserir_form(tabela, valores):
    try:
        with con:
            # Cria o cursor dentro do escopo da função
            cur = con.cursor()
            colunas = ", ".join(nome_colunas(tabela))
            placeholders = ",".join(["?"] * len(valores[0]))
            query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
            cur.executemany(query, valores)

    except lite.IntegrityError as e:
        # Verifica se o erro é de violação de restrição UNIQUE
        if "UNIQUE constraint failed" in str(e):
            if tabela == 'estrutura':
                usuario = valores[0][-1].split("--")[0]
                codigo = valores[0][0]
                confirmar_usuario = verificar_usuario(usuario, codigo)
                if confirmar_usuario:
                    confirmar = messagebox.askyesno('Aviso', "O código informado já se encontra cadastrado,"
                                                 "deseja sobrescrevê-lo?")
                    if confirmar:
                        deletar_form(tabela,'CODIGO',[codigo])
                        inserir_form(tabela, valores)
                else:
                    messagebox.showerror('Bloqueado', 'Esse código já foi cadastrado por outro usuário, '
                                                      'utilize outro código!')
        else:
            # Caso outro erro de integridade ocorra, exibe a mensagem
            messagebox.showerror("ERRO",f"Ocorreu um erro de integridade:\n\n {str(e)}")
    except lite.OperationalError as e:
        # Captura erros operacionais, como número errado de valores ou erro de sintaxe
        messagebox.showerror("ERRO",f"Ocorreu um erro ao inserir os dados:\n\n {str(e)}")

# inserir os blocos abaixo assim que finalizar as cotações da atlas
# inserir_form('calculo_MPS',[['BLOCO_PU_D16', 'MP01.0.0303', 'BLOCO_PU_D18', 1350, 1, 'M3']])
# inserir_form('calculo_MPS',[['BLOCO_PU_D16', 'MP01.0.0563', 'BLOCO_PU_D18', 450, 1, 'M3']])
# inserir_form('calculo_MPS',[['BLOCO_PU_D16', 'MP01.0.0106', 'BLOCO_PU_D16', 450, 1, 'M3']])
# #


def deletar_form(tb, coluna, i):
    with con:
        cur = con.cursor()
        query = f"DELETE FROM {tb} WHERE {coluna} ==?"
        cur.execute(query, i)

# deletar_form('calculo_MPS','CHAVE',['BLOCO_PU_D18'])

def atualizar_tabela(tabela, coluna, col_chave, novo_valor, valor_chave):
    with con:
        cur = con.cursor()

        query = f"""UPDATE {tabela} SET {coluna} = ? WHERE {col_chave} = ?"""

        try:
            cur.execute(query, (novo_valor, valor_chave))
            con.commit()
            # messagebox.showinfo('Concluído', 'Registro atualizado com sucesso!')
        except lite.Error as e:
            messagebox.showerror('Erro', f"Erro ao executar a atualização: {e}")


# FAZER AS ATUALIZAÇÕES ABAIXO QUANDO COMPRARMOS O BLOCO D16 NOVAMENTE
# atualizar_tabela('Roteiro', 'DESCRICAO', 'ID',
                    # 'REV00 $ASS ( $DATA ) // QTD. PECA/BLANK = $PCBLK $UNI/BLANK' , '5D')
# atualizar_tabela('calculo_MPS', 'DESCRICAO', 'CHAVE', 'BLOCO_PU_D16', 'BLOCO_PU_D16')
# atualizar_tabela('calculo_MPS', 'VALOR', 'CHAVE', 400, 'BLOCO_PU_D16')

def filtrar_conjunto(tabela, coluna, valor_inicio, valor_final):
    # Filtra registros de uma tabela SQLite com base em um intervalo de valores para uma coluna específica.
    with con:
        cursor = con.cursor()
        query = f"""SELECT * FROM {tabela} WHERE {coluna} BETWEEN ? AND ?"""

        try:
            cursor.execute(query, (valor_inicio, valor_final))
            resultados = cursor.fetchall()
        except lite.Error as e:
            messagebox.showerror('Erro', f"Erro ao executar a consulta: {e}")
            resultados = []

    return resultados


def cadastrar_excel(arquivo):
    import pandas as pd
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo)
    # Converter para maiúsculas
    df = df.apply(lambda x: x.astype(str).str.upper())
    # [print(i) for i in df.values]
    [inserir_form('Roteiro', [i]) for i in df.values]

# cadastrar_excel('roteiro.xlsx')

def nomes_tabelas():
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Obter e exibir os nomes das tabelas
    tabelas = cursor.fetchall()
    # print([tabela[0] for tabela in tabelas])

# nomes_tabelas()
