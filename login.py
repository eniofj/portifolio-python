import sqlite3

def validar_login(usuario, senha):
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect('dados.db')
        cursor = conn.cursor()

        # Consulta para verificar se o usuário e a senha estão corretos
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()

        # Fecha a conexão
        conn.close()

        # Retorna True se encontrou um usuário, senão False
        return resultado is not None

    except:
        return False


def cadastrar_usuario(usuario, senha):
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect('dados.db')
        cursor = conn.cursor()

        # Verifica se o usuário já existe
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            conn.close()
            return False, "Usuário já existe."

        # Insere o novo usuário
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return True, "Usuário cadastrado com sucesso."

    except sqlite3.Error as e:
        return False, f"Erro ao acessar o banco de dados: {e}"
