import datetime
import streamlit as st
from services import task_service
from services import subject_service
from services import auth_service
from components.sidebar_profile import render_sidebar_profile

st.set_page_config(page_title="Minhas Tarefas", page_icon="📝", layout="wide")

# Botão de Perfil Flutuante estilo Discord
render_sidebar_profile()

st.title("📝 Minhas Tarefas")

auth_token = st.session_state.get("auth_token")

# Mapeamentos amigáveis de status
STATUS_CONFIG = {
    "pending": {"label": "Pendente", "badge": "📌 Pendente"},
    "in_progress": {"label": "Em Andamento", "badge": "⏳ Em Andamento"},
    "completed": {"label": "Concluída", "badge": "✅ Concluída"},
}
STATUS_KEYS = ["pending", "in_progress", "completed"]
STATUS_PORTUGUESE_LABELS = [STATUS_CONFIG[k]["label"] for k in STATUS_KEYS]


def parse_date(date_val):
    """Converte valor de data para datetime.date ou None."""
    if not date_val:
        return None
    if isinstance(date_val, datetime.date):
        return date_val
    try:
        return datetime.datetime.strptime(str(date_val)[:10], "%Y-%m-%d").date()
    except Exception:
        return None


# Abas para separar Listagem e Cadastro (similar a 1_📚_Disciplinas.py)
tab_lista, tab_novo = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])

