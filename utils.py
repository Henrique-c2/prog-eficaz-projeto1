import json

def load_data(nome_arquivo):
    with open(f"static/data/{nome_arquivo}", "r",encoding="utf-8") as arquivo_json:
        texto = arquivo_json.read()

        dicionario = json.loads(texto)
        return dicionario

    
def load_template (nome_arquivo):
    with open(f"static/templates/{nome_arquivo}","r",encoding="utf-8") as template:
        texto = template.read()

        return texto

def add_form (titulo,detalhes):
    with open(f"static/data/notes.json","r", encoding="utf-8") as arquivo_json:
        dicionario = json.load(arquivo_json)

    with open(f"static/data/notes.json","w", encoding="utf-8") as arquivo_json:
        dicionario.append({"titulo" : titulo, "detalhes" : detalhes})

        dicionario = json.dump(dicionario, arquivo_json)