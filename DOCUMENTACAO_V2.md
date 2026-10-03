# 📄 Documentação Técnica V2 - Sistema de Presença Acadêmica (SPA)
**Curso Técnico em TI | Grau Técnico**  
**Autores:** Alex Silva & Emilly Alcântara[cite: 1]  
**Status:** Fase 2 Concluída (Implementação, POO e Testes Iniciais)[cite: 1]

## 1. Evolução para a Fase 2 (Desenvolvimento)
A arquitetura conceitual planejada na V1 foi traduzida para código executável em **Python**, estruturado utilizando os pilares da **Programação Orientada a Objetos (POO)**[cite: 1].

## 2. Estrutura de Classes Implementadas
* **`Usuário` (Superclasse):** Centraliza os atributos base de autenticação (`id_usuario`, `nome`, `cpf`, `senha`, `data_nascimento`) e validação de login[cite: 1].
* **`Aluno` e `Professor` (Subclasses):** Herdam de `Usuário` e especializam atributos e métodos específicos para cada perfil (matrícula/biometria e abertura de chamadas, respectivamente)[cite: 1].
* **`Chamada` e `RegistroPresenca`:** Gerenciam a geração de códigos temporários, validação da janela de tempo (RN02) e cálculo de geolocalização por raio perimetral (RN03)[cite: 1].

## 3. Relatório de Testes Iniciais
Os testes executados no ambiente de desenvolvimento integrado (VS Code) validaram com sucesso:
1. **Validação de Janela Temporal (RN02):** Bloqueio automático de tentativas de check-in fora do tempo estipulado pelo docente[cite: 1].
2. **Validação de Perímetro por GPS / Geofencing (RN03 / RNF05):** Testes de coordenadas dentro do raio tolerado de 20 metros registraram check-in instantâneo, enquanto posições externas foram barradas[cite: 1].
3. **Herança e POO:** Instanciação correta dos objetos de classes distintas e integração fluida dos métodos de validação[cite: 1].