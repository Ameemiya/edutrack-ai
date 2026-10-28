# pages-crud-sync Specification

## Purpose

Enables full bidirectional synchronization of subject and academic task mutations (updates, status toggles, deletions) between Streamlit pages and Xano tables via authenticated endpoints.

## Requirements

### Requirement: Sincronização de Mutações de Disciplinas
The system SHALL allow updating and deleting subjects directly in the Xano database via `PATCH /subjects/{subjects_id}` and `DELETE /subjects/{subjects_id}` endpoints from the Disciplinas page.

#### Scenario: Atualização de disciplina no Xano
- **WHEN** o usuário autenticado edita os dados de uma disciplina existente e confirma a alteração
- **THEN** o sistema envia a requisição para `PATCH /subjects/{subjects_id}` e atualiza o registro no Xano

#### Scenario: Exclusão de disciplina no Xano
- **WHEN** o usuário autenticado confirma a exclusão de uma disciplina existente
- **THEN** o sistema envia a requisição para `DELETE /subjects/{subjects_id}` e remove o registro no Xano

### Requirement: Sincronização de Mutações de Tarefas
The system SHALL allow updating task status, editing task details, and deleting tasks directly in the Xano database via `PATCH /academic_tasks/{academic_tasks_id}` and `DELETE /academic_tasks/{academic_tasks_id}` endpoints from the Tarefas page.

#### Scenario: Atualização de status e detalhes de tarefa no Xano
- **WHEN** o usuário autenticado altera o status ou edita os dados de uma tarefa
- **THEN** o sistema envia a requisição para `PATCH /academic_tasks/{academic_tasks_id}` e reflete a modificação no Xano

#### Scenario: Exclusão de tarefa no Xano
- **WHEN** o usuário autenticado confirma a exclusão de uma tarefa existente
- **THEN** o sistema envia a requisição para `DELETE /academic_tasks/{academic_tasks_id}` e remove o registro no Xano

