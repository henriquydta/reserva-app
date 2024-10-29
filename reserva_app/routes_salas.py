from flask import Blueprint, render_template, request, redirect
from .db import get_db_connection

usuario_bp = Blueprint('salas', __name__)

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

