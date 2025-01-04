from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessária para gerenciar as sessões

# Função Middleware
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Você precisa estar logado para acessar esta página.")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Carregar usuários do arquivo JSON
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        flash("Erro: Arquivo de usuários não encontrado.")
        return redirect(url_for('login_page'))

    # Verificar credenciais
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if user:
        session['user'] = user  # Salvar o usuário na sessão
        flash("Login realizado com sucesso!")
        return redirect(url_for('home'))
    else:
        flash("Credenciais inválidas. Tente novamente.")
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remover o usuário da sessão
    flash("Logout realizado com sucesso!")
    return redirect(url_for('login_page'))

@app.route('/home')
@login_required
def home():
    return render_template('base.html')

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    try:
        # Carregar usuários do JSON
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []  # Caso o arquivo não exista

    if request.method == 'POST':
        new_user = {
            "email": request.form['email'],
            "password": request.form['password']
        }
        users.append(new_user)

        # Salvar de volta no JSON
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)

        flash("Usuário adicionado com sucesso!")
        return redirect(url_for('add_user'))  # Redireciona para evitar reenvio do formulário

    # Passar a lista de usuários ao template
    return render_template('add_user.html', users=users)


@app.route('/remove_user', methods=['POST'])
@login_required
def remove_user():
    email_to_remove = request.form['email']

    # Carregar usuários do JSON
    with open('data/users.json', 'r') as f:
        users = json.load(f)

    # Filtrar para excluir o usuário especificado
    users = [user for user in users if user['email'] != email_to_remove]

    # Salvar de volta no JSON
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

    return "Usuário removido com sucesso!", 200
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        try:
            with open('data/projects.json', 'r') as f:
                projects = json.load(f)
        except FileNotFoundError:
            projects = []

        new_project = {
            "name": request.form['name'],
            "description": request.form['description']
        }
        projects.append(new_project)

        with open('data/projects.json', 'w') as f:
            json.dump(projects, f, indent=4)

        flash("Projeto adicionado com sucesso!")
        return redirect(url_for('home'))

    return render_template('add_project.html')

@app.route('/add_developer', methods=['GET', 'POST'])
@login_required
def add_developer():
    if request.method == 'POST':
        try:
            with open('data/developers.json', 'r') as f:
                developers = json.load(f)
        except FileNotFoundError:
            developers = []

        new_developer = {
            "name": request.form['name'],
            "skills": request.form['skills']
        }
        developers.append(new_developer)

        with open('data/developers.json', 'w') as f:
            json.dump(developers, f, indent=4)

        flash("Desenvolvedor adicionado com sucesso!")
        return redirect(url_for('home'))

    return render_template('add_developer.html')

if __name__ == '__main__':
    app.run(debug=True)
