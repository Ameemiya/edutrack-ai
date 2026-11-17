import streamlit as st
from services import subject_service
from services import task_service
from services import auth_service
from services import report_service
from components.sidebar_profile import render_sidebar_profile
from scripts.calculate_progress import calculate_all_subjects_progress, calculate_subject_progress

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

# Status de Conexão na Sidebar
if auth_token:
    st.sidebar.success("🟢 Conectado ao Xano")
    if st.sidebar.button("🔄 Atualizar Dados", use_container_width=True):
        st.rerun()
else:
    st.sidebar.warning("⚠️ Não conectado")

# Botão de Perfil Flutuante estilo Discord
render_sidebar_profile()

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
            progress_data = calculate_all_subjects_progress(auth_token=auth_token)

        subjects_list = subjects if success_subj and isinstance(subjects, list) else []
        tasks_list = tasks if success_tasks and isinstance(tasks, list) else []
        subject_map = {s["id"]: s.get("name", "Sem Nome") for s in subjects_list if "id" in s}

        progress_by_subj = {}
        if isinstance(progress_data, dict) and progress_data.get("status") == "success":
            subj_list = progress_data.get("subjects") or progress_data.get("subjects_progress") or []
            progress_by_subj = {p["subject_id"]: p for p in subj_list if "subject_id" in p}

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
                # Indicadores consolidados de progresso total antes das disciplinas cadastradas
                total_hours = sum(
                    int(s.get("hours")) for s in subjects_list
                    if s.get("hours") is not None and str(s.get("hours")).isdigit()
                )
                tot_tasks_all = progress_data.get("total_tasks") if isinstance(progress_data, dict) and "total_tasks" in progress_data else len(tasks_list)
                comp_tasks_all = progress_data.get("total_completed_tasks") if isinstance(progress_data, dict) and "total_completed_tasks" in progress_data else completed_tasks
                overall_pct = progress_data.get("overall_progress_percentage") if isinstance(progress_data, dict) and "overall_progress_percentage" in progress_data else None
                if overall_pct is None:
                    overall_pct = round((comp_tasks_all / tot_tasks_all) * 100.0, 1) if tot_tasks_all and tot_tasks_all > 0 else 0.0

                col_tot1, col_tot2, col_tot3 = st.columns(3)
                col_tot1.metric("Progresso Total", f"{overall_pct}%")
                col_tot2.metric("Tarefas Concluídas", f"{comp_tasks_all} / {tot_tasks_all}")
                col_tot3.metric("Carga Horária Total", f"{total_hours} horas")
                st.progress(min(float(overall_pct) / 100.0, 1.0))
                st.markdown("---")

                for s in subjects_list[:5]:
                    sub_id = s.get("id")
                    p_info = progress_by_subj.get(sub_id)
                    if not p_info:
                        sub_tasks = [t for t in tasks_list if t.get("subject_id") == sub_id]
                        tot = len(sub_tasks)
                        comp = sum(1 for t in sub_tasks if t.get("status") == "completed")
                        p_info = {
                            "progress_percentage": round((comp / tot) * 100.0, 1) if tot > 0 else 0.0,
                            "completed_tasks": comp,
                            "total_tasks": tot,
                        }

                    pct = p_info.get("progress_percentage", 0.0)
                    completed = p_info.get("completed_tasks", 0)
                    total = p_info.get("total_tasks", 0)

                    prof = s.get("teacher") or s.get("professor") or "Não informado"
                    hours_val = s.get("hours")
                    hours_str = f" — ⏱️ {hours_val} horas" if hours_val else ""
                    st.markdown(f"**{s.get('name', 'Sem Nome')}**")
                    st.markdown(f"👨‍🏫 {prof}{hours_str}")
                    st.progress(min(pct / 100.0, 1.0))
                    st.caption(f"Progresso: **{pct}%** ({completed}/{total})")
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
            tarefas_abertas = [t for t in tasks_list if t.get("status") in ("pending", "in_progress") or t.get("status") != "completed"]
            if tarefas_abertas:
                # Agrupamento de tarefas pendentes e em andamento por disciplina
                tasks_by_subject = {}
                for t in tarefas_abertas:
                    sub_id = t.get("subject_id")
                    sub_name = subject_map.get(sub_id) if sub_id else "Sem disciplina vinculada"
                    if sub_name not in tasks_by_subject:
                        tasks_by_subject[sub_name] = []
                    tasks_by_subject[sub_name].append(t)

                for disc_name, group_tasks in tasks_by_subject.items():
                    st.markdown(f"##### 📚 {disc_name}")
                    for t in group_tasks:
                        badge = STATUS_CONFIG.get(t.get("status"), "📌")
                        st.markdown(f"**{badge} {t.get('title', 'Sem Título')}**")

                        due_val = str(t.get("due_date"))[:10] if t.get("due_date") else None
                        if due_val:
                            st.markdown(
                                f'<div style="font-size: 0.875rem; margin-top: -6px; margin-bottom: 10px; margin-left: 2px;">'
                                f'<span style="opacity: 1; filter: none;">📅</span> <span style="opacity: 0.75;">Prazo: {due_val}</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.write("")
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
        with st.spinner("Carregando disciplinas e progresso do Xano..."):
            success, result = subject_service.fetch_subjects(auth_token)
            progress_res = calculate_all_subjects_progress(auth_token=auth_token)

        prog_map = {}
        if isinstance(progress_res, dict) and progress_res.get("status") == "success":
            subj_list = progress_res.get("subjects") or progress_res.get("subjects_progress") or []
            prog_map = {p["subject_id"]: p for p in subj_list if "subject_id" in p}

        if success:
            if isinstance(result, list) and len(result) > 0:
                st.write(f"Você possui **{len(result)}** disciplina(s) cadastrada(s):")
                table_data = []
                for s in result:
                    sub_id = s.get("id")
                    p_info = prog_map.get(sub_id)
                    if not p_info:
                        single = calculate_subject_progress(sub_id, auth_token=auth_token)
                        p_info = single if isinstance(single, dict) and single.get("status") == "success" else {}

                    pct = p_info.get("progress_percentage", 0.0)
                    comp_tasks = p_info.get("completed_tasks", 0)
                    tot_tasks = p_info.get("total_tasks", 0)

                    table_data.append({
                        "ID": sub_id,
                        "Disciplina": s.get("name", "N/D"),
                        "Professor": s.get("teacher") or s.get("professor") or "Não informado",
                        "Carga Horária (h)": s.get("hours") or "-",
                        "Progresso (%)": f"{pct}%",
                        "Tarefas Concluídas / Total": f"{comp_tasks} / {tot_tasks}",
                    })
                st.dataframe(table_data, use_container_width=True)

                st.markdown("---")
                st.subheader("📊 Progresso das Disciplinas")
                for s in result:
                    sub_id = s.get("id")
                    p_info = prog_map.get(sub_id)
                    if not p_info:
                        single = calculate_subject_progress(sub_id, auth_token=auth_token)
                        p_info = single if isinstance(single, dict) and single.get("status") == "success" else {}

                    pct = p_info.get("progress_percentage", 0.0)
                    comp_tasks = p_info.get("completed_tasks", 0)
                    tot_tasks = p_info.get("total_tasks", 0)

                    prof = s.get("teacher") or s.get("professor") or "Não informado"
                    hours_val = s.get("hours")
                    hours_str = f" — ⏱️ {hours_val} horas" if hours_val else ""
                    st.markdown(f"**{s.get('name', 'Sem Nome')}**")
                    st.markdown(f"👨‍🏫 {prof}{hours_str}")
                    st.progress(min(pct / 100.0, 1.0))
                    st.caption(f"Progresso: **{pct}%** ({comp_tasks}/{tot_tasks})")
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