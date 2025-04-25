# Cálculo PPCP

Este projeto é um sistema desenvolvido em Python com interface Tkinter para cálculo de consumo de matéria-prima e tempos de processos produtivos. O programa auxilia no planejamento e controle da produção (PPCP), gerando dados de custo, rendimento e integração com o sistema Protheus.

---

## :hammer_and_wrench: Funcionalidades

- Cálculo de consumo de matéria-prima (MP) com base em medidas dimensionais.
- Estimativa de custo final do produto com base nas MPs e processos.
- Cálculo de tempos de processos produtivos (energia e mão de obra).
- Cadastro de produtos e seus cálculos no banco de dados.
- Interface de login com controle de acesso.
- Visualização e edição de cálculos salvos.
- Integração com o sistema Protheus:
  - Cadastro automatizado da estrutura do produto.
  - Cadastro automatizado do roteiro de operações.

---

## :computer: Tecnologias Utilizadas

- Python 3.x
- Tkinter (GUI)
- SQLite3 (banco de dados local)
- PyAutoGUI (integração com o Protheus via automação de tela)

---

## :floppy_disk: Banco de Dados

O banco de dados é criado localmente com o nome `calc_ppcp.db`. Para iniciar o banco do zero, utilize o script `criar_banco.py`, que está incluído neste repositório.

### Como criar o banco:
```bash
python criar_banco.py
```

Esse script cria todas as tabelas necessárias, incluindo:
- `categoria_produtos`
- `medidas_entrada`
- `processos_produtivos`
- `tempos_processos`
- `calculo_MPS`
- `estrutura`
- `componentes_fm`
- `MPS_por_processo`
- `Operacoes`
- `Roteiro`

> Obs: não é necessário versionar o arquivo `.db` no GitHub. Apenas o script de criação é suficiente.

---

## :rocket: Como Executar o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. (Opcional) Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o sistema:
```bash
python main.py
```

---

## :lock: Controle de Acesso

O sistema possui tela de login. Para cadastrar um novo usuário:
1. Na tela inicial, preencha o usuário e senha.
2. Clique em "Cadastrar Usuário".

Usuários cadastrados têm permissões para salvar e editar cálculos.

---

## :inbox_tray: Integração com Protheus

A partir dos dados salvos, o sistema permite:
- Cadastrar estruturas diretamente no Protheus.
- Cadastrar roteiros de operações usando modelos (gabaritos).
- Automatização via PyAutoGUI, com validações de tela para garantir a correta interação.

> Certifique-se de estar com o Protheus aberto no módulo correto antes de iniciar os cadastros automáticos.

---

## :file_folder: Estrutura do Projeto
```
/
├── main.py                  # Inicializa a interface
├── interface.py             # Interface principal com Tkinter
├── login.py                 # Cadastro e validação de usuário
├── view.py                  # Acesso e manipulação do banco SQLite
├── gravar_calculo.py        # Lógica para salvar estrutura e roteiro
├── calcular_mps.py          # Cálculo de matérias-primas e custos
├── calcular_processos.py    # Cálculo de tempos dos processos
├── cad_estrutura_protheus.py# Cadastro automatizado no Protheus
├── cad_roteiro.py           # Cadastro de roteiro de operações no Protheus
├── validar_screen.py        # Validação de telas via imagem (PyAutoGUI)
├── criar_banco.py           # Script para criação do banco de dados
```

---

## :memo: Licença

Este projeto é de uso interno. Consulte o autor para permissão de distribuição ou modificação.

---

## :handshake: Contato

Para dúvidas, sugestões ou suporte, entre em contato com o desenvolvedor principal.
