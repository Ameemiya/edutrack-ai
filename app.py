import streamlit as st
from services import subject_service
from services import task_service
from services import auth_service
from services import report_service

# Configuração da Página
st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

# Título Principal
st.title("🎓 EduTrack AI")

auth_token = st.session_state.get("auth_token")
user_data = st.session_state.get("user")

# Sidebar (Menu Lateral)
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Acesso Rápido:**")
try:
    st.sidebar.page_link("pages/1_📚_Disciplinas.py", label="Gestão de Disciplinas", icon="📚")
    st.sidebar.page_link("pages/2_📝_Tarefas.py", label="Gestão de Tarefas", icon="📝")
    st.sidebar.page_link("pages/3_👤_Perfil.py", label="Meu Perfil / Login", icon="👤")
except Exception:
    pass

# Status de Conexão na Sidebar
if auth_token:
    st.sidebar.success("🟢 Conectado ao Xano")
    if st.sidebar.button("🔄 Atualizar Dados", use_container_width=True):
        st.rerun()
else:
    st.sidebar.warning("⚠️ Não conectado")

# Mapeamento visual de status de tarefas
STATUS_CONFIG = {
    "pending": "📌 Pendente",
    "in_progress": "⏳ Em Andamento",
    "completed": "✅ Concluída",
}

# Conteúdo Dinâmico
if menu_option == "Dashboard":
    if not auth_token:
        st.info("👋 Bem-vindo ao **EduTrack AI**, seu assistente de gestão acadêmica!")
        st.warning("⚠️ Você não está autenticado. Conecte sua conta para carregar e sincronizar suas disciplinas e tarefas em tempo real com o Xano.")
        try:
            st.page_link("pages/3_👤_Perfil.py", label="Acessar Página de Login / Cadastro", icon="👤")
        except Exception:
            pass

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Disciplinas Cadastradas", "0", help="Faça login para ver suas disciplinas")
        col2.metric("Tarefas Pendentes", "0", help="Faça login para ver suas tarefas pendentes")
        col3.metric("Tarefas Concluídas", "0", help="Faça login para ver suas tarefas concluídas")

    else:
        # Usuário autenticado: busca dados reais no Xano
        with st.spinner("Carregando informações do Xano..."):
            success_subj, subjects = subject_service.fetch_subjects(auth_token)
            success_tasks, tasks = task_service.fetch_tasks(auth_token)

        subjects_list = subjects if success_subj and isinstance(subjects, list) else []
        tasks_list = tasks if success_tasks and isinstance(tasks, list) else []

        # Contagens reais
        total_subjects = len(subjects_list)
        pending_tasks = sum(1 for t in tasks_list if t.get("status") in ("pending", "in_progress"))
        completed_tasks = sum(1 for t in tasks_list if t.get("status") == "completed")

        user_name = user_data.get("name") if user_data else "Estudante"
        st.write(f"Bem-vindo(a) de volta, **{user_name}**! Aqui está o resumo das suas atividades acadêmicas:")

        # Métricas visuais dinâmicas
        col1, col2, col3 = st.columns(3)
        col1.metric("📚 Disciplinas Cadastradas", str(total_subjects))
        col2.metric("⏳ Tarefas em Aberto", str(pending_tasks))
        col3.metric("✅ Tarefas Concluídas", str(completed_tasks))

        st.markdown("---")

        # Painéis de resumo
        col_resumo_disc, col_resumo_tarefas = st.columns(2)

        with col_resumo_disc:
            st.subheader("📚 Suas Disciplinas")
            if subjects_list:
                for s in subjects_list[:5]:
                    prof = s.get("teacher") or s.get("professor") or "Não informado"
                    hours = f"{s.get('hours')}h" if s.get("hours") else ""
                    st.markdown(f"- **{s.get('name', 'Sem Nome')}** — {prof} {f'({hours})' if hours else ''}")
                if len(subjects_list) > 5:
                    st.caption(f"E mais {len(subjects_list) - 5} disciplina(s)...")
            else:
                st.info("Nenhuma disciplina cadastrada ainda.")

            try:
                st.page_link("pages/1_📚_Disciplinas.py", label="Ver / Gerenciar Disciplinas", icon="📚")
            except Exception:
                pass

        with col_resumo_tarefas:
            st.subheader("📝 Tarefas Pendentes Recentes")
            tarefas_abertas = [t for t in tasks_list if t.get("status") != "completed"]
            if tarefas_abertas:
                for t in tarefas_abertas[:5]:
                    due = f" (Prazo: {str(t.get('due_date'))[:10]})" if t.get("due_date") else ""
                    badge = STATUS_CONFIG.get(t.get("status"), "📌")
                    st.markdown(f"- {badge} **{t.get('title', 'Sem Título')}**{due}")
                if len(tarefas_abertas) > 5:
                    st.caption(f"E mais {len(tarefas_abertas) - 5} tarefa(s) pendente(s)...")
            else:
                st.info("🎉 Nenhuma tarefa pendente no momento!")

            try:
                st.page_link("pages/2_📝_Tarefas.py", label="Ver / Gerenciar Tarefas", icon="📝")
            except Exception:
                pass

        # Seção para Geração e Download de Relatório de Desempenho
        st.markdown("---")
        with st.container(border=True):
            st.subheader("📄 Relatório de Desempenho Acadêmico (PDF)")
            st.write(
                "Baixe em um clique o relatório formal em PDF com o seu desempenho acadêmico, "
                "incluindo taxa de conclusão, detalhamento por disciplina e tarefas cadastradas."
            )

            try:
                pdf_bytes = report_service.generate_student_pdf_report(
                    auth_token=auth_token,
                    user_data=user_data,
                    subjects=subjects_list,
                    tasks=tasks_list,
                )
                user_id_slug = f"_{user_data.get('id')}" if (user_data and user_data.get("id")) else ""
                st.download_button(
                    label="📥 Gerar e Baixar Relatório (PDF)",
                    data=pdf_bytes,
                    file_name=f"relatorio_desempenho{user_id_slug}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                    key="btn_download_relatorio_dash",
                )
            except Exception as e:
                st.error(f"Erro ao preparar relatório de desempenho: {e}")

