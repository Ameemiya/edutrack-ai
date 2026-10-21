## 1. Environment Configuration

- [x] 1.1 Criar arquivo `.env` na raiz do projeto contendo a variável `XANO_AUTH_API_URL`

## 2. Authentication Service

- [x] 2.1 Criar `services/auth_service.py` com integração aos endpoints `auth/signup`, `auth/login` e `auth/me` lendo a URL do `.env`

## 3. Frontend Profile Page

- [x] 3.1 Implementar página `pages/3_👤_Perfil.py` com formulários de cadastro e login salvando token na sessão
- [x] 3.2 Implementar exibição dos dados de perfil do usuário autenticado a partir de `auth/me` e botão de logout

