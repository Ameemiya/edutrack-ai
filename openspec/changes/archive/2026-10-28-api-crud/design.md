## Context

As tabelas `subjects` e `academic_tasks` estão modeladas no XanoScript (`table/subjects.xs` e `table/academic_tasks.xs`) com relacionamento de chave estrangeira para a tabela de usuários (`user_id`). Para permitir a gestão desses recursos pela aplicação cliente, serão implementados os grupos de API RESTful em XanoScript com controle rigoroso de acesso e isolamento de tenant via `$auth.id`.

## Goals / Non-Goals

**Goals:**
- Implementar grupo de API e endpoints CRUD (`POST`, `GET`, `PATCH`, `DELETE`) para a tabela `subjects`.
- Implementar grupo de API e endpoints CRUD (`POST`, `GET`, `PATCH`, `DELETE`) para a tabela `academic_tasks`.
- Proteger todos os endpoints com autenticação de usuário (`auth = "user"`).
- Garantir isolamento de dados: registros criados recebem `$auth.id` e consultas/mutações operam apenas sobre dados pertencentes ao usuário logado.

**Non-Goals:**
- Alterações em schemas de tabelas existentes.
- Implementação de telas ou lógica de frontend (Streamlit).
- Push ou deploy automático para o servidor Xano (conforme Regra nº 2 do projeto).

## Decisions

- **Decisão 1: Estrutura modular de endpoints em XanoScript**
  - Cada grupo de API possui seu arquivo de declaração de grupo e arquivos individuais para cada verbo/operação:
    - `api/subjects/subjects.xs` (api_group)
    - `api/subjects/subjects_POST.xs` (`POST /subjects`)
    - `api/subjects/subjects_GET.xs` (`GET /subjects`)
    - `api/subjects/subjects_subjects_id_PATCH.xs` (`PATCH /subjects/{subjects_id}`)
    - `api/subjects/subjects_subjects_id_DELETE.xs` (`DELETE /subjects/{subjects_id}`)
    - `api/academic_tasks/academic_tasks.xs` (api_group)
    - `api/academic_tasks/academic_tasks_POST.xs` (`POST /academic_tasks`)
    - `api/academic_tasks/academic_tasks_GET.xs` (`GET /academic_tasks`)
    - `api/academic_tasks/academic_tasks_academic_tasks_id_PATCH.xs` (`PATCH /academic_tasks/{academic_tasks_id}`)
    - `api/academic_tasks/academic_tasks_academic_tasks_id_DELETE.xs` (`DELETE /academic_tasks/{academic_tasks_id}`)

- **Decisão 2: Validação de Propriedade e Isolamento**
  - Em `POST`: `user_id` é preenchido diretamente com `$auth.id`, ignorando qualquer tentativa de injeção manual.
  - Em `GET`: `db.query` filtra explicitamente por `where = [{field: "user_id", op: "==", value: $auth.id}]`.
  - Em `PATCH` e `DELETE`: consulta prévia do registro (`db.get`) seguida de `precondition ($existing.user_id == $auth.id)` para retornar erro caso o recurso pertença a outro usuário.

## Risks / Trade-offs

- **[Tentativa de acesso a recurso de outro usuário]** → O uso de `precondition` garante falha imediata antes de qualquer operação no banco.

