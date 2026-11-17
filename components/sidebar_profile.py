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
    /* Oculta o link padrão de perfil na lista de páginas superior da sidebar */
    [data-testid="stSidebarNav"] a[href*="Perfil"],
    [data-testid="stSidebarNavItems"] li:has(a[href*="Perfil"]),
    [data-testid="stSidebarNavItems"] li:has(a[href*="3_"]) {{
        display: none !important;
    }}

    /* Cria o contexto de posicionamento na barra lateral */
    section[data-testid="stSidebar"] {{
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
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {{
        padding-bottom: 85px !important;
    }}

    /* Botão flutuante estilo Discord fixado no canto inferior esquerdo da barra lateral */
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] {{
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

    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"]:hover {{
        background-color: #2b2d31 !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
        transform: translateY(-1px) !important;
    }}

    /* Esconde o botão e espaçador se a sidebar for recolhida */
    section[data-testid="stSidebar"][aria-expanded="false"] a[data-testid="stPageLink-NavLink"][href*="Perfil"],
    section[data-testid="stSidebar"][aria-expanded="false"] .sidebar-profile-spacer {{
        display: none !important;
    }}

    /* Avatar do perfil (ícone 👤 na foto de perfil do Discord) */
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Icon"],
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :first-child {{
        position: relative !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
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

    /* Nome do usuário ocupando a área de nome e status */
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] [data-testid="stPageLink-Label"],
    section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][href*="Perfil"] > :last-child {{
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
