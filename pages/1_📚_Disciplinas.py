import streamlit as st
from services import subject_service
from services import auth_service

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")

st.title("📚 Gestão de Disciplinas")

# Abas para separar Listagem e Cadastro
tab_lista, tab_novo = st.tabs(["📋 Minhas Disciplinas", "➕ Nova Disciplina"])

with tab_lista:
    st.subheader("Disciplinas Cadastradas")

    auth_token = st.session_state.get("auth_token")

    if not auth_token:
        st.warning("⚠️ Você precisa estar conectado para visualizar suas disciplinas.")
        st.info("Acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
    else:
        with st.spinner("Carregando disciplinas do Xano..."):
            success, result = subject_service.fetch_subjects(auth_token)

        if success:
            if isinstance(result, list) and len(result) > 0:
                # Formata os dados para exibição amigável
                display_data = []
                for item in result:
                    display_data.append({
                        "ID": item.get("id"),
                        "Nome da Disciplina": item.get("name", "N/D"),
                        "Professor": item.get("teacher") or item.get("professor") or "Não informado",
                        "Carga Horária (h)": item.get("hours") or "-",
                        "Data de Criação": str(item.get("created_at", "-")),
                    })
                st.dataframe(display_data, use_container_width=True)
            else:
                st.info("ℹ️ Nenhuma disciplina cadastrada no momento. Adicione sua primeira matéria na aba 'Nova Disciplina'!")
        else:
            st.error(f"Falha ao carregar disciplinas: {result}")
            if st.button("Tentar Novamente"):
                st.rerun()

with tab_novo:
    st.subheader("Cadastrar Nova Disciplina")

    auth_token = st.session_state.get("auth_token")

    if not auth_token:
        st.warning("⚠️ Você precisa estar conectado para cadastrar uma nova disciplina.")
        st.info("Acesse a página **👤 Perfil** para fazer login.")
    else:
        with st.form("form_disciplina"):
            nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Arquitetura de Software")
            professor = st.text_input("Professor(a)", placeholder="Ex: Prof. Carlos")
            horas = st.number_input("Carga Horária (horas)", min_value=1, max_value=500, value=60, step=10)

            submitted = st.form_submit_button("Salvar Disciplina", type="primary")
            if submitted:
                if not nome.strip():
                    st.error("O nome da disciplina é obrigatório.")
                else:
                    with st.spinner("Salvando no Xano..."):
                        try:
                            created = subject_service.create_subject(
                                name=nome,
                                teacher=professor,
                                hours=int(horas),
                                auth_token=auth_token,
                            )
                            st.success(f"Disciplina '{nome}' cadastrada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao salvar disciplina: {e}")
