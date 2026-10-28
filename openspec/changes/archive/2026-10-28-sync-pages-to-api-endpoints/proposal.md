## Why

As páginas de Disciplinas e Tarefas no Streamlit atualmente carregam e criam registros básicos, mas necessitam de sincronização completa de mutações (atualização de dados, alteração de status e exclusão) com as tabelas `subjects` e `academic_tasks` do Xano através dos endpoints CRUD existentes.

## What Changes

- Sincronização da página `pages/1_📚_Disciplinas.py` com os endpoints `PATCH /subjects/{subjects_id}` e `DELETE /subjects/{subjects_id}` do Xano.
- Sincronização da página `pages/2_📝_Tarefas.py` com os endpoints `PATCH /academic_tasks/{academic_tasks_id}` (incluindo marcação rápida de conclusão) e `DELETE /academic_tasks/{academic_tasks_id}` do Xano.
- Integração da seleção de disciplinas reais do usuário no formulário de criação/edição de tarefas.
- Suporte a operações de edição e exclusão autenticadas na camada de serviços (`subject_service.py` e `task_service.py`).

## Capabilities

### New Capabilities
- `pages-crud-sync`: Sincronização completa de criação, atualização e exclusão das páginas Streamlit com as tabelas `subjects` e `academic_tasks` do Xano.

### Modified Capabilities

## Impact

- Arquivos frontend: `pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py`.
- Serviços: `services/subject_service.py` e `services/task_service.py`.
- Consumo dos endpoints `PATCH` e `DELETE` das APIs do Xano.

