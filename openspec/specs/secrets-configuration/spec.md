# secrets-configuration Specification

## Purpose

Permite carregar configurações e segredos de conexão de forma nativa e segura através do Streamlit secrets, garantindo compatibilidade com ambientes locais e em nuvem.

## Requirements

### Requirement: Carregamento Prioritário via Streamlit Secrets
O sistema SHALL priorizar a leitura de chaves de configuração e URLs de API (`XANO_AUTH_API_URL`, `XANO_TASKS_API_URL`, `XANO_SUBJECTS_API_URL`, `XANO_API_URL`) a partir de `st.secrets` quando em execução dentro do ambiente Streamlit.

#### Scenario: Chave presente em Streamlit secrets
- **WHEN** o serviço solicitar uma chave de configuração e ela estiver definida em `st.secrets`
- **THEN** o sistema SHALL retornar o valor obtido de `st.secrets` sem tentar carregar arquivos `.env`

#### Scenario: Chave ausente em secrets com fallback para variáveis de ambiente
- **WHEN** o serviço solicitar uma chave ausente em `st.secrets` ou quando executado fora do runtime do Streamlit
- **THEN** o sistema SHALL consultar `os.environ` como mecanismo de fallback

### Requirement: Proteção de Arquivo de Segredos Locais
O sistema SHALL armazenar segredos de ambiente de desenvolvimento em `.streamlit/secrets.toml` e MUST garantir que o diretório `.streamlit/` esteja ignorado no controle de versão Git.

#### Scenario: Verificação de proteção de segredos no gitignore
- **WHEN** o arquivo `.gitignore` for analisado pelo sistema
- **THEN** o padrão `.streamlit/` SHALL constar explicitamente para evitar vazamento acidental de credenciais

