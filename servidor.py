from flask import Flask, render_template_string, request, redirect
import views
from utils import init_db

init_db()

app = Flask(__name__)

# Configurando a pasta de arquivos estáticos
app.static_folder = 'static'

@app.route('/')
def index():

    return render_template_string(views.index())

@app.route('/submit', methods=['POST'])
def submit_form():
    titulo = request.form.get('titulo')  # Obtém o valor do campo 'titulo'
    detalhes = request.form.get('detalhes')  # Obtém o valor do campo 'detalhes'

    views.submit(titulo, detalhes)
    return redirect('/')

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    views.delete(note_id)
    return redirect("/")

@app.route("/update/<int:note_id>")
def edit_note(note_id):
    return render_template_string(views.edit(note_id))


@app.route("/update", methods=["POST"])
def update_note():
    note_id = request.form.get("id")
    titulo = request.form.get("titulo")
    detalhes = request.form.get("detalhes")

    views.update(note_id, titulo, detalhes)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)