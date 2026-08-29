import sqlite3

nome_banco = "banco.db"

class Note:
    def __init__(self, id, titulo, detalhes):
        self.id = id
        self.titulo = titulo
        self.detalhes = detalhes

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

    cursor.execute("SELECT id, titulo, detalhes FROM notes")
    resultados = cursor.fetchall()

    conexao.close()
    notas = [
        {
            "id": resultado[0],
            "titulo": resultado[1],
            "detalhes": resultado[2]
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

def delete_note(note_id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conexao.commit()
    conexao.close()

def get_note(note_id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, titulo, detalhes FROM notes WHERE id = ?",
        (note_id,)
    )

    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    return Note(
        id=resultado[0],
        titulo=resultado[1],
        detalhes=resultado[2]
    )


def update_note(note_id, titulo, detalhes):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE notes
        SET titulo = ?, detalhes = ?
        WHERE id = ?
        """,
        (titulo, detalhes, note_id)
    )

    conexao.commit()
    conexao.close()