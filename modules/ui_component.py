"""UI Components - Reusable UI elements."""
import streamlit as st
import config


def apply_custom_styles():
    st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    [data-testid="stSidebar"] { background-color: #f8fafc; }
    h1 { color: #1e293b; font-weight: 700; }
    h2 { color: #334155; font-weight: 600; }
    h3 { color: #475569; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown(f"<h1 style='text-align:center;'>{config.APP_ICON}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;color:#4F46E5;'>{config.APP_TITLE}</h2>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### Navigation")
        pages = {
            "Dashboard": "🏠", "Upload Notes": "📤", "AI Tutor": "🤖",
            "Summary": "📝", "Quiz Generator": "❓", "Flashcards": "🎴", "Study Planner": "📅",
        }
        selected = st.radio("Go to", list(pages.keys()), format_func=lambda x: f"{pages[x]} {x}", label_visibility="collapsed")

        st.markdown("---")
        st.markdown("### API Status")
        from config import check_api_keys
        is_valid, msg = check_api_keys()
        if is_valid:
            st.success("Connected")
        else:
            st.error("Not Connected")
            st.caption(msg)

        st.markdown("---")
        st.caption("Made with ❤️ for students")

        return selected


def render_header(title, subtitle=""):
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color:#64748b;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")


def render_info_box(message, box_type="info"):
    if box_type == "info":
        st.info(message)
    elif box_type == "warning":
        st.warning(message)
    elif box_type == "success":
        st.success(message)


def render_metric_card(title, value, icon="📊"):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:1.5rem;border-radius:10px;text-align:center;">
        <div style="font-size:2rem;">{icon}</div>
        <div style="font-size:2rem;font-weight:bold;">{value}</div>
        <div style="font-size:0.9rem;opacity:0.9;">{title}</div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role, content, sources=None):
    if role == "user":
        st.markdown(f"<div style='background:#e0e7ff;padding:1rem;border-radius:10px;margin-left:20%;'><b>You:</b><br>{content}</div>", unsafe_allow_html=True)
    else:
        sources_html = f"<br><small>Sources: {', '.join(sources)}</small>" if sources else ""
        st.markdown(f"<div style='background:#f3f4f6;padding:1rem;border-radius:10px;margin-right:20%;'><b>AI Tutor:</b><br>{content}{sources_html}</div>", unsafe_allow_html=True)


def render_footer():
    st.markdown("---")
    st.markdown("<div style='text-align:center;color:#94a3b8;'>AI Study Assistant | Built with Streamlit & LangChain</div>", unsafe_allow_html=True)
