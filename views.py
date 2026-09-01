from utils import load_data, load_template, add_form, delete_note,get_note,update_note,toggle_favorite
def index():
    note_template = load_template("components/note.html")

    notes_li = [
        note_template.format(
            id=dados["id"],
            title=dados["title"],
            details=dados["content"],
            favorite_class="favorite" if dados["favorita"] else "",
            favorite_icon="★" if dados["favorita"] else "☆"
        )
        for dados in load_data()
    ]

    notes = "\n".join(notes_li)

    return load_template("index.html").format(notes=notes)

def submit(titulo, detalhes):
    add_form(titulo, detalhes)

def delete(note_id):
    delete_note(note_id)

def edit(note_id):
    note = get_note(note_id)

    if note is None:
        return "Anotação não encontrada"

    return load_template("edit.html").format(
        id=note.id,
        title=note.title,
        details=note.content
    )

def update(note_id, titulo, detalhes):
    update_note(note_id, titulo, detalhes)

def favorite(note_id):
    toggle_favorite(note_id)