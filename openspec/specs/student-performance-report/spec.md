# student-performance-report Specification

## Purpose

Enables generation of student academic performance reports in PDF format and downloading them via an authenticated Xano backend endpoint.

## Requirements

### Requirement: Geração de Relatório PDF de Desempenho
The system SHALL generate a PDF document detailing student performance, including student information, enrolled subjects, completed tasks, pending tasks, and overall progress metrics.

#### Scenario: Geração bem-sucedida de relatório PDF
- **WHEN** o script de geração de relatório PDF é executado com os dados acadêmicos do aluno
- **THEN** o sistema SHALL criar um arquivo PDF formatado contendo as métricas de desempenho e disciplinas

#### Scenario: Geração de relatório sem disciplinas ou tarefas
- **WHEN** o aluno não possui disciplinas ou tarefas registradas
- **THEN** o sistema SHALL gerar o PDF indicando a ausência de registros acadêmicos sem gerar erros de execução

### Requirement: Endpoint Xano para Download de Relatório
The system SHALL provide an authenticated endpoint in Xano allowing users to download or retrieve their performance report file securely.

#### Scenario: Download de relatório por usuário autenticado
- **WHEN** um usuário autenticado envia uma requisição GET para o endpoint de download de relatório
- **THEN** o sistema SHALL fornecer o arquivo de relatório vinculado ao usuário autenticado

#### Scenario: Tentativa de download sem autenticação
- **WHEN** uma requisição de download é realizada sem token de autenticação válido
- **THEN** o sistema SHALL rejeitar a solicitação com erro de acesso não autorizado