with tab_lista:
    st.subheader("Tarefas Cadastradas")

    if not auth_token:
        st.warning("⚠️ Você precisa estar conectado para visualizar suas tarefas acadêmicas.")
        st.info("Acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
    else:
        # Carrega disciplinas para vincular às tarefas com mapeamento robusto
        subjects_list = subject_service.list_subjects(auth_token)
        subject_map = {}
        for s in subjects_list:
            if "id" in s:
                s_name = s.get("name") or f"Disciplina #{s['id']}"
                subject_map[s["id"]] = s_name
                subject_map[str(s["id"])] = s_name
                try:
                    subject_map[int(s["id"])] = s_name
                except (ValueError, TypeError):
                    pass

        # Cabeçalho e filtros de busca mantidos conforme solicitado
        col_busca, col_filtro = st.columns([3, 1])

        with col_busca:
            search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas, Prova P1...")

        with col_filtro:
            filtro_status = st.selectbox(
                "Filtrar por Status",
                ["Todas", "Pendente", "Em Andamento", "Concluída"]
            )

        st.markdown("---")

        # Carregamento das tarefas a partir do endpoint do Xano
        with st.spinner("Carregando tarefas do Xano..."):
            success, result = task_service.fetch_tasks(auth_token)

        if success:
            if isinstance(result, list) and len(result) > 0:
                with st.expander("Exibir Tabela"):
                    display_tasks = []
                    for t in result:
                        status_raw = t.get("status", "pending")
                        status_badge = STATUS_CONFIG.get(status_raw, {}).get("badge", str(status_raw).title())
                        sub_id = t.get("subject_id")
                        raw_name = None
                        if sub_id is not None:
                            raw_name = subject_map.get(sub_id) or subject_map.get(str(sub_id))
                            try:
                                raw_name = raw_name or subject_map.get(int(sub_id))
                            except (ValueError, TypeError):
                                pass
                        sub_name = str(raw_name).strip() if raw_name and str(raw_name).strip().lower() not in ("none", "", "null", "undefined") else "Sem disciplina vinculada"
                        due_date = str(t.get("due_date"))[:10] if t.get("due_date") else "Não definida"

                        display_tasks.append({
                            "ID": t.get("id"),
                            "Status": status_badge,
                            "Título": t.get("title", "Sem Título"),
                            "Disciplina": sub_name,
                            "Prazo": due_date,
                        })
                    st.dataframe(display_tasks, use_container_width=True)

                # Mapeamento do filtro para a chave do banco
                filter_map = {
                    "Pendente": "pending",
                    "Em Andamento": "in_progress",
                    "Concluída": "completed",
                }
                target_status = filter_map.get(filtro_status)

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
                    st.write(f"Exibindo **{len(filtered_tasks)}** de **{len(result)}** tarefa(s):")

                    # Agrupamento das tarefas por disciplina se disponível
                    tasks_by_subject = {}
                    for task in filtered_tasks:
                        sub_id = task.get("subject_id")
                        raw_name = None
                        if sub_id is not None:
                            raw_name = subject_map.get(sub_id) or subject_map.get(str(sub_id))
                            try:
                                raw_name = raw_name or subject_map.get(int(sub_id))
                            except (ValueError, TypeError):
                                pass

                        if not raw_name or str(raw_name).strip().lower() in ("none", "", "null", "undefined"):
                            sub_name = "Sem disciplina vinculada"
                        else:
                            sub_name = str(raw_name).strip()

                        if sub_name not in tasks_by_subject:
                            tasks_by_subject[sub_name] = []
                        tasks_by_subject[sub_name].append(task)

                    # Ordena as seções para exibir disciplinas cadastradas primeiro e sem disciplina no final
                    sorted_subjects = sorted(
                        tasks_by_subject.keys(),
                        key=lambda d: (d == "Sem disciplina vinculada", d.lower()),
                    )

                    for disc_name in sorted_subjects:
                        group_tasks = tasks_by_subject[disc_name]
                        st.markdown(f"#### 📚 {disc_name}")

                        for task in group_tasks:
                            task_id = task.get("id")
                            title = task.get("title", "Sem Título")
                            status = task.get("status", "pending")
                            desc = task.get("description") or "Nenhuma descrição fornecida."
                            due_date = task.get("due_date")
                            due_display = str(due_date)[:10] if due_date else "Não definida"

                            status_badge = STATUS_CONFIG.get(status, {}).get("badge", f"📌 {str(status).title()}")

                            # Caixa de exibição fixa por tarefa (similar a 1_📚_Disciplinas.py)
                            with st.container(border=True):
                                # Título da tarefa com indicador de status
                                st.subheader(f"{status_badge} — {title}")

                                # Prazo da tarefa
                                st.markdown(f"📅 Prazo: `{due_display}`")

                                # Descrição da tarefa
                                if desc and desc != "Nenhuma descrição fornecida.":
                                    st.markdown(f"**Descrição:** {desc}")

                                st.write("")

                            # Ações rápidas: toggle de status e botões de editar/excluir
                            col_toggle, col_edit_btn, col_del_btn = st.columns(3)

                            with col_toggle:
                                if status == "completed":
                                    toggle_label = "🔄 Reabrir Tarefa"
                                    next_status = "pending"
                                else:
                                    toggle_label = "✅ Marcar como Concluída"
                                    next_status = "completed"

                                if st.button(toggle_label, key=f"toggle_{task_id}"):
                                    with st.spinner("Atualizando status..."):
                                        updated = task_service.update_task(
                                            task_id,
                                            title=title,
                                            description=task.get("description") or "",
                                            due_date=due_date,
                                            subject_id=sub_id,
                                            status=next_status,
                                            auth_token=auth_token,
                                        )
                                    if updated:
                                        st.success("Status atualizado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error("Falha ao atualizar o status. Tente novamente.")

                            with col_edit_btn:
                                if st.button("✏️ Editar", key=f"edit_task_btn_{task_id}"):
                                    st.session_state[f"editing_task_{task_id}"] = True

                            with col_del_btn:
                                if st.button("🗑️ Excluir", key=f"del_task_btn_{task_id}", type="secondary"):
                                    st.session_state[f"confirm_delete_task_{task_id}"] = True

                            # Confirmação de exclusão inline
                            if st.session_state.get(f"confirm_delete_task_{task_id}"):
                                st.warning(f"Tem certeza que deseja excluir **{title}**?")
                                col_yes, col_no = st.columns(2)
                                with col_yes:
                                    if st.button("✅ Confirmar Exclusão", key=f"del_yes_{task_id}", type="primary"):
                                        with st.spinner("Excluindo..."):
                                            deleted = task_service.delete_task(task_id, auth_token=auth_token)
                                        if deleted:
                                            st.success(f"Tarefa '{title}' excluída com sucesso!")
                                            st.session_state.pop(f"confirm_delete_task_{task_id}", None)
                                            st.rerun()
                                        else:
                                            st.error("Falha ao excluir a tarefa. Tente novamente.")
                                with col_no:
                                    if st.button("❌ Cancelar", key=f"del_no_{task_id}"):
                                        st.session_state.pop(f"confirm_delete_task_{task_id}", None)
                                        st.rerun()

                            # Formulário de edição inline
                            if st.session_state.get(f"editing_task_{task_id}"):
                                st.markdown("---")
                                st.markdown("**Editar Tarefa:**")

                                subject_choices = [None] + [s["id"] for s in subjects_list if "id" in s]
                                if sub_id and sub_id not in subject_choices:
                                    subject_choices.append(sub_id)
                                current_sub_idx = subject_choices.index(sub_id) if sub_id in subject_choices else 0

                                current_status_idx = STATUS_KEYS.index(status) if status in STATUS_KEYS else 0

                                with st.form(key=f"form_edit_task_{task_id}"):
                                    edit_title = st.text_input(
                                        "Título *",
                                        value=title,
                                        key=f"edit_task_title_{task_id}",
                                    )
                                    edit_desc = st.text_area(
                                        "Descrição",
                                        value=task.get("description") or "",
                                        key=f"edit_task_desc_{task_id}",
                                    )
                                    col_edit_date, col_edit_status = st.columns(2)
                                    with col_edit_date:
                                        edit_date = st.date_input(
                                            "Data de Entrega",
                                            value=parse_date(due_date),
                                            key=f"edit_task_date_{task_id}",
                                        )
                                    with col_edit_status:
                                        edit_status_idx = st.selectbox(
                                            "Status",
                                            options=list(range(len(STATUS_KEYS))),
                                            index=current_status_idx,
                                            format_func=lambda i: STATUS_PORTUGUESE_LABELS[i],
                                            key=f"edit_task_status_{task_id}",
                                        )
                                    edit_sub = st.selectbox(
                                        "Disciplina Associada",
                                        options=subject_choices,
                                        index=current_sub_idx,
                                        format_func=lambda sid: "Nenhuma (não vinculada)" if sid is None else f"📚 {subject_map.get(sid, f'ID {sid}')}",
                                        key=f"edit_task_sub_{task_id}",
                                    )

                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        save_edit = st.form_submit_button("💾 Salvar Alterações", type="primary")
                                    with col_cancel:
                                        cancel_edit = st.form_submit_button("Cancelar")

                                if save_edit:
                                    if not edit_title.strip():
                                        st.error("O título da tarefa é obrigatório.")
                                    else:
                                        with st.spinner("Atualizando no Xano..."):
                                            chosen_status_key = STATUS_KEYS[edit_status_idx]
                                            updated = task_service.update_task(
                                                task_id,
                                                title=edit_title,
                                                description=edit_desc,
                                                due_date=str(edit_date) if edit_date else None,
                                                status=chosen_status_key,
                                                subject_id=edit_sub,
                                                auth_token=auth_token,
                                            )
                                        if updated:
                                            st.success(f"Tarefa '{edit_title}' atualizada com sucesso!")
                                            st.session_state.pop(f"editing_task_{task_id}", None)
                                            st.rerun()
                                        else:
                                            st.error("Falha ao atualizar a tarefa. Tente novamente.")

                                if cancel_edit:
                                    st.session_state.pop(f"editing_task_{task_id}", None)
                                    st.rerun()
                else:
                    st.info("ℹ️ Nenhuma tarefa encontrada com os filtros aplicados.")
            else:
                st.info("ℹ️ Nenhuma tarefa cadastrada no momento. Suas tarefas do Xano aparecerão aqui.")
        else:
            st.error(f"Falha ao carregar tarefas: {result}")
            if st.button("Tentar Novamente"):
                st.rerun()

with tab_novo:
    st.subheader("Cadastrar Nova Tarefa")

    if not auth_token:
        st.warning("⚠️ Você precisa estar conectado para cadastrar uma nova tarefa.")
        st.info("Acesse a página **👤 Perfil** para fazer login.")
    else:
        # Carrega opções de disciplina para a nova tarefa
        subjects_list = subject_service.list_subjects(auth_token)
        new_subject_choices = [None] + [s["id"] for s in subjects_list if "id" in s]
        subject_map_new = {s["id"]: s.get("name", f"Disciplina #{s['id']}") for s in subjects_list if "id" in s}

        with st.form("form_nova_tarefa"):
            novo_titulo = st.text_input("Título da Tarefa *", placeholder="Ex: Entregar Relatório P1")
            nova_desc = st.text_area("Descrição", placeholder="Instruções ou notas sobre a tarefa...")

            col_nova_data, col_novo_status = st.columns(2)
            with col_nova_data:
                nova_data = st.date_input("Data de Entrega", value=None)
            with col_novo_status:
                novo_status_idx = st.selectbox(
                    "Status Inicial",
                    options=list(range(len(STATUS_KEYS))),
                    index=0,
                    format_func=lambda i: STATUS_PORTUGUESE_LABELS[i],
                )

            nova_disciplina = st.selectbox(
                "Disciplina (Opcional)",
                options=new_subject_choices,
                index=0,
                format_func=lambda sid: "Nenhuma (não vinculada)" if sid is None else f"📚 {subject_map_new.get(sid, f'ID {sid}')}",
            )

            btn_salvar_tarefa = st.form_submit_button("Salvar Tarefa", type="primary")
            if btn_salvar_tarefa:
                if not novo_titulo.strip():
                    st.error("O título da tarefa é obrigatório.")
                else:
                    with st.spinner("Salvando tarefa no Xano..."):
                        try:
                            chosen_status = STATUS_KEYS[novo_status_idx]
                            task_service.create_task(
                                title=novo_titulo,
                                description=nova_desc,
                                due_date=str(nova_data) if nova_data else None,
                                status=chosen_status,
                                subject_id=nova_disciplina,
                                auth_token=auth_token,
                            )
                            st.success(f"Tarefa '{novo_titulo}' criada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao salvar tarefa: {e}")
