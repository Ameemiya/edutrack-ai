# progress-calculation Specification

## Purpose

Calculate academic completion progress for a discipline based on its associated tasks and output structured JSON data.

## Requirements

### Requirement: Cálculo de Progresso de Disciplina
The system SHALL calculate the completion percentage of an academic discipline based on the ratio of completed tasks to total tasks linked to that discipline and output the result as JSON.

#### Scenario: Disciplina com tarefas concluídas e pendentes
- **WHEN** a disciplina possui tarefas registradas e pelo menos uma concluída
- **THEN** o sistema SHALL calcular a porcentagem como `(concluídas / total) * 100` e retornar um JSON contendo o progresso e contagens

#### Scenario: Disciplina sem tarefas cadastradas
- **WHEN** a disciplina não possui nenhuma tarefa associada
- **THEN** o sistema SHALL retornar um JSON com total de tarefas igual a 0 e porcentagem de progresso de 0.0%

#### Scenario: Execução com disciplina inexistente ou não encontrada
- **WHEN** o ID da disciplina informado não for encontrado nos endpoints CRUD
- **THEN** o sistema SHALL retornar um JSON de erro indicando que a disciplina não foi localizada

