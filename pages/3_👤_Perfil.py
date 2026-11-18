import streamlit as st
from services import auth_service
from components.sidebar_profile import render_sidebar_profile

# Configuração da Página
st.set_page_config(page_title="Perfil e Autenticação", page_icon="👤", layout="centered")

# Botão de Perfil Flutuante estilo Discord
render_sidebar_profile()

st.title("👤 Perfil do Usuário")

# Verifica se o usuário já possui um token na sessão
auth_token = st.session_state.get("auth_token")

if auth_token:
    # Usuário autenticado: busca os dados do perfil via endpoint auth/me
    with st.spinner("Carregando dados do perfil..."):
        success, user_data = auth_service.get_me(auth_token)

    if success and isinstance(user_data, dict):
        st.session_state["user"] = user_data
        st.success("🟢 Sessão ativa e autenticada com sucesso")

        with st.container(border=True):
            st.subheader(f"Olá, {user_data.get('name', 'Estudante')}! 👋")
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Nome:** {user_data.get('name', 'N/D')}")
                st.markdown(f"**E-mail:** {user_data.get('email', 'N/D')}")
            with col2:
                st.markdown(f"**ID do Usuário:** `{user_data.get('id', 'N/D')}`")

        st.write("")
        if st.button("🚪 Sair da Conta (Logout)", type="secondary", use_container_width=True):
            auth_service.logout()
            st.info("Você saiu da sua conta.")
            st.rerun()

    else:
        # Token inválido ou expirado
        st.warning(f"Sua sessão expirou ou não pôde ser validada: {user_data}")
        auth_service.logout()
        st.button("Tentar Novamente", on_click=lambda: st.rerun())

else:
    # Usuário não autenticado: formulários de Login e Cadastro
    st.info("Entre com sua conta existente ou cadastre-se para acessar o EduTrack AI.")

    tab_login, tab_signup = st.tabs(["🔑 Entrar (Login)", "📝 Criar Conta (Cadastro)"])

    # Aba de Login (auth/login)
    with tab_login:
        st.subheader("Acesse sua conta")
        with st.form("form_login"):
            login_email = st.text_input("E-mail", placeholder="exemplo@faculdadeimpacta.com.br")
            login_password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

            btn_login = st.form_submit_button("Entrar", type="primary", use_container_width=True)

            if btn_login:
                if not login_email or not login_password:
                    st.error("Por favor, preencha o e-mail e a senha.")
                else:
                    with st.spinner("Autenticando..."):
                        ok, res = auth_service.login(login_email, login_password)
                        if ok and isinstance(res, dict) and "authToken" in res:
                            st.session_state["auth_token"] = res["authToken"]
                            st.success("Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Falha no login: {res}")

    # Aba de Cadastro (auth/signup)
    with tab_signup:
        st.subheader("Criar nova conta")
        with st.form("form_signup"):
            signup_name = st.text_input("Nome Completo", placeholder="Seu Nome")
            signup_email = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
            signup_password = st.text_input("Senha", type="password", placeholder="Crie uma senha segura")
            signup_password_confirm = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")

            btn_signup = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)

            if btn_signup:
                if not signup_name or not signup_email or not signup_password:
                    st.error("Todos os campos são obrigatórios.")
                elif signup_password != signup_password_confirm:
                    st.error("As senhas informadas não coincidem.")
                else:
                    with st.spinner("Criando conta no Xano..."):
                        ok, res = auth_service.signup(signup_name, signup_email, signup_password)
                        if ok and isinstance(res, dict) and "authToken" in res:
                            st.session_state["auth_token"] = res["authToken"]
                            st.success("Cadastro realizado com sucesso! Você já está conectado.")
                            st.rerun()
                        else:
                            st.error(f"Falha no cadastro: {res}")



