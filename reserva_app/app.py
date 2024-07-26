from flask import Flask, render_template, request, redirect

app = Flask("Reserva App")

idSala = 0

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro/processar', methods=['POST'])
def processar_cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['password']
    
    texto = f"{nome},{email},{senha}\n"
    with open("reserva_app/files/usuarios.csv", "a", encoding="utf-8") as usuarios:
        usuarios.write(texto)
    
    return redirect('/')

@app.route('/reservas')
def reserva():
    return render_template('reservas.html')

@app.route('/reservas/nova')
def nova_reserva():
    return render_template('reservar-sala.html')

@app.route('/reservas/nova/processar', methods=['POST'])
def processar_reserva():
    sala = request.form['sala']
    inicio = request.form['inicio']
    fim = request.form['fim']
    
    texto = f"{sala},{inicio},{fim}\n"
    with open("reserva_app/files/reservas.csv", "a", encoding="utf-8") as reservas:
        reservas.write(texto)
    
    return redirect('/reservas/nova/sucesso')

@app.route('/reservas/nova/sucesso')
def detalhe_reserva():
    return render_template('reserva/detalhe-reserva.html')

@app.route('/salas')
def listar_salas():
    return render_template('listar-salas.html')

@app.route('/salas/nova')
def nova_sala():
    return render_template('cadastrar-sala.html')

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

@app.route('/salas/nova/processar', methods=['POST'])
def processar_sala():
    idSala = ultimo_id() + 1
    tipo = request.form['tipo']
    capacidade = request.form['capacidade']
    descricao = request.form['descricao']
    
    texto = f"{idSala},{tipo},{capacidade},{descricao}\n"
    with open("reserva_app/files/salas.csv", "a", encoding="utf-8") as salas:
        salas.write(texto)

    return redirect('/salas/nova/sucesso')
    
@app.route('/salas/nova/sucesso')
def detalhe_sala():
    return render_template('detalhe-sala.html')

if __name__ == '__main__':
    app.run(debug=True)
