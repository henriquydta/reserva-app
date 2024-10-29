from flask import Blueprint, render_template, request, redirect
from .db import get_db_connection

usuario_bp = Blueprint('reservas', __name__)

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
    '''
    texto = f"{numReserva},{sala},{inicio_formatado},{fim_formatado}\n"
    with open("reserva_app/files/reservas.csv", "a", encoding="utf-8") as reservas:
        reservas.write(texto)
    '''

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reserva (num_reserva, sala, inicio, fim, usuario) VALUES (%s, %s, %s, %s, %s)",
        (numReserva, sala, inicio_formatado, fim_formatado, "ADM")
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/reservas/nova/sucesso')

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
    # with open("reserva_app/files/reservas.csv", "r") as arquivo_reserva:
        ## SELECT
        reservas = []

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT num_reserva, sala, inicio, fim, usuario FROM reserva")

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
