import streamlit as st
from services import subject_service
from services import auth_service
from services import report_service
from scripts.calculate_progress import calculate_subject_progress, calculate_all_subjects_progress

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
                # Painel de monitoramento consolidado via calculate_progress.py
                with st.expander("📊 Monitoramento Geral de Progresso (calculate_progress.py)", expanded=False):
                    with st.spinner("Calculando progresso das disciplinas no Xano..."):
                        gen_data = calculate_all_subjects_progress(auth_token=auth_token)

                    if gen_data.get("status") == "success":
                        c_g1, c_g2, c_g3 = st.columns(3)
                        c_g1.metric("Progresso Geral", f"{gen_data.get('overall_progress_percentage', 0.0)}%")
                        c_g2.metric("Disciplinas Monitoradas", gen_data.get("total_subjects", 0))
                        c_g3.metric("Tarefas (Concluídas / Total)", f"{gen_data.get('total_completed_tasks', 0)} / {gen_data.get('total_tasks', 0)}")
                        st.progress(min(gen_data.get("overall_progress_percentage", 0.0) / 100.0, 1.0))

                        with st.expander("📄 Ver JSON Consolidado"):
                            st.json(gen_data)

                        st.markdown("---")
                        st.markdown("**Exportar Relatório Acadêmico (PDF):**")
                        try:
                            user_info = st.session_state.get("user")
                            pdf_bytes_disc = report_service.generate_student_pdf_report(
                                auth_token=auth_token,
                                user_data=user_info,
                                subjects=result if isinstance(result, list) else None,
                            )
                            user_id_slug = f"_{user_info.get('id')}" if (user_info and user_info.get("id")) else ""
                            st.download_button(
                                label="📥 Gerar e Baixar Relatório (PDF)",
                                data=pdf_bytes_disc,
                                file_name=f"relatorio_desempenho{user_id_slug}.pdf",
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True,
                                key="btn_download_pdf_disc_single",
                            )
                        except Exception as e:
                            st.error(f"Erro ao preparar relatório de desempenho: {e}")

                st.write(f"Exibindo **{len(result)}** disciplina(s):")

                for item in result:
                    subject_id = item.get("id")
                    subject_name = item.get("name", "Sem Nome")
                    teacher = item.get("teacher") or item.get("professor") or "Não informado"
                    hours = item.get("hours") or "-"

                    with st.expander(f"📚 {subject_name} — Professor(a): {teacher}", expanded=False):
                        st.markdown(f"**Carga Horária:** {hours}h")
                        st.caption(f"ID: {subject_id} | Criado em: {item.get('created_at', '-')}")

                        # Botões de ação com ícone para monitorar progresso
                        col_prog, col_edit, col_del = st.columns([1, 1, 1])

                        # Monitorar disciplina com calculate_progress.py
                        with col_prog:
                            if st.button("📊 Monitorar", key=f"prog_btn_{subject_id}"):
                                st.session_state[f"show_progress_{subject_id}"] = not st.session_state.get(f"show_progress_{subject_id}", False)

                        # Editar disciplina
                        with col_edit:
                            if st.button("✏️ Editar", key=f"edit_btn_{subject_id}"):
                                st.session_state[f"editing_subject_{subject_id}"] = True

                        # Excluir disciplina
                        with col_del:
                            if st.button("🗑️ Excluir", key=f"del_btn_{subject_id}", type="secondary"):
                                st.session_state[f"confirm_delete_subject_{subject_id}"] = True

                        # Exibição do monitoramento de progresso da disciplina
                        if st.session_state.get(f"show_progress_{subject_id}"):
                            st.markdown("---")
                            st.markdown("##### 📊 Monitoramento de Progresso")
                            prog_info = calculate_subject_progress(subject_id, auth_token=auth_token)

                            if prog_info.get("status") == "success":
                                pct = prog_info.get("progress_percentage", 0.0)
                                st.write(f"**Conclusão das Tarefas:** `{pct}%`")
                                st.progress(min(pct / 100.0, 1.0))

                                p1, p2, p3 = st.columns(3)
                                p1.metric("Total Tarefas", prog_info.get("total_tasks", 0))
                                p2.metric("Concluídas", prog_info.get("completed_tasks", 0))
                                p3.metric("Pendentes", prog_info.get("pending_tasks", 0))

                                with st.expander("📄 Ver JSON do Script"):
                                    st.json(prog_info)
                            else:
                                st.error(prog_info.get("error", "Não foi possível carregar o progresso."))

                        # Confirmação de exclusão
                        if st.session_state.get(f"confirm_delete_subject_{subject_id}"):
                            st.warning(f"Tem certeza que deseja excluir **{subject_name}**? Esta ação não pode ser desfeita.")
                            col_yes, col_no = st.columns(2)
                            with col_yes:
                                if st.button("✅ Confirmar Exclusão", key=f"confirm_yes_{subject_id}", type="primary"):
                                    with st.spinner("Excluindo..."):
                                        deleted = subject_service.delete_subject(subject_id, auth_token=auth_token)
                                    if deleted:
                                        st.success(f"Disciplina '{subject_name}' excluída com sucesso!")
                                        st.session_state.pop(f"confirm_delete_subject_{subject_id}", None)
                                        st.rerun()
                                    else:
                                        st.error("Falha ao excluir a disciplina. Tente novamente.")
                            with col_no:
                                if st.button("❌ Cancelar", key=f"confirm_no_{subject_id}"):
                                    st.session_state.pop(f"confirm_delete_subject_{subject_id}", None)
                                    st.rerun()

                        # Formulário de edição inline
                        if st.session_state.get(f"editing_subject_{subject_id}"):
                            st.markdown("---")
                            st.markdown("**Editar Disciplina:**")
                            with st.form(key=f"form_edit_subject_{subject_id}"):
                                edit_nome = st.text_input(
                                    "Nome da Disciplina *",
                                    value=subject_name,
                                    key=f"edit_name_{subject_id}",
                                )
                                edit_professor = st.text_input(
                                    "Professor(a)",
                                    value=teacher if teacher != "Não informado" else "",
                                    key=f"edit_teacher_{subject_id}",
                                )
                                edit_horas = st.number_input(
                                    "Carga Horária (horas)",
                                    min_value=1,
                                    max_value=500,
                                    value=int(hours) if str(hours).isdigit() else 60,
                                    step=10,
                                    key=f"edit_hours_{subject_id}",
                                )
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    save_edit = st.form_submit_button("💾 Salvar Alterações", type="primary")
                                with col_cancel:
                                    cancel_edit = st.form_submit_button("Cancelar")

                            if save_edit:
                                if not edit_nome.strip():
                                    st.error("O nome da disciplina é obrigatório.")
                                else:
                                    with st.spinner("Atualizando no Xano..."):
                                        updated = subject_service.update_subject(
                                            subject_id,
                                            name=edit_nome,
                                            teacher=edit_professor,
                                            hours=int(edit_horas),
                                            auth_token=auth_token,
                                        )
                                    if updated:
                                        st.success(f"Disciplina '{edit_nome}' atualizada com sucesso!")
                                        st.session_state.pop(f"editing_subject_{subject_id}", None)
                                        st.rerun()
                                    else:
                                        st.error("Falha ao atualizar a disciplina. Tente novamente.")

                            if cancel_edit:
                                st.session_state.pop(f"editing_subject_{subject_id}", None)
                                st.rerun()
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
