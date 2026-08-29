from utils import load_data, load_template, add_form, delete_note
def index():
    note_template = load_template("components/note.html")

    notes_li = [
        note_template.format(
            id=dados["id"],
            title=dados["titulo"],
            details=dados["detalhes"]
        )
        for dados in load_data()
    ]

    notes = "\n".join(notes_li)

    return load_template("index.html").format(notes=notes)

def submit(titulo, detalhes):
    add_form(titulo, detalhes)

def delete(note_id):
    delete_note(note_id)