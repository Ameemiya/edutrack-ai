import streamlit as st
from services import auth_service


def render_sidebar_profile() -> None:
    """
    Renders a Discord-styled floating profile button docked at the bottom-left of the Streamlit sidebar.
    Shows the user profile icon (👤) in the avatar area with a filled status dot
    (green when logged in, yellow when not logged in), and the user's name occupying the space
    normally used for username and status in Discord.
    """
    auth_token = st.session_state.get("auth_token")
    user_data = st.session_state.get("user")

    user_display_name = "Fazer Login"

    if auth_token:
        if not user_data:
            try:
                success, fetched_user = auth_service.get_me(auth_token)
                if success and isinstance(fetched_user, dict):
                    st.session_state["user"] = fetched_user
                    user_data = fetched_user
            except Exception:
                pass

        if user_data and isinstance(user_data, dict):
            user_display_name = user_data.get("name") or user_data.get("email") or "Usuário Conectado"
        else:
            user_display_name = "Usuário Conectado"
        # Verde de logado (Conectado ao Xano)
        status_color = "#23a55a"
    else:
        # Amarelo padrão de não logado (Não conectado / Warning do app.py)
        status_color = "#ffbd45"

    discord_profile_css = f"""
    <style>
    /* =====================================================================
       OCULTAÇÃO PERMANENTE DA ABA DE PERFIL NA LISTA NATIVA SUPERIOR
       ===================================================================== */
    [data-testid="stSidebarNav"] a[href*="Perfil"],
    [data-testid="stSidebarNav"] a[href*="3_"],
    [data-testid="stSidebarNavItems"] li:has(a[href*="Perfil"]),
    [data-testid="stSidebarNavItems"] li:has(a[href*="3_"]),
    [data-testid="stSidebarNavItems"] li:nth-child(4),
    [data-testid="stSidebarNavItems"] li:last-child {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
    }}

    /* =====================================================================
       ÍCONE DO APP.PY NA NAVEGAÇÃO
       ===================================================================== */
    /* Ícone 🎓 para o app.py (Início) na lista de navegação */
    [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"]::before,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href="/"]::before,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href=""]::before,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"])::before {{
        content: "🎓" !important;
        font-size: 1.25rem !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 0.5rem !important;
        flex-shrink: 0 !important;
    }}

    /* Ajusta o texto de app.py para Início no modo expandido */
    [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href="/"] span,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) span {{
        font-size: 0 !important;
    }}
    [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] span::after,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href="/"] span::after,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) span::after {{
        content: "Início" !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }}

    /* =====================================================================
       MODO EXPANDIDO
       ===================================================================== */
    /* Cria o contexto de posicionamento apenas no modo expandido */
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) {{
        transform: translate3d(0, 0, 0) !important;
        position: relative !important;
    }}

    /* Remove o contexto de posicionamento relativo do container imediato do Streamlit */
    section[data-testid="stSidebar"] div:has(> a[data-testid="stPageLink-NavLink"][href*="Perfil"]) {{
        position: static !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Espaço extra na base do conteúdo da sidebar para evitar sobreposição */
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) div[data-testid="stSidebarUserContent"] {{
        padding-bottom: 85px !important;
    }}

    /* Botão flutuante estilo Discord fixado no canto inferior esquerdo da barra lateral (expandida) */
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"] {{
        position: fixed !important;
        bottom: 16px !important;
        left: 16px !important;
        right: 16px !important;
        width: auto !important;
        z-index: 99999 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        background-color: #232428 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
        box-sizing: border-box !important;
    }}

    section[data-testid="stSidebar"]:not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover {{
        background-color: #2b2d31 !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
        transform: translateY(-1px) !important;
    }}

    /* =====================================================================
       MODO MINIMIZADO: Barra lateral compacta exibindo APENAS OS ÍCONES
       ===================================================================== */
    section[data-testid="stSidebar"][aria-expanded="false"] {{
        width: 68px !important;
        min-width: 68px !important;
        max-width: 68px !important;
        transform: none !important;
        margin-left: 0 !important;
        transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        overflow: hidden !important;
        z-index: 100 !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] {{
        width: 68px !important;
        min-width: 68px !important;
        max-width: 68px !important;
        padding: 50px 0 75px 0 !important;
        overflow-x: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }}

    /* Oculta resize handle no modo minimizado */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarResizeHandle"] {{
        display: none !important;
    }}

    /* Elimina botão duplicado: oculta o cabeçalho/botão nativo de recolhimento no modo minimizado */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    /* Único botão de expansão (>>) visível no topo da barra minimizada */
    button[data-testid="stExpandSidebarButton"] {{
        position: fixed !important;
        top: 10px !important;
        left: 17px !important;
        z-index: 999999 !important;
        width: 34px !important;
        height: 34px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: rgba(255, 255, 255, 0.06) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: background-color 0.15s ease !important;
    }}

    button[data-testid="stExpandSidebarButton"]:hover {{
        background-color: rgba(255, 255, 255, 0.15) !important;
    }}

    /* Itens de navegação da mini-sidebar: centralizados */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] {{
        width: 100% !important;
        padding: 0 !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] {{
        width: 100% !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 6px !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Garante que a aba de perfil permaneça removida mesmo ao minimizar */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:nth-child(4),
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:last-child,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] a[href*="Perfil"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] a[href*="3_"] {{
        display: none !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"] {{
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        min-height: 44px !important;
        padding: 0 !important;
        margin: 0 auto !important;
        border-radius: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0 !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"]:hover {{
        transform: scale(1.08) !important;
    }}

    /* Oculta apenas os rótulos de texto das páginas (o segundo filho), preservando os ícones (:first-child) */
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"] > :last-child {{
        display: none !important;
    }}

    /* Oculta o texto residual exclusivo de app.py para exibir unicamente o ícone ::before (🎓) */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] > span,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"][href="/"] > span,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) > span {{
        display: none !important;
    }}

    /* Ícone 🎓 de app.py centralizado ao minimizar */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"]::before,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"][href="/"]::before,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"])::before {{
        margin-right: 0 !important;
        font-size: 22px !important;
    }}

    /* Ícones das demais páginas (📚 Disciplinas, 📝 Tarefas) visíveis e perfeitamente centralizados */
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"] > :first-child,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"] > :first-child * {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 22px !important;
        line-height: 1 !important;
        visibility: visible !important;
        opacity: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* =====================================================================
       BOTÃO DE PERFIL DISCORD (CANTO INFERIOR ESQUERDO)
       ===================================================================== */
    /* Avatar do perfil (ícone 👤 na foto de perfil do Discord) */
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"],
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child {{
        position: relative !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%) !important;
        font-size: 18px !important;
        margin-right: 12px !important;
        flex-shrink: 0 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }}

    /* Círculo preenchido de status no canto inferior direito da foto do 👤 */
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"]::after,
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child::after {{
        content: "" !important;
        position: absolute !important;
        bottom: -2px !important;
        right: -2px !important;
        width: 10px !important;
        height: 10px !important;
        border-radius: 50% !important;
        background-color: {status_color} !important;
        border: 2px solid #232428 !important;
        box-sizing: content-box !important;
        z-index: 10 !important;
    }}

    /* Nome do usuário ocupando a área de nome e status no modo expandido */
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"]:not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child {{
        display: flex !important;
        align-items: center !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #f2f3f5 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        height: 36px !important;
        line-height: 1.2 !important;
    }}

    /* Botão de Perfil minimizado: o avatar 👤 MANTÉM seu tamanho real (38x38px) e proporção sem diminuir */
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] {{
        display: flex !important;
        position: fixed !important;
        bottom: 16px !important;
        left: 15px !important;
        right: auto !important;
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        justify-content: center !important;
        align-items: center !important;
        border-radius: 50% !important;
        z-index: 99999 !important;
        transition: transform 0.15s ease !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover {{
        transform: scale(1.08) !important;
        background: transparent !important;
    }}

    /* Esconde o texto/nome de usuário ao minimizar */
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child {{
        display: none !important;
    }}

    /* Remove margem lateral no modo minimizado para centralizar perfeitamente os 38px dentro dos 68px */
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"],
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child {{
        margin-right: 0 !important;
    }}

    /* Ajuste de alertas/avisos na sidebar minimizada */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stAlert"] {{
        padding: 4px !important;
        margin: 6px auto !important;
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        overflow: hidden !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border-radius: 8px !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
        font-size: 0 !important;
        margin: 0 !important;
    }}

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p::before {{
        content: "⚠️" !important;
        font-size: 18px !important;
    }}
    </style>
    """

    st.sidebar.markdown(discord_profile_css, unsafe_allow_html=True)

    # Espaçador físico para garantir que o último botão/controle da sidebar nunca fique sobreposto
    st.sidebar.markdown(
        '<div class="sidebar-profile-spacer" style="height: 75px; min-height: 75px; width: 100%; pointer-events: none;" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    try:
        st.sidebar.page_link(
            "pages/3_👤_Perfil.py",
            label=user_display_name,
            icon="👤",
        )
    except Exception:
        pass
