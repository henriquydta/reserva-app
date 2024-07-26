def salvar_usuarios(nome, email, senha):
    texto = f"{nome},{email},{senha}"
    with open("reserva_app/files/usuarios.csv", "a", encoding="utf-8") as usuarios:
        usuarios.write(texto)
        
salvar_usuarios("Henry", "henriquy@gmail.com", "123456")

def indice_id(linha):
    id = 0
    dados = (linha.strip().split(","))
    id = int(dados[0])
    return id
    
def ultimo_id():
    with open("reserva_app/files/salas.csv", "r", encoding="utf-8") as salas:
        ultimoId = [indice_id(linha) for linha in salas]
    return ultimoId[-1]
    
ultimoId = ultimo_id()

print(ultimoId)
