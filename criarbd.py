# importando o SQLite
import sqlite3 as lite

# Criando conexão
con = lite.connect('calc_ppcp.db')

# importando o SQLite
import sqlite3 as lite

# Criando conexão
con = lite.connect('calc_ppcp.db')


## Criando tabela categoria_produtos
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE categoria_produtos (CATEGORIA TEXT PRIMARY KEY, TIPO_1 TEXT,"
#                 "TIPO_2 TEXT, TIPO_3 TEXT, TIPO_4 TEXT, TIPO_5 TEXT, TIPO_6 TEXT,"
#                 "TIPO_7 TEXT, TIPO_8 TEXT)")
#


## Criando tabela medidas_entrada
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE medidas_entrada (CATEGORIA TEXT, TP_PRODUTO TEXT,"
#                 "MEDIDA_1 TEXT, MEDIDA_2 TEXT, MEDIDA_3 TEXT, MEDIDA_4 TEXT, MEDIDA_5 TEXT,"
#                 "MEDIDA_6 TEXT, MEDIDA_7 TEXT)")
#
#


## Criando tabela processos_produtivos
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE processos_produtivos (CATEGORIA TEXT PRIMARY KEY, PROCESSO_1 TEXT,"
#                 "PROCESSO_2 TEXT, PROCESSO_3 TEXT, PROCESSO_4 TEXT, PROCESSO_5 TEXT, PROCESSO_6 TEXT,"
#                 "PROCESSO_7 TEXT, PROCESSO_8 TEXT, PROCESSO_9 TEXT, PROCESSO_10 TEXT, PROCESSO_11 TEXT,"
#                 "PROCESSO_12 TEXT, PROCESSO_13 TEXT, PROCESSO_14 TEXT)")
#


## Criando tabela tempos de processos
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE tempos_processos (COD_PROCESSO TEXT PRIMARY KEY, NOME_PROCESSO TEXT,"
#                 "FAMILIA TEXT, UNIDADE TEXT, UN_MULT_1 TEXT, UN_MULT_2 TEXT, TP_MINUTOS DECIMAL,"
#                 "OBSERVACOES TEXT)")


## Criando tabela calculo_MPS
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE calculo_MPS (CHAVE TEXT PRIMARY KEY, COD_MP TEXT, DESCRICAO TEXT, VALOR DECIMAL,"
#                 "QTD_MULT_MP DECIMAL, UM_MUTIPLICADORA TEXT)")
#


## Criando tabela de ESTRUTURA
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE Estrutura (CODIGO VARCHAR(11) PRIMARY KEY, QTD_BASE TEXT, "
#                 "COMPONENTES TEXT, CADASTRADO CHAR, VALOR TEXT, DATA TEXT)")
#


## Criando tabela de componentes de FM
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE Componentes_fm (COD_FM TEXT PRIMARY KEY, DESCRICAO TEXT, "
#                 "MP1 TEXT, QTD1 DECIMAL, MP2 TEXT, QTD2 DECIMAL, MP3 TEXT, QTD3 DECIMAL, MP4 TEXT, QTD4 DECIMAL)")
#

## Criando tabela de MPs por processo
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE MPS_por_processo (PROCESSO TEXT PRIMARY KEY, MP_BASE TEXT, "
#                 "QTD_APLICACAO INTEGER, MULT_1 TEXT, MULT_2 DECIMAL, MULT_3 TEXT, UNIDADE TEXT)")
#

## Criando tabela de Operações
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE Operacoes (CHAVE INTEGER PRIMARY KEY, SEQUENCIA TEXT, "
#                 "COD_PROCESSO TEXT, NOME_PROCESSO TEXT, DESC_PROCESSO TEXT, DESC_PROCESSO_2 TEXT,"
#                 "DESC_PROCESSSO_3 TEXT)")
#

## Criando tabela de ESTRUTURA PA
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE Estrutura (CODIGO VARCHAR(11) PRIMARY KEY, QTD_BASE TEXT, "
#                 "COMPONENTES TEXT, CADASTRADO CHAR)")



## Criando tabela de Roteiro de Operações
# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE Roteiro (ID TEXT PRIMARY KEY, COD_PROCESSO VARCHAR(6), "
#                 "NOME_PROCESSO TEXT, DESCRICAO TEXT)")


## INCLUINDO UMA COLUNA NA TABELA
# with con:
    # cur = con.cursor()
    # cur.execute("ALTER TABLE Estrutura ADD COLUMN DADOS_ROTEIRO TEXT")


## EXCLUINDO UMA TABELA
# with con:
#     cur = con.cursor()
#     cur.execute("DROP TABLE Estrutura")


## VIZUALIZAR AS TABELAS
# with con:
#     cur = con.cursor()
#     tabelas = list(cur.execute("SELECT * FROM sqlite_master WHERE type='table'"))
#     for tb in tabelas:
#         print(tb)
#




