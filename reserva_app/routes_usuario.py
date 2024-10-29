from flask import Blueprint, render_template, request, redirect
from .db import get_db_connection

usuario_bp = Blueprint('usuario', __name__)

# cadastro e login

@usuario_bp.route('/')
def inicio():
    return render_template('login.html')

@usuario_bp.route('/entrar')
def login():
    # adicionar login do banco de dados

@usuario_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@usuario_bp.route('/cadastro/processar', methods=['POST'])
def processar_cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuario (nome, email, senha, ativo, isAdmin) VALUES (%s, %s, %s, )", (nome, email, senha))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')