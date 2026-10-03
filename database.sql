-- =====================================================================
-- PROJETO: Sistema de Presença Acadêmica (SPA)
-- MATÉRIA: Banco de Dados | Curso Técnico em TI (Grau Técnico)
-- AUTORES: Alex Junio da Silva & Emilly Alcântara
-- DESCRIÇÃO: Script SQL para criação do Banco de Dados Relacional MySQL
-- =====================================================================

-- Criação e seleção do Banco de Dados
CREATE DATABASE IF NOT EXISTS db_spa_presenca
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE db_spa_presenca;

-- ---------------------------------------------------------------------
-- 1. TABELA DE USUÁRIOS (Base para Alunos, Professores e Gestores)
-- ---------------------------------------------------------------------
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('ALUNO', 'PROFESSOR', 'ADMIN') NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- 2. TABELA DE CURSOS E TURMAS
-- ---------------------------------------------------------------------
CREATE TABLE turmas (
    id_turma INT AUTO_INCREMENT PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    modulo VARCHAR(30) NOT NULL,
    ano_letivo INT NOT NULL
);

-- ---------------------------------------------------------------------
-- 3. TABELA DE DISCIPLINAS
-- ---------------------------------------------------------------------
CREATE TABLE disciplinas (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nome_disciplina VARCHAR(80) NOT NULL,
    carga_horaria INT NOT NULL
);

-- ---------------------------------------------------------------------
-- 4. TABELA DE CHAMADAS (Abertas pelos Professores)
-- ---------------------------------------------------------------------
CREATE TABLE chamadas (
    id_chamada INT AUTO_INCREMENT PRIMARY KEY,
    id_professor INT NOT NULL,
    id_disciplina INT NOT NULL,
    id_turma INT NOT NULL,
    codigo_verificacao VARCHAR(6) NOT NULL,
    latitude_aula DECIMAL(10, 8) NOT NULL,
    longitude_aula DECIMAL(11, 8) NOT NULL,
    raio_permitido_metros INT DEFAULT 20,
    data_hora_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_hora_fim DATETIME NOT NULL,
    status_chamada ENUM('ABERTA', 'ENCERRADA') DEFAULT 'ABERTA',
    FOREIGN KEY (id_professor) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
);

-- ---------------------------------------------------------------------
-- 5. TABELA DE REGISTRO DE PRESENÇA (Check-in dos Alunos)
-- ---------------------------------------------------------------------
CREATE TABLE registros_presenca (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_chamada INT NOT NULL,
    id_aluno INT NOT NULL,
    latitude_aluno DECIMAL(10, 8) NOT NULL,
    longitude_aluno DECIMAL(11, 8) NOT NULL,
    distancia_calculada_metros DECIMAL(6, 2) NOT NULL,
    status_presenca ENUM('PRESENTE', 'AUSENTE', 'JUSTIFICADO') NOT NULL,
    data_hora_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_chamada) REFERENCES chamadas(id_chamada),
    FOREIGN KEY (id_aluno) REFERENCES usuarios(id_usuario)
);

-- =====================================================================
-- FIM DO SCRIPT DE CRIAÇÃO DO BANCO DE DADOS
-- =====================================================================