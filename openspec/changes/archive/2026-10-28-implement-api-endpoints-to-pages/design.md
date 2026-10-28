## Context

As páginas de `Disciplinas` e `Tarefas` atualmente utilizam dados fictícios ou estáticos. Os endpoints REST do Xano (`GET /subjects` e `GET /academic_tasks`) já foram implementados com autenticação (`auth = "user"`), garantindo que cada usuário acesse apenas seus próprios registros. As páginas do Streamlit precisam realizar requisições autenticadas para esses endpoints e renderizar as informações retornadas.

## Goals / Non-Goals

**Goals:**
- Implementar o carregamento dinâmico de disciplinas via `GET /subjects` na página `pages/1_📚_Disciplinas.py`.
- Implementar o carregamento dinâmico de tarefas via `GET /academic_tasks` na página `pages/2_📝_Tarefas.py`.
- Tratar autenticação do usuário (envio do token JWT no header `Authorization: Bearer <token>`) e exibir mensagens adequadas caso o usuário não esteja logado.
- Tratar cenários de lista vazia e falhas na comunicação com a API.

**Non-Goals:**
- Alterações em schemas ou criação de novos endpoints no Xano.
- Criação de novos fluxos de cadastro ou edição não solicitados (foco exclusivo em carregar as informações nas páginas).

## Decisions

- **Decisão 1: Criação/Atualização dos métodos de serviço em Python (`services/`)**
  - *Rationale*: Centralizar as chamadas HTTP (`requests.get`) em módulos de serviço (`subject_service.py` e `task_service.py`), permitindo obter a URL base (`XANO_API_URL`) e injetar o token de autenticação vindo de `st.session_state`.
  - *Alternativa considerada*: Chamar `requests` diretamente dentro dos arquivos de página do Streamlit. Descartado para manter separação de responsabilidades e reutilização.

- **Decisão 2: Tratamento de autenticação nas páginas Streamlit**
  - *Rationale*: Verificar se o usuário possui token ativo em `st.session_state`. Se autenticado, carregar os dados reais da API; se não estiver autenticado, orientar o usuário a realizar login na página de Perfil.

## Risks / Trade-offs

- **[Token ausente ou expirado]** → A aplicação exibe aviso orientando o login em vez de quebrar a tela.
- **[Conexão com Xano indisponível]** → Exibir mensagem amigável de erro informando a indisponibilidade temporária.

