from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import mysql.connector

app = Flask("Reserva App")
app.secret_key = "chave-secreta" # (?)

# Início
@app.route('/')
def inicio():
    return render_template('login.html')

''' Cadastro de usuários '''
# Tela de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='estudante1',
        password='teste123',
        database='teste_python'
    )
    return conn

# Processar cadastro
@app.route('/cadastro/processar', methods=['POST'])
def processar_cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['password']
    
    '''
    texto = f"{nome},{email},{senha}\n"
    with open("reserva_app/files/usuarios.csv", "a", encoding="utf-8") as usuarios:
        usuarios.write(texto)
    '''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuario (Nome, Email, Senha) VALUES (%s, %s, %s)", (nome, email, senha))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

''' Reservas '''
# Lista reservas
@app.route('/reservas')
def reserva():
    return render_template('reservas.html')

# Nova reserva
@app.route('/reservas/nova')
def nova_reserva():
    return render_template('reservar-sala.html')

# Métodos para processar corretamente a reserva
def indice_num_reserva(linha):
    dados = (linha.strip().split(","))
    try:
        return int(dados[0])  # Retorna o ID da linha
    except (IndexError, ValueError):
        return 0  # Retorna 0 se houver um problema ao converter para inteiro
    
def ultimo_num_reserva():
    with open("reserva_app/files/reservas.csv", "r", encoding="utf-8") as reservas:
        ultimoId = [indice_num_reserva(linha) for linha in reservas]
        
    if ultimoId:  # Verifica se a lista não está vazia
        return ultimoId[-1]
    return 0  # Valor padrão quando a lista está vazia

def format_datetime_br(dt_string):
    dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M")
    formatted_dt = dt.strftime("%d/%m/%Y %H:%M")
    return formatted_dt

# Rota para processar reserva
@app.route('/reservas/nova/processar', methods=['POST'])
def processar_reserva():
    numReserva = ultimo_num_reserva() + 1
    sala = request.form['sala']
    inicio = request.form['inicio']
    fim = request.form['fim']
    
    # Formatar datas
    inicio_formatado = format_datetime_br(inicio)
    fim_formatado = format_datetime_br(fim)
    
    reserva = {
        "numReserva": numReserva,
        "sala": sala,
        "inicio": inicio_formatado,
        "fim": fim_formatado,
        "usuario": "ADM"
    }
    
    session['ultimaReservaRegistradaPeloUsuario'] = reserva
    
    ## INSERT

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reserva (Data_Hota_Inicio, Data_Hora_Final, ID_usuario, ID_sala) VALUES (%s, %s, %s)", (inicio_formatado, fim_formatado, senha))
    conn.commit()
    cursor.close()
    conn.close()
    '''
    texto = f"{numReserva},{sala},{inicio_formatado},{fim_formatado}\n"
    with open("reserva_app/files/reservas.csv", "a", encoding="utf-8") as reservas:
        reservas.write(texto)
    
    return redirect('/reservas/nova/sucesso')
'''
# Métodos para leitura do arquivo de reservas
def reserva_para_dicionario(linha):
    dados = (linha.strip().split(","))
    return {
        "numReserva": dados[0],
        "sala": dados[1],
        "inicio": dados[2],
        "fim": dados[3],        
    }

def obter_reserva_dicionario():
    with open("reserva_app/files/reservas.csv", "r") as arquivo_reserva:
        ## SELECT
        reservas = []
        for linha in arquivo_reserva:
            reserva = reserva_para_dicionario(linha)
            reservas.append(reserva)
        return reservas
    
lista_reservas = obter_reserva_dicionario()
ultima_reserva = lista_reservas[-1]
    
# Exibe detalhes da última reserva
@app.route('/reservas/nova/sucesso')
def detalhe_reserva():
    reserva = session.get('ultimaReservaRegistradaPeloUsuario')
    return render_template('reserva/detalhe-reserva.html', reserva = reserva)

''' Salas '''
# Métodos para leitura do arquivo de salas
def sala_para_dicionario(linha):
    dados = (linha.strip().split(","))
    
    if dados[1] == "1":
        tipo = "Laboratório de Informática"
    elif dados[1] == "2":
        tipo = "Laboratório de Química"
    elif dados[1] == "3":
        tipo = "Sala de Aula"
        
    return {
        "id": dados[0],
        "sala": tipo,
        "capacidade": dados[2],
        "descricao": dados[3],   
        "ativa": "Sim"     
    }

def obter_dicionario_salas():
    with open("reserva_app/files/salas.csv", "r", encoding="utf-8") as arquivo_salas:
        salas = []
        for linha in arquivo_salas:
            sala = sala_para_dicionario(linha)
            salas.append(sala)
        return salas

# Listar salas
@app.route('/salas')
def listar_salas():
    lista_salas = obter_dicionario_salas()
    return render_template('listar-salas.html', salas = lista_salas)

# Cadastrar nova sala
@app.route('/salas/nova')
def nova_sala():
    return render_template('cadastrar-sala.html')

# Métodos para processar corretamente a sala, verificando o último ID registrado
def indice_id(linha):
    dados = (linha.strip().split(","))
    try:
        return int(dados[0])  # Retorna o ID da linha
    except (IndexError, ValueError):
        return 0  # Retorna 0 se houver um problema ao converter para inteiro
    
def ultimo_id():
    with open("reserva_app/files/salas.csv", "r", encoding="utf-8") as salas:
        ultimoId = [indice_id(linha) for linha in salas]
        
    if ultimoId:  # Verifica se a lista não está vazia
        return ultimoId[-1]
    return 0  # Valor padrão quando a lista está vazia

# Rota para processar a sala
@app.route('/salas/nova/processar', methods=['POST'])
def processar_sala():
    id_sala = ultimo_id() + 1
    tipo = request.form['tipo']
    capacidade = request.form['capacidade']
    descricao = request.form['descricao']
    ativa = True
    usuario = "ADM"
    
    if tipo == "1":
        tipo_string = "Laboratório de Informática"
    elif tipo == "2":
        tipo_string = "Laboratório de Química"
    elif tipo == "3":
        tipo_string = "Sala de Aula"
        
    if ativa:
        ativa_string = "Sim"
    else:
        ativa_string = "Não"
    
    sala_registrada = {
        "id_sala": id_sala,
        "tipo": tipo_string,
        "capacidade": capacidade,
        "descricao": descricao,
        "ativa": ativa_string,
        "usuario": "ADM"
    }
    
    session['ultimaSalaRegistradaPeloUsuario'] = sala_registrada
    
    texto = f"{id_sala},{tipo},{capacidade},{descricao}\n"
    with open("reserva_app/files/salas.csv", "a", encoding="utf-8") as salas:
        salas.write(texto)

    return redirect('/salas/nova/sucesso')

# Detalhes da sala registrada
@app.route('/salas/nova/sucesso')
def detalhe_sala():
    sala_registrada = session.get('ultimaSalaRegistradaPeloUsuario')
    return render_template('detalhe-sala.html', salaRegistrada = sala_registrada)

if __name__ == '__main__':
    app.run(debug=True)



'''
def conexao_sql (sala, reserva, usuario):
    return mysql.connector.connect(sala=sala, reserva=reserva, usuario=usuario)

def fechar_conexao (con):
    con.close
    '''