elif menu_option == "Disciplinas":
    st.subheader("📚 Minhas Disciplinas")

    if not auth_token:
        st.warning("⚠️ Você precisa estar conectado para carregar suas disciplinas do Xano.")
        try:
            st.page_link("pages/3_👤_Perfil.py", label="Ir para Login / Cadastro", icon="👤")
        except Exception:
            pass
    else:
        with st.spinner("Carregando disciplinas do Xano..."):
            success, result = subject_service.fetch_subjects(auth_token)

        if success:
            if isinstance(result, list) and len(result) > 0:
                st.write(f"Você possui **{len(result)}** disciplina(s) cadastrada(s):")
                table_data = []
                for s in result:
                    table_data.append({
                        "ID": s.get("id"),
                        "Disciplina": s.get("name", "N/D"),
                        "Professor": s.get("teacher") or s.get("professor") or "Não informado",
                        "Carga Horária (h)": s.get("hours") or "-",
                    })
                st.dataframe(table_data, use_container_width=True)
            else:
                st.info("Nenhuma disciplina cadastrada no momento.")

            st.write("")
            try:
                st.page_link("pages/1_📚_Disciplinas.py", label="➕ Cadastrar, Editar ou Excluir Disciplinas", icon="📚")
            except Exception:
                pass
        else:
            st.error(f"Falha ao carregar disciplinas: {result}")
            if st.button("Tentar Novamente"):
                st.rerun()

elif menu_option == "Tarefas":
    st.subheader("📝 Gerenciamento de Tarefas")

    if not auth_token:
        st.warning("⚠️ Você precisa estar conectado para carregar suas tarefas do Xano.")
        try:
            st.page_link("pages/3_👤_Perfil.py", label="Ir para Login / Cadastro", icon="👤")
        except Exception:
            pass
    else:
        with st.spinner("Carregando tarefas e disciplinas do Xano..."):
            success_tasks, tasks_res = task_service.fetch_tasks(auth_token)
            _, subjects_res = subject_service.fetch_subjects(auth_token)

        subject_map = {}
        if isinstance(subjects_res, list):
            subject_map = {s["id"]: s.get("name") for s in subjects_res if "id" in s}

        if success_tasks:
            if isinstance(tasks_res, list) and len(tasks_res) > 0:
                st.write(f"Você possui **{len(tasks_res)}** tarefa(s) registrada(s):")
                display_tasks = []
                for t in tasks_res:
                    status_raw = t.get("status", "pending")
                    sub_id = t.get("subject_id")
                    sub_name = subject_map.get(sub_id, f"ID {sub_id}") if sub_id else "Nenhuma"
                    due_date = str(t.get("due_date"))[:10] if t.get("due_date") else "Não definida"

                    display_tasks.append({
                        "ID": t.get("id"),
                        "Status": STATUS_CONFIG.get(status_raw, status_raw),
                        "Título": t.get("title", "Sem Título"),
                        "Disciplina": sub_name,
                        "Prazo": due_date,
                    })
                st.dataframe(display_tasks, use_container_width=True)
            else:
                st.info("Nenhuma tarefa cadastrada no momento.")

            st.write("")
            try:
                st.page_link("pages/2_📝_Tarefas.py", label="➕ Cadastrar, Concluir, Editar ou Excluir Tarefas", icon="📝")
            except Exception:
                pass
        else:
            st.error(f"Falha ao carregar tarefas: {tasks_res}")
            if st.button("Tentar Novamente"):
                st.rerun()