# page-data-loading Specification

## Purpose

Enables the Streamlit frontend pages for Disciplinas and Tarefas to load and display data directly from the authenticated Xano API endpoints.

## ADDED Requirements

### Requirement: Carregamento de Disciplinas na Página
The system SHALL load the authenticated user's subjects by calling the Xano endpoint `GET /subjects` and display them in the Disciplinas page.

#### Scenario: Disciplinas carregadas com sucesso
- **WHEN** o usuário autenticado acessa a página de Disciplinas
- **THEN** o sistema requisita o endpoint `GET /subjects` e exibe a lista de disciplinas retornadas

#### Scenario: Exibição de estado vazio quando não há disciplinas
- **WHEN** a resposta do endpoint `GET /subjects` contiver uma lista vazia
- **THEN** o sistema exibe uma mensagem indicando que nenhuma disciplina foi cadastrada

### Requirement: Carregamento de Tarefas na Página
The system SHALL load the authenticated user's academic tasks by calling the Xano endpoint `GET /academic_tasks` and display them in the Tarefas page.

#### Scenario: Tarefas carregadas com sucesso
- **WHEN** o usuário autenticado acessa a página de Tarefas
- **THEN** o sistema requisita o endpoint `GET /academic_tasks` e exibe a lista de tarefas retornadas

#### Scenario: Exibição de estado vazio quando não há tarefas
- **WHEN** a resposta do endpoint `GET /academic_tasks` contiver uma lista vazia
- **THEN** o sistema exibe uma mensagem indicando que nenhuma tarefa foi cadastrada

