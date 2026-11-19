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
       ÍCONE DO APP.PY NA NAVEGAÇÃO E RENOMEAÇÃO PARA EDUTRACK AI
       ===================================================================== */
    /* Garante que links de outras páginas não tenham ::before do EduTrack AI */
    [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"]::before {{
        content: none !important;
        display: none !important;
    }}

    /* Ícone 🎓 para o app.py (EduTrack AI) na lista de navegação */
    [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"]::before,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href="/"]::before,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href=""]::before,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"])::before {{
        content: "🎓" !important;
        font-size: 20px !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 24px !important;
        height: 24px !important;
        margin-right: 0.5rem !important;
        flex-shrink: 0 !important;
    }}

    /* Renomeia o texto de app.py para "EduTrack AI" no modo expandido */
    [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href="/"] span,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) span {{
        font-size: 0 !important;
    }}
    [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] span::after,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"][href="/"] span::after,
    [data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) span::after {{
        content: "EduTrack AI" !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        visibility: visible !important;
        display: inline-block !important;
        height: auto !important;
    }}

    /* =====================================================================
       ANIMAÇÃO SUAVE DE MINIMIZAR E MAXIMIZAR A BARRA LATERAL
       ===================================================================== */
    section[data-testid="stSidebar"] {{
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    min-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    min-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    padding 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {{
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                    background-color 0.15s ease,
                    transform 0.15s cubic-bezier(0.4, 0, 0.2, 1),
                    box-shadow 0.15s ease !important;
    }}

    /* =====================================================================
       MODO EXPANDIDO: PADRONIZAÇÃO DE TAMANHO (40PX), POSIÇÃO E ESTILO
       ===================================================================== */
    /* Cria o contexto de posicionamento apenas no modo expandido */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]),
    section[data-testid="stSidebar"][data-collapsed="false"] {{
        transform: translate3d(0, 0, 0) !important;
        position: relative !important;
    }}

    /* Remove o contexto de posicionamento relativo do container imediato do Streamlit */
    section[data-testid="stSidebar"] div:has(> a[data-testid="stPageLink-NavLink"][href*="Perfil"]) {{
        position: static !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Cabeçalho expandido com botão de recolhimento padronizado em 40x40px */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarHeader"] {{
        height: 60px !important;
        min-height: 60px !important;
        max-height: 60px !important;
        box-sizing: border-box !important;
        padding: 10px 14px !important;
        display: flex !important;
        align-items: center !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarCollapseButton"] button,
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarCollapseButton"] button {{
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarCollapseButton"] button:hover,
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarCollapseButton"] button:hover {{
        background-color: rgba(255, 255, 255, 0.15) !important;
        transform: scale(1.08) !important;
    }}

    /* Lista de navegação no modo expandido: alinhamento e espaçamento consistente */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarNav"] {{
        padding: 0 !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarNavItems"],
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarNavItems"] {{
        padding: 0 14px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarNavItems"] li,
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarNavItems"] li {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }}

    /* Botões das páginas no modo expandido: altura exata de 40px e bordas de 10px */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) a[data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"][data-collapsed="false"] a[data-testid="stSidebarNavLink"] {{
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
        border-radius: 10px !important;
        padding: 0 10px !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 10px !important;
        transition: background-color 0.15s ease, transform 0.15s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.15s ease !important;
    }}

    /* Animação idêntica ao minimizar: efeito de sobreposição (hover) com leve escala suave */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) a[data-testid="stSidebarNavLink"]:hover,
    section[data-testid="stSidebar"][data-collapsed="false"] a[data-testid="stSidebarNavLink"]:hover {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        transform: scale(1.04) !important;
        transform-origin: center left !important;
    }}

    /* Ícones das páginas no modo expandido padronizados em 20px */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child,
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child *,
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child,
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child * {{
        font-size: 20px !important;
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 20px !important;
        height: 20px !important;
        margin: 0 !important;
        padding: 0 !important;
        flex-shrink: 0 !important;
    }}

    /* =====================================================================
       ALERTA PERSONALIZADO "NÃO CONECTADO" (substitui st.sidebar.warning)
       ===================================================================== */

    /* Modo expandido: linha horizontal com ícone + texto */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) .edutrack-alert-warning,
    section[data-testid="stSidebar"][data-collapsed="false"] .edutrack-alert-warning {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 10px !important;
        height: 40px !important;
        box-sizing: border-box !important;
        padding: 0 10px !important;
        margin: 0 !important;
        border-radius: 10px !important;
        width: 100% !important;
        background-color: rgba(255, 193, 7, 0.15) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        cursor: default !important;
    }}

    /* Zera o container do Streamlit que envolve o nosso div no modo expandido */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stMarkdownContainer"]:has(.edutrack-alert-warning),
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stMarkdownContainer"]:has(.edutrack-alert-warning) {{
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) .edutrack-alert-icon,
    section[data-testid="stSidebar"][data-collapsed="false"] .edutrack-alert-icon {{
        font-size: 20px !important;
        line-height: 1 !important;
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 20px !important;
        height: 20px !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) .edutrack-alert-text,
    section[data-testid="stSidebar"][data-collapsed="false"] .edutrack-alert-text {{
        font-size: 0.875rem !important;
        line-height: 1 !important;
        color: inherit !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        flex: 1 !important;
        min-width: 0 !important;
    }}

    /* Modo minimizado: apenas ícone 40x40 */
    section[data-testid="stSidebar"][data-collapsed="true"] .edutrack-alert-warning,
    section[data-testid="stSidebar"][aria-expanded="false"] .edutrack-alert-warning {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        box-sizing: border-box !important;
        padding: 0 !important;
        margin: 0 auto !important;
        border-radius: 10px !important;
        background-color: rgba(255, 193, 7, 0.15) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        cursor: default !important;
    }}

    /* Zera o container do Streamlit que envolve o nosso div no minimizado */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stMarkdownContainer"]:has(.edutrack-alert-warning),
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stMarkdownContainer"]:has(.edutrack-alert-warning) {{
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] .edutrack-alert-icon,
    section[data-testid="stSidebar"][aria-expanded="false"] .edutrack-alert-icon {{
        font-size: 20px !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: auto !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] .edutrack-alert-text,
    section[data-testid="stSidebar"][aria-expanded="false"] .edutrack-alert-text {{
        display: none !important;
    }}

    /* Espaço extra na base do conteúdo da sidebar para evitar sobreposição */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) div[data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"][data-collapsed="false"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"][data-collapsed="false"] div[data-testid="stSidebarUserContent"] {{
        padding-bottom: 85px !important;
    }}

    /* Botão flutuante estilo Discord fixado no canto inferior da barra lateral (expandida) */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"],
    section[data-testid="stSidebar"][data-collapsed="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] {{
        position: fixed !important;
        bottom: 16px !important;
        left: 14px !important;
        right: 14px !important;
        height: 52px !important;
        min-height: 52px !important;
        max-height: 52px !important;
        box-sizing: border-box !important;
        width: auto !important;
        z-index: 99999 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        padding: 6px 10px !important;
        border-radius: 10px !important;
        background-color: #232428 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
    }}

    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover,
    section[data-testid="stSidebar"][data-collapsed="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover {{
        background-color: #2b2d31 !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
        transform: scale(1.03) !important;
        transform-origin: center left !important;
    }}

    /* =====================================================================
       MODO MINIMIZADO: BARRA LATERAL COMPACTA (ALINHAMENTO E TAMANHO IDÊNTICOS)
       ===================================================================== */
    section[data-testid="stSidebar"][data-collapsed="true"],
    section[data-testid="stSidebar"][aria-expanded="false"] {{
        width: 68px !important;
        min-width: 68px !important;
        max-width: 68px !important;
        transform: none !important;
        margin-left: 0 !important;
        overflow: hidden !important;
        z-index: 100 !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] {{
        width: 68px !important;
        min-width: 68px !important;
        max-width: 68px !important;
        padding: 60px 0 75px 0 !important;
        overflow-x: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarUserContent"] {{
        width: 68px !important;
        min-width: 68px !important;
        max-width: 68px !important;
        padding: 0 !important;
        margin: 0 auto !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }}

    /* Oculta resize handle no modo minimizado */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarResizeHandle"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarResizeHandle"] {{
        display: none !important;
    }}

    /* Elimina botão duplicado: oculta o cabeçalho/botão nativo de recolhimento no modo minimizado */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}

    /* Único botão de expansão (>>) visível no topo da barra minimizada (padronizado em 40x40px) */
    button[data-testid="stExpandSidebarButton"] {{
        position: fixed !important;
        top: 10px !important;
        left: 14px !important;
        z-index: 999999 !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
    }}

    button[data-testid="stExpandSidebarButton"]:hover {{
        background-color: rgba(255, 255, 255, 0.15) !important;
        transform: scale(1.08) !important;
    }}

    /* Itens de navegação da mini-sidebar: centralizados com alinhamento vertical e gap idênticos ao modo normal */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] {{
        width: 100% !important;
        padding: 0 !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] {{
        width: 100% !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 6px !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Garante que a aba de perfil permaneça removida mesmo ao minimizar */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:nth-child(4),
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:last-child,
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNav"] a[href*="Perfil"],
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNav"] a[href*="3_"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:nth-child(4),
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:last-child,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] a[href*="Perfil"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"] a[href*="3_"] {{
        display: none !important;
    }}

    /* Links da sidebar minimizada: botões quadrados centralizados padronizados em 40x40px */
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"] {{
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
        padding: 0 !important;
        margin: 0 auto !important;
        border-radius: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0 !important;
        overflow: hidden !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stSidebarNavLink"]:hover,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"]:hover {{
        transform: scale(1.08) !important;
        transform-origin: center !important;
    }}

    /* =====================================================================
       ÍCONES DAS PÁGINAS NO MODO MINIMIZADO
       ===================================================================== */
    /* 1. Página principal app.py (EduTrack AI): oculta o texto span e centraliza o ícone ::before (🎓) */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] span,
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) span,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"] span,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"]) span {{
        display: none !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"]::before,
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"])::before,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:first-child a[data-testid="stSidebarNavLink"]::before,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stSidebarNavLink"]:not([href*="Disciplinas"]):not([href*="Tarefas"]):not([href*="Perfil"])::before {{
        content: "🎓" !important;
        font-size: 20px !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}

    /* 2. Demais páginas (📚 Disciplinas, 📝 Tarefas):
          Oculta apenas o rótulo de texto (:last-child) e exibe o ícone nativo (:first-child) centralizado */
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :last-child,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :last-child {{
        display: none !important;
    }}

    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child,
    section[data-testid="stSidebar"][data-collapsed="true"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child *,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNavItems"] li:not(:first-child) a[data-testid="stSidebarNavLink"] > :first-child * {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 20px !important;
        line-height: 1 !important;
        visibility: visible !important;
        opacity: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* =====================================================================
       BOTÃO DE PERFIL DISCORD (CANTO INFERIOR ESQUERDO)
       ===================================================================== */
    /* Avatar do perfil (ícone 👤 na foto de perfil do Discord): 40x40px */
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"],
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child {{
        position: relative !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        min-height: 40px !important;
        max-width: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%) !important;
        font-size: 19px !important;
        margin-right: 10px !important;
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
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"]:not([data-collapsed="true"]):not([aria-expanded="false"]) a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child,
    section[data-testid="stSidebar"][data-collapsed="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"][data-collapsed="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child {{
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

    /* Botão de Perfil minimizado: padronizado em 40x40px */
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stPageLink-NavLink"][href*="Perfil"],
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] {{
        display: flex !important;
        position: fixed !important;
        bottom: 16px !important;
        left: 14px !important;
        right: auto !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
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

    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover {{
        transform: scale(1.08) !important;
        background: transparent !important;
    }}

    /* Avatar do perfil no modo minimizado (40x40px) */
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"],
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"],
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child {{
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        box-sizing: border-box !important;
        margin-right: 0 !important;
        border-radius: 50% !important;
        font-size: 19px !important;
    }}

    /* Esconde o texto/nome de usuário ao minimizar */
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"][data-collapsed="true"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child,
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child {{
        display: none !important;
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
