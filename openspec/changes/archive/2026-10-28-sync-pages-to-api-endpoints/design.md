## Context

As páginas do Streamlit de Disciplinas e Tarefas já realizam o carregamento de listagem e criação básica via API. Os endpoints de mutação do Xano (`PATCH /subjects/{subjects_id}`, `DELETE /subjects/{subjects_id}`, `PATCH /academic_tasks/{academic_tasks_id}` e `DELETE /academic_tasks/{academic_tasks_id}`) já foram criados e protegem os dados por usuário (`$auth.id`). Esta mudança conecta as ações de alteração, conclusão e remoção da interface aos endpoints correspondentes.

## Goals / Non-Goals

**Goals:**
- Sincronizar operações de edição e exclusão em `services/subject_service.py` diretamente com os endpoints `PATCH /subjects/{id}` e `DELETE /subjects/{id}` do Xano.
- Sincronizar operações de edição, mudança de status e exclusão em `services/task_service.py` diretamente com os endpoints `PATCH /academic_tasks/{id}` e `DELETE /academic_tasks/{id}` do Xano.
- Integrar botões/modais de edição e exclusão na página `pages/1_📚_Disciplinas.py`.
- Integrar botões de conclusão, edição e exclusão na página `pages/2_📝_Tarefas.py`.
- Vincular dinamicamente o campo `subject_id` nas tarefas às disciplinas reais cadastradas pelo usuário.

**Non-Goals:**
- Modificações no schema das tabelas do Xano.
- Criação de novos endpoints no Xano (utilização dos endpoints já implementados).
- Deploy automático para o servidor Xano.

## Decisions

- **Decisão 1: Sincronização remota nos serviços Python (`subject_service.py` e `task_service.py`)**
  - Cada método de mutação (`update_*` e `delete_*`) deve priorizar a chamada HTTP autenticada (`PATCH` ou `DELETE`) usando `Authorization: Bearer <token>`.
  - Em caso de sucesso HTTP 200/204, sincroniza o estado local e retorna sucesso.
- **Decisão 2: Experiência interativa no Streamlit**
  - Cada item na página de Tarefas ganha controle interativo para alternar o status diretamente para `completed` ou `pending` via API.
  - Adição de botão de exclusão com confirmação para evitar perdas acidentais.

## Risks / Trade-offs

- **[Falha de conexão durante mutação]** → Exibir mensagens de erro claras via `st.error` mantendo a interface reativa sem perda de estado.

