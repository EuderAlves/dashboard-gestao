# Flask: Importa o framework Flask, que permite criar aplicações web.
# render_template: Permite carregar arquivos HTML para serem exibidos no navegador.
# request: Captura dados enviados pelo cliente (como dados de um formulário).
# jsonify: Converte dados Python (listas, dicionários) em JSON, um formato padrão para enviar respostas da aplicação.
from flask import Flask, render_template, request, jsonify

# app: É a instância principal da aplicação Flask.
# O argumento __name__ informa ao Flask onde o código principal está localizado, ajudando na organização de rotas e arquivos.
app = Flask(__name__)

# @app.route('/'):
# Define uma URL específica que o servidor vai responder.
# A / é a raiz da aplicação. Quando você acessa http://localhost:5000, essa função será executada.
# def home():
# Função associada à rota /. Quando alguém visita a URL, essa função é chamada.
# render_template('login.html'):
# Carrega o arquivo templates/login.html e o envia como resposta para o navegador.
# Isso exibe a interface de login ao usuário.
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


import json

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Carregar usuários do JSON
    with open('data/users.json', 'r') as f:
        users = json.load(f)

    # Verificar credenciais
    for user in users:
        if user['email'] == email and user['password'] == password:
            return jsonify({"status": "success", "message": "Login successful"}), 200

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

