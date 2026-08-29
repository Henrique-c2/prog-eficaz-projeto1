import sqlite3

nome_banco = "banco.db"

class Note:
    def __init__(self, id, titulo, detalhes, favorita=0):
        self.id = id
        self.titulo = titulo
        self.detalhes = detalhes
        self.favorita = favorita

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
            detalhes TEXT NOT NULL,
            favorita INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Atualiza bancos que já existiam antes da fase 5
    cursor.execute("PRAGMA table_info(notes)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "favorita" not in colunas:
        cursor.execute("""
            ALTER TABLE notes
            ADD COLUMN favorita INTEGER NOT NULL DEFAULT 0
        """)

    conexao.commit()
    conexao.close()


def load_data(nome_arquivo=None):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, titulo, detalhes, favorita
        FROM notes
        ORDER BY favorita DESC, id ASC
    """)

    resultados = cursor.fetchall()
    conexao.close()

    notas = [
        {
            "id": resultado[0],
            "titulo": resultado[1],
            "detalhes": resultado[2],
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
        """
        SELECT id, titulo, detalhes, favorita
        FROM notes
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
        titulo=resultado[1],
        detalhes=resultado[2],
        favorita=resultado[3]
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

def toggle_favorite(note_id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE notes
        SET favorita = CASE
            WHEN favorita = 1 THEN 0
            ELSE 1
        END
        WHERE id = ?
    """, (note_id,))

    conexao.commit()
    conexao.close()