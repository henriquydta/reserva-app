CREATE DATABASE reserva_app;

use reserva_app;

CREATE TABLE usuario (
	id_usuario INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(100) NOT NULL,
	email VARCHAR(50) UNIQUE NOT NULL,
	senha VARCHAR(30) NOT NULL,
	ativo BOOL NOT NULL,
	is_admin BOOL NOT NULL
);

CREATE TABLE sala (
	id_sala INT PRIMARY KEY AUTO_INCREMENT,
	capacidade INT NOT NULL,
	ativa BOOL NOT NULL,
	tipo INT NOT NULL,
	descricao BLOB
);

CREATE TABLE reserva (
	id_reserva INT PRIMARY KEY,
	id_usuario INT NOT NULL,
	id_sala INT NOT NULL,
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
   FOREIGN KEY (id_sala) REFERENCES sala(id_sala),
   data_inicio DATETIME NOT NULL,
   data_fim DATETIME NOT NULL,
   ativa BOOL NOT NULL
);