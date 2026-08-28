import sqlite3

nome_banco = "banco.db"


def get_connection():
    conexao = sqlite3.connect(nome_banco)
    return conexao


def init_db():
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            detalhes TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def load_data(nome_arquivo=None):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("SELECT titulo, detalhes FROM notes")
    resultados = cursor.fetchall()

    conexao.close()

    notas = [
        {
            "titulo": resultado[0],
            "detalhes": resultado[1]
        }
        for resultado in resultados
    ]

    return notas


def load_template(nome_arquivo):
    with open(
        f"static/templates/{nome_arquivo}",
        "r",
        encoding="utf-8"
    ) as template:
        texto = template.read()
        return texto


def add_form(titulo, detalhes):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO notes (titulo, detalhes) VALUES (?, ?)",
        (titulo, detalhes)
    )

    conexao.commit()
    conexao.close()