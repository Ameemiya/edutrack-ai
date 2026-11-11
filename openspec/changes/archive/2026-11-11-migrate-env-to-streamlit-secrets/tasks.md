## 1. Migração de Serviços para Streamlit Secrets

- [x] 1.1 Atualizar leitura de configurações em `services/auth_service.py` para priorizar `st.secrets` com fallback para `os.environ`
- [x] 1.2 Atualizar leitura de configurações em `services/subject_service.py` para priorizar `st.secrets` com fallback para `os.environ`
- [x] 1.3 Atualizar leitura de configurações em `services/task_service.py` para priorizar `st.secrets` com fallback para `os.environ`
- [x] 1.4 Atualizar leitura de configurações em `services/report_service.py` para priorizar `st.secrets` com fallback para `os.environ`

## 2. Migração de Scripts e Páginas

- [x] 2.1 Atualizar resolução de credenciais em `scripts/calculate_progress.py` para priorizar `st.secrets` com fallback para `os.environ`
- [x] 2.2 Atualizar leitura de configurações em `pages/3_👤_Perfil.py` para priorizar `st.secrets` com fallback para `os.environ`
