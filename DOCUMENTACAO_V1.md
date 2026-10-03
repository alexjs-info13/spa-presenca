# 📄 Documentação Técnica V1 - Sistema de Presença Acadêmica (SPA)
**Curso Técnico em TI | Grau Técnico**  
**Autores:** Alex Silva & Emilly Alcântara[cite: 1]

## 1. Visão Geral do Projeto
O **Sistema de Presença Acadêmica (SPA)** é uma solução mobile/web desenvolvida para automatizar o processo de chamada e controle de frequência escolar[cite: 1]. O sistema permite que o estudante registre sua presença garantindo a autenticidade por meio de dupla validação (geolocalização e biometria facial) sob a supervisão do professor[cite: 1].

## 2. Requisitos do Sistema
* **Requisitos Funcionais (RF):** Cadastro de alunos (RF01), Autenticação (RF02), Liberação de Chamada (RF03), Validação de Geolocalização - Geofencing (RF04), Biometria Facial (RF05), Registro de Presença (RF06), Painel da Coordenadoria (RF07) e Consulta de Frequência (RF08)[cite: 1].
* **Requisitos Não Funcionais (RNF):** Desempenho de resposta em até 3s (RNF01), conformidade com LGPD e criptografia (RNF02), usabilidade e acessibilidade (RNF03), alta disponibilidade (RNF04) e precisão de geolocalização com raio de 10 a 20 metros (RNF05)[cite: 1].
* **Regras de Negócio (RN):** Obrigatoriedade de dados do responsável para menores de 18 anos (RN01), janela temporal restrita configurada pelo professor (RN02), restrição perimetral por GPS (RN03), tolerância de correspondência biométrica superior a 85% (RN04) e bloqueio de sessão dupla por CPF (RN05)[cite: 1].

## 3. Matriz MoSCoW
* **Must Have:** Login (CPF/Senha), código de chamada temporário, validação GPS (Geofence) e biometria facial na chamada[cite: 1].
* **Should Have:** Painel da Coordenadoria, histórico de frequência do aluno, alerta de faltas (limite LDB) e solicitação de validação manual[cite: 1].
* **Could Have:** Leitura de código via QR Code, exportação de relatórios em PDF e Modo Escuro no App[cite: 1].
* **Won't Have:** Câmeras fixas no teto da sala, integração com catracas do prédio e suporte a Smartwatches[cite: 1].

## 4. Modelagem e Prototipação
* **Casos de Uso:** Mapeamento completo dos atores Aluno, Professor e Coordenadoria interagindo com as funções de autenticação, liberação de chamada e registros.
* **Modelagem de Classes (POO):** Estrutura definida com a superclasse `Usuário`, as subclasses `Aluno` e `Professor`, além das classes de controle `Chamada` e `RegistroPresenca`[cite: 1].