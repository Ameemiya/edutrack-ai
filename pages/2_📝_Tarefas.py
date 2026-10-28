import streamlit as st
from services import task_service
from services import subject_service
from services import auth_service

st.set_page_config(page_title="Minhas Tarefas", page_icon="📝", layout="wide")

st.title("📝 Minhas Tarefas")

auth_token = st.session_state.get("auth_token")

if not auth_token:
    st.warning("⚠️ Você precisa estar conectado para visualizar suas tarefas acadêmicas.")
    st.info("Acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
else:
    # Cabeçalho e filtros de busca
    col_busca, col_filtro = st.columns([3, 1])

    with col_busca:
        search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas, Prova P1...")

    with col_filtro:
        filtro_status = st.selectbox(
            "Filtrar por Status",
            ["Todas", "Pendente (pending)", "Em Andamento (in_progress)", "Concluída (completed)"]
        )

    st.markdown("---")

    # Carregamento das tarefas a partir do endpoint do Xano
    with st.spinner("Carregando tarefas do Xano..."):
        success, result = task_service.fetch_tasks(auth_token)

    if success:
        if isinstance(result, list) and len(result) > 0:
            # Mapeamento do filtro
            status_map = {
                "Pendente (pending)": "pending",
                "Em Andamento (in_progress)": "in_progress",
                "Concluída (completed)": "completed",
            }
            target_status = status_map.get(filtro_status)

            # Filtragem local
            filtered_tasks = []
            for task in result:
                title = str(task.get("title", "")).lower()
                desc = str(task.get("description", "")).lower()
                query = search.strip().lower()

                matches_search = (not query) or (query in title or query in desc)
                matches_status = (target_status is None) or (task.get("status") == target_status)

                if matches_search and matches_status:
                    filtered_tasks.append(task)

            if filtered_tasks:
                st.write(f"Exibindo **{len(filtered_tasks)}** de **{len(result)}** tarefas:")
                for task in filtered_tasks:
                    task_id = task.get("id")
                    title = task.get("title", "Sem Título")
                    status = task.get("status", "pending")
                    desc = task.get("description") or "Nenhuma descrição fornecida."
                    due_date = task.get("due_date") or "Não definida"

                    # Ícone conforme status
                    if status == "completed":
                        status_badge = "✅ Concluída"
                    elif status == "in_progress":
                        status_badge = "⏳ Em Andamento"
                    else:
                        status_badge = "📌 Pendente"

                    with st.expander(f"{status_badge} — {title}", expanded=False):
                        st.markdown(f"**Descrição:** {desc}")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"**Prazo:** `{due_date}`")
                        with col_b:
                            if task.get("subject_id"):
                                st.markdown(f"**ID da Disciplina:** `{task.get('subject_id')}`")
                            st.caption(f"ID da Tarefa: {task_id}")
            else:
                st.info("ℹ️ Nenhuma tarefa encontrada com os filtros aplicados.")
        else:
            st.info("ℹ️ Nenhuma tarefa cadastrada no momento. Suas tarefas do Xano aparecerão aqui.")
    else:
        st.error(f"Falha ao carregar tarefas: {result}")
        if st.button("Tentar Novamente"):
            st.rerun()

    # Seção para cadastro de nova tarefa
    st.markdown("---")
    with st.expander("➕ Adicionar Nova Tarefa"):
        with st.form("form_nova_tarefa"):
            novo_titulo = st.text_input("Título da Tarefa *", placeholder="Ex: Entregar Relatório P1")
            nova_desc = st.text_area("Descrição", placeholder="Instruções ou notas sobre a tarefa...")
            nova_data = st.date_input("Data de Entrega", value=None)
            novo_status = st.selectbox("Status Inicial", ["pending", "in_progress", "completed"], index=0)

            btn_salvar_tarefa = st.form_submit_button("Salvar Tarefa", type="primary")
            if btn_salvar_tarefa:
                if not novo_titulo.strip():
                    st.error("O título da tarefa é obrigatório.")
                else:
                    with st.spinner("Salvando tarefa no Xano..."):
                        try:
                            task_service.create_task(
                                title=novo_titulo,
                                description=nova_desc,
                                due_date=str(nova_data) if nova_data else None,
                                status=novo_status,
                                auth_token=auth_token,
                            )
                            st.success(f"Tarefa '{novo_titulo}' criada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao salvar tarefa: {e}")
