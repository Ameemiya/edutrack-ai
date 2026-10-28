## Why

Atualmente, as páginas de Disciplinas e Tarefas no Streamlit exibem dados simulados ou estáticos. Com os endpoints CRUD do Xano já criados e autenticados, é necessário integrar as páginas do frontend para carregar as informações reais de disciplinas e tarefas acadêmicas a partir do backend.

## What Changes

- Integração da página `pages/1_📚_Disciplinas.py` para carregar a listagem de disciplinas do usuário a partir do endpoint do Xano (`GET /subjects`).
- Integração da página `pages/2_📝_Tarefas.py` para carregar a listagem de tarefas do usuário a partir do endpoint do Xano (`GET /academic_tasks`).
- Suporte para tratamento de estados (carregando, lista vazia, erro ou não autenticado) na exibição dos dados das páginas.

## Capabilities

### New Capabilities
- `page-data-loading`: Carregamento de informações de disciplinas e tarefas nas páginas do Streamlit a partir dos endpoints do Xano.

### Modified Capabilities

## Impact

- Arquivos do frontend afetados: `pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`.
- Serviços de dados em `services/`.
- Consumo dos endpoints `GET /subjects` e `GET /academic_tasks`.
- Nenhuma modificação no schema das tabelas do backend.

