import streamlit as st

NAV_ITEMS = [
    ("홈", "Home.py", "🏠"),
    ("CS 챗봇", "pages/01_cs_chat.py", "💬"),
    ("진단 퀴즈", "pages/02_quiz.py", "🧭"),
    ("과제 제출", "pages/03_homework.py", "📤"),
    ("리스크 체크", "pages/04_risk_check.py", "🛡️"),
    ("관리자", "pages/05_admin.py", "⚙️"),
    ("공지 허브", "pages/06_announcements.py", "📢"),
    ("온보딩", "pages/07_onboarding.py", "🚀"),
    ("운영자 대시보드", "pages/08_operator_dashboard.py", "📊"),
    ("교육 콘텐츠", "pages/09_content_library.py", "📚"),
    ("과제 채점", "pages/10_grading_assistant.py", "✏️"),
    ("언락 해설", "pages/11_unlocked_lessons.py", "🔓"),
    ("심화 연습", "pages/12_advanced_practice.py", "🎯"),
]


def render_sidebar():
    # 기본 페이지 네비 숨기기
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] { display: none !important; }
            [data-testid="stSidebar"] { padding-top: 0.75rem; }
            .sidebar-title { font-weight: 700; font-size: 1rem; margin: 0.5rem 0 1rem 0; color: #e5e7eb; }
            .stButton { margin-bottom: 0.45rem; }
            .stButton > button {
                width: 100%;
                text-align: left;
                padding: 0.55rem 0.85rem;
                border-radius: 999px;
                border: 1px solid transparent;
                background: transparent;
                color: #e2e8f0;
                box-shadow: none;
                transition: all 0.25s ease;
            }
            .stButton > button:hover {
                border-color: rgba(99,102,241,0.35);
                background: rgba(99,102,241,0.08);
                transform: translateY(0);
            }
            .stButton > button:active {
                transform: translateY(0);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="sidebar-title">BuyLow OS</div>', unsafe_allow_html=True)
    for label, path, icon in NAV_ITEMS:
        st.sidebar.page_link(path, label=f"{icon} {label}")
