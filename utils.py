import sqlite3

nome_banco = "banco.db"

class Note:
    def __init__(self, id, title, content, favorita=0):
        self.id = id
        self.title = title
        self.content = content
        self.favorita = favorita

def get_connection():
    conexao = sqlite3.connect(nome_banco)
    return conexao

def init_db():
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            favorita INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Atualiza bancos que já existiam antes da fase 5
    cursor.execute("PRAGMA table_info(note)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "favorita" not in colunas:
        cursor.execute("""
            ALTER TABLE note
            ADD COLUMN favorita INTEGER NOT NULL DEFAULT 0
        """)

    conexao.commit()
    conexao.close()


def load_data(nome_arquivo=None):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, title, content, favorita
        FROM note
        ORDER BY favorita DESC, id ASC
    """)

    resultados = cursor.fetchall()
    conexao.close()

    notas = [
        {
            "id": resultado[0],
            "title": resultado[1],
            "content": resultado[2],
            "favorita": resultado[3]
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


def add_form(title, content):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO note (title, content) VALUES (?, ?)",
        (title, content)
    )

    conexao.commit()
    conexao.close()

def delete_note(note_id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM note WHERE id = ?",
        (note_id,)
    )

    conexao.commit()
    conexao.close()

def get_note(note_id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, title, content, favorita
        FROM note
        WHERE id = ?
        """,
        (note_id,)
    )

    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    return Note(
        id=resultado[0],
        title=resultado[1],
        content=resultado[2],
        favorita=resultado[3]
    )


def update_note(note_id, title, content):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE note
        SET title = ?, content = ?
        WHERE id = ?
        """,
        (title, content, note_id)
    )

    conexao.commit()
    conexao.close()

def toggle_favorite(note_id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE note
        SET favorita = CASE
            WHEN favorita = 1 THEN 0
            ELSE 1
        END
        WHERE id = ?
    """, (note_id,))

    conexao.commit()
    conexao.close()