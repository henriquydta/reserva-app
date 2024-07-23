from flask import Flask, render_template

app = Flask("Reserva App")

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/reservas')
def reserva():
    return render_template('reservas.html')

@app.route('/reservas/nova')
def nova_reserva():
    return render_template('reservar-sala.html')

@app.route('/reservas/nova/sucesso')
def detalhe_reserva():
    return render_template('reserva/detalhe-reserva.html')

@app.route('/salas')
def listar_salas():
    return render_template('listar-salas.html')

@app.route('/salas/nova')
def nova_sala():
    return render_template('cadastrar-sala.html')
