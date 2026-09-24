import streamlit as st
from services import subject_service

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

# Título Principal
st.title("🎓 EduTrack AI")

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

st.sidebar.markdown("---")
if subject_service.is_connected_to_xano():
    st.sidebar.success("🟢 Backend: Xano Conectado")
else:
    st.sidebar.info("🟠 Backend: Armazenamento Local")

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.subheader("📊 Painel Geral")
    st.write("Bem-vindo ao seu assistente acadêmico!")
    
    active_count = subject_service.count_active_subjects()
    all_subjects = subject_service.list_subjects()
    
    # Métricas Visuais
    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas Ativas", str(active_count))
    col2.metric("Total de Disciplinas", str(len(all_subjects)))
    col3.metric("Tarefas Pendentes", "0")
    
    st.markdown("---")
    st.subheader("Minhas Disciplinas Ativas")
    active_list = [s for s in all_subjects if s.get("status") == "Ativa"]
    if active_list:
        cols = st.columns(min(len(active_list), 3))
        for idx, subj in enumerate(active_list):
            with cols[idx % 3]:
                st.markdown(f"**{subj['name']}**")
                if subj.get("code"):
                    st.caption(f"Código: {subj['code']}")
                if subj.get("professor"):
                    st.write(f"👨‍🏫 {subj['professor']}")
                if subj.get("semester"):
                    st.write(f"📅 {subj['semester']}")
    else:
        st.info("Nenhuma disciplina ativa no momento.")

elif menu_option == "Disciplinas":
    st.subheader("📚 Minhas Disciplinas")
    
    # Seção para Adicionar Nova Disciplina
    with st.expander("➕ Cadastrar Nova Disciplina", expanded=False):
        with st.form("form_nova_disciplina", clear_on_submit=True):
            col_nome, col_code = st.columns([2, 1])
            nome = col_nome.text_input("Nome da Disciplina *", placeholder="Ex: Innovation Lab")
            code = col_code.text_input("Código / Sigla", placeholder="Ex: ILAB-2025")
            
            col_prof, col_sem, col_status = st.columns([2, 1, 1])
            professor = col_prof.text_input("Professor(a)", placeholder="Ex: Prof. Silva")
            semester = col_sem.text_input("Semestre", placeholder="Ex: 2025/1")
            status = col_status.selectbox("Status", ["Ativa", "Concluída", "Trancada"], index=0)
            
            notes = st.text_area("Observações / Ementa", placeholder="Tópicos da matéria, links de aulas, etc.")
            
            submitted = st.form_submit_button("Salvar Disciplina")
            if submitted:
                if not nome or not nome.strip():
                    st.error("O nome da disciplina é obrigatório!")
                else:
                    try:
                        subject_service.create_subject(
                            name=nome,
                            code=code,
                            professor=professor,
                            semester=semester,
                            status=status,
                            notes=notes
                        )
                        st.success(f"Disciplina '{nome.strip()}' cadastrada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao cadastrar disciplina: {e}")

    # Listagem de Disciplinas
    subjects = subject_service.list_subjects()
    if not subjects:
        st.info("Nenhuma disciplina cadastrada ainda. Clique em '➕ Cadastrar Nova Disciplina' acima para começar!")
    else:
        # Filtro por Status
        status_filter = st.selectbox("Filtrar por Status:", ["Todas", "Ativa", "Concluída", "Trancada"], index=0)
        filtered_subjects = subjects
        if status_filter != "Todas":
            filtered_subjects = [s for s in subjects if s.get("status") == status_filter]

        st.caption(f"Exibindo {len(filtered_subjects)} disciplina(s)")

        for subj in filtered_subjects:
            with st.container(border=True):
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    status_badge = "🟢 Ativa" if subj.get("status") == "Ativa" else ("🔵 Concluída" if subj.get("status") == "Concluída" else "⚪ Trancada")
                    code_tag = f"({subj['code']})" if subj.get("code") else ""
                    st.markdown(f"### {subj['name']} {code_tag}")
                    st.markdown(f"**Status:** {status_badge}")
                    
                    detalhes = []
                    if subj.get("professor"):
                        detalhes.append(f"👨‍🏫 **Professor(a):** {subj['professor']}")
                    if subj.get("semester"):
                        detalhes.append(f"📅 **Semestre:** {subj['semester']}")
                    if detalhes:
                        st.write(" | ".join(detalhes))
                    
                    if subj.get("notes"):
                        st.write(f"📝 {subj['notes']}")
                
                with col_actions:
                    current_status = subj.get("status", "Ativa")
                    valid_statuses = ["Ativa", "Concluída", "Trancada"]
                    current_idx = valid_statuses.index(current_status) if current_status in valid_statuses else 0
                    
                    new_status = st.selectbox(
                        "Alterar Status",
                        valid_statuses,
                        index=current_idx,
                        key=f"status_select_{subj['id']}"
                    )
                    if new_status != current_status:
                        subject_service.update_subject(subj["id"], status=new_status)
                        st.rerun()

                    if st.button("🗑️ Excluir", key=f"del_subj_{subj['id']}", type="secondary"):
                        subject_service.delete_subject(subj["id"])
                        st.rerun()

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.checkbox("Exemplo: Estudar Streamlit")