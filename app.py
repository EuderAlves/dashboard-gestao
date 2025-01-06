from datetime import date
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
    try:
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        projects = []

    today = date.today().isoformat()
    return render_template('home.html', projects=projects, today=today)


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
        return redirect(url_for('add_project'))

    # Carregar projetos existentes
    try:
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        projects = []

    return render_template('add_project.html', projects=projects)

@app.route('/remove_project', methods=['POST'])
@login_required
def remove_project():
    project_name = request.form['name']

    # Carregar projetos do JSON
    with open('data/projects.json', 'r') as f:
        projects = json.load(f)

    # Remover o projeto especificado
    projects = [project for project in projects if project['name'] != project_name]

    # Salvar de volta no JSON
    with open('data/projects.json', 'w') as f:
        json.dump(projects, f, indent=4)

    flash("Projeto removido com sucesso!")
    return redirect(url_for('add_project'))


@app.route('/add_developer', methods=['GET', 'POST'])
@login_required
def add_developer():
    try:
        with open('data/developers.json', 'r') as f:
            developers = json.load(f)
    except FileNotFoundError:
        developers = []

    if request.method == 'POST':
        new_developer = {
            "name": request.form['name'],
            "role": request.form['role'],
            "frameworks": request.form['frameworks'],
            "details": request.form['details']
        }
        developers.append(new_developer)

        with open('data/developers.json', 'w') as f:
            json.dump(developers, f, indent=4)

        flash("Desenvolvedor adicionado com sucesso!")
        return redirect(url_for('add_developer'))

    return render_template('add_developer.html', developers=developers)


@app.route('/edit_developer/<name>', methods=['POST'])
@login_required
def edit_developer(name):
    try:
        with open('data/developers.json', 'r') as f:
            developers = json.load(f)
    except FileNotFoundError:
        flash("Nenhum desenvolvedor encontrado!")
        return redirect(url_for('add_developer'))

    developer = next((dev for dev in developers if dev['name'] == name), None)
    if developer:
        developer['role'] = request.form['role']
        developer['frameworks'] = request.form['frameworks']
        developer['details'] = request.form['details']

        with open('data/developers.json', 'w') as f:
            json.dump(developers, f, indent=4)

        flash("Desenvolvedor atualizado com sucesso!")
    else:
        flash("Desenvolvedor não encontrado!")

    return redirect(url_for('add_developer'))


@app.route('/remove_developer/<name>', methods=['POST'])
@login_required
def remove_developer(name):
    try:
        with open('data/developers.json', 'r') as f:
            developers = json.load(f)
    except FileNotFoundError:
        flash("Nenhum desenvolvedor encontrado!")
        return redirect(url_for('add_developer'))

    developers = [dev for dev in developers if dev['name'] != name]

    with open('data/developers.json', 'w') as f:
        json.dump(developers, f, indent=4)

    flash("Desenvolvedor removido com sucesso!")
    return redirect(url_for('add_developer'))

@app.route('/project/<project_name>', methods=['GET', 'POST'])
@login_required
def manage_project(project_name):
    try:
        # Carregar projetos existentes
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        flash("Nenhum projeto encontrado!")
        return redirect(url_for('add_project'))

    # Encontrar o projeto correspondente
    project = next((p for p in projects if p['name'] == project_name), None)
    if not project:
        flash("Projeto não encontrado!")
        return redirect(url_for('add_project'))

    if request.method == 'POST':
        # Atualizar informações do projeto
        project['start_date'] = request.form.get('start_date', project.get('start_date', ''))
        project['end_date'] = request.form.get('end_date', project.get('end_date', ''))
        project['tasks_total'] = int(request.form.get('tasks_total', project.get('tasks_total', 0)))
        project['tasks_completed'] = int(request.form.get('tasks_completed', project.get('tasks_completed', 0)))
        project['developers'] = request.form.getlist('developers')

        # Salvar as atualizações
        with open('data/projects.json', 'w') as f:
            json.dump(projects, f, indent=4)

        flash("Informações do projeto atualizadas com sucesso!")
        return redirect(url_for('add_project'))  # Redirecionar após salvar


    # Carregar desenvolvedores
    try:
        with open('data/developers.json', 'r') as f:
            developers = json.load(f)
    except FileNotFoundError:
        developers = []

    return render_template('manage_project.html', project=project, developers=developers)
@app.route('/project/<int:project_id>')
@login_required
def project_details(project_id):
    try:
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
    except FileNotFoundError:
        return "Projeto não encontrado.", 404

    if 0 <= project_id < len(projects):
        project = projects[project_id]
        return render_template('project_details.html', project=project)
    else:
        return "Projeto não encontrado.", 404


if __name__ == '__main__':
    app.run(debug=True)
