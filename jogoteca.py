from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuarioUm = Usuario('Matheus', 'math', '123')
usuarioDois = Usuario('Nathalia', 'nath', '1234')
usuarioTres = Usuario('Fernanda', 'fefa', '12345')
usuarios = {usuarioUm.nickname: usuarioUm,
            usuarioDois.nickname: usuarioDois,
            usuarioTres.nickname: usuarioTres}


jogo_um = Jogo('Pokemon', 'RPG', 'GBA')
jogo_dois = Jogo('Tetris', 'Puzzle', 'Atari')
jogo_tres = Jogo('Zelda', 'RPG', 'SNES')
lista_jogos = [jogo_um, jogo_dois, jogo_tres]


app = Flask(__name__)
app.secret_key = 'JogoSenha'


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)


@app.route('/novo')
def novo():
    if session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_jogos.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


app.run(debug=True)
