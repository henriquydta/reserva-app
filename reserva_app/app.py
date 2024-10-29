from flask import Flask
from reserva_app.routes_usuario import usuario_bp
from reserva_app.routes_salas import salas_bp
from reserva_app.routes_reservas import reservas_bp

app = Flask("Reserva App")
app.secret_key = "chave-secreta"

app.register_blueprint(usuario_bp)
app.register_blueprint(salas_bp)
app.register_blueprint(reservas_bp)
