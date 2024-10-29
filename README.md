# Reserva App

Projeto para avaliação na matéria LP3.

# Para utilizar

* Instalar o Poetry no computador
* Configurar o virtual environment (venv) do Poetry para o projeto
* Verificar se está tudo configurado corretamente
  * Flask funcionando? Venv escolhido corretamente?
* poetry run python -m reserva_app.app

# Descrição

Aplicação de exemplo para aulas sobre desenvolvimento web backend e criação de multipage applications utilizando Python e Flask.

## Usuários vs. Funcionalidades
- Administrador
  - Login
  - Reservar Sala
  - Ver Reservas
  - Cancelar Reserva
  - Gerenciar Salas
  - Logout
- Professor
  - Cadastrar
  - Login
  - Reservar Sala
  - Ver Reservas
  - Cancelar Reserva
  - Logout

## Models
- Usuário
  - codigo
  - nome
  - email
  - senha
  - ativo
  - admin
- Sala
  - codigo
  - capacidade
  - ativa
  - tipo
  - descricao
- Reserva
  - codigo
  - usuario
  - sala
  - data e hora início
  - data e hora fim
  - ativa
  
