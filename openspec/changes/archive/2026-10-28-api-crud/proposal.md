## Why

As tabelas de disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`) necessitam de endpoints CRUD completos (POST, GET, PATCH, DELETE) no Xano com autenticação obrigatória, garantindo que cada usuário acerte e gerencie apenas seus próprios dados.

## What Changes

- Criação dos endpoints CRUD autenticados (`POST`, `GET`, `PATCH`, `DELETE`) para a tabela `subjects` no Xano, filtrando e vinculando os registros ao ID do usuário autenticado (`$auth.id`).
- Criação dos endpoints CRUD autenticados (`POST`, `GET`, `PATCH`, `DELETE`) para a tabela `academic_tasks` no Xano, filtrando e vinculando os registros ao ID do usuário autenticado (`$auth.id`).
- Aplicação de regras de autorização (`auth = "user"`) e validação de propriedade (`user_id == $auth.id`) para impedir acesso indevido entre usuários.

## Capabilities

### New Capabilities
- `api-crud`: Endpoints RESTful CRUD autenticados para `subjects` e `academic_tasks` com isolamento rigoroso por usuário.

### Modified Capabilities

## Impact

- Novos arquivos de API em XanoScript adicionados em `api/subjects/` e `api/academic_tasks/`.
- Requisições devem incluir cabeçalho de autenticação Bearer JWT (`auth = "user"`).

