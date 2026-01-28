import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="공지 허브 - BuyLow", page_icon="📢", layout="wide", initial_sidebar_state="expanded")
render_sidebar()

# CSS (공통 스타일)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #0f0f14;
        --bg-card: #18181f;
        --bg-card-hover: #1e1e28;
        --border: rgba(255,255,255,0.08);
        --text-primary: #ffffff;
        --text-secondary: rgba(255,255,255,0.6);
        --text-muted: rgba(255,255,255,0.4);
        --accent-primary: #6366f1;
        --accent-glow: rgba(99, 102, 241, 0.3);
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    .stApp {
        background: var(--bg-dark);
        background-image: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.12), transparent);
    }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .page-header { padding: 2rem 0; animation: fadeInUp 0.6s ease-out; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    .page-subtitle { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-secondary); margin-top: 0.25rem; }
    
    .tag-filter { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }
    .tag-btn { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; padding: 0.5rem 1rem; border-radius: 20px; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-secondary); cursor: pointer; transition: all 0.2s ease; }
    .tag-btn:hover, .tag-btn.active { background: var(--accent-primary); color: white; border-color: var(--accent-primary); }
    
    .announcement-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; transition: all 0.3s ease; }
    .announcement-card:hover { border-color: var(--accent-primary); transform: translateY(-4px); }
    .announcement-card.pinned { border-left: 4px solid var(--warning); }
    
    .announcement-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem; }
    .announcement-title { font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0; }
    .announcement-meta { display: flex; gap: 0.5rem; align-items: center; }
    .announcement-tag { font-family: 'Noto Sans KR', sans-serif; font-size: 0.7rem; padding: 0.25rem 0.6rem; border-radius: 12px; background: rgba(99,102,241,0.2); color: var(--accent-primary); }
    .announcement-date { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--text-muted); }
    .pin-badge { font-size: 0.7rem; padding: 0.2rem 0.5rem; border-radius: 8px; background: rgba(245,158,11,0.2); color: var(--warning); }
    
    .announcement-content { font-family: 'Noto Sans KR', sans-serif; font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; white-space: pre-wrap; margin: 1rem 0; }
    
    .action-buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); }
    .action-btn { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; padding: 0.5rem 1rem; border-radius: 8px; background: var(--bg-dark); border: 1px solid var(--border); color: var(--text-secondary); cursor: pointer; transition: all 0.2s ease; text-decoration: none; }
    .action-btn:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
    
    .telegram-links { display: flex; gap: 1rem; margin: 1rem 0; padding: 1rem; background: var(--bg-card); border-radius: 12px; }
    .tg-link { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--accent-primary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
    .tg-link:hover { text-decoration: underline; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1rem; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 1000px; }
</style>
""", unsafe_allow_html=True)

ANNOUNCEMENTS_PATH = Path("data/announcements.json")

def load_announcements():
    if ANNOUNCEMENTS_PATH.exists():
        with open(ANNOUNCEMENTS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 텔레그램 링크 (데모용)
st.markdown("""
<div class="telegram-links">
    <a href="https://t.me/buylow_channel" target="_blank" class="tg-link">📢 공식 채널</a>
    <a href="https://t.me/buylow_cs" target="_blank" class="tg-link">💬 CS 문의</a>
</div>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📢 공지 허브</h1>
    <p class="page-subtitle">모든 공지를 한 곳에서 확인하세요</p>
</div>
""", unsafe_allow_html=True)

announcements = load_announcements()

# 태그 필터
all_tags = list(set(a.get('tag', '기타') for a in announcements))
all_tags = ["전체"] + sorted(all_tags)

col1, col2 = st.columns([3, 1])
with col1:
    selected_tag = st.selectbox("태그 필터", all_tags, label_visibility="collapsed")
with col2:
    search_query = st.text_input("검색", placeholder="🔍 검색...", label_visibility="collapsed")

# 필터링
filtered = announcements
if selected_tag != "전체":
    filtered = [a for a in filtered if a.get('tag') == selected_tag]
if search_query:
    filtered = [a for a in filtered if search_query.lower() in a.get('title', '').lower() or search_query.lower() in a.get('content', '').lower()]

# 고정 공지 먼저, 그 다음 날짜순
pinned = [a for a in filtered if a.get('pinned')]
not_pinned = [a for a in filtered if not a.get('pinned')]
sorted_announcements = pinned + sorted(not_pinned, key=lambda x: x.get('created_at', ''), reverse=True)

st.markdown(f"**{len(sorted_announcements)}개의 공지**")

# 공지 표시
for ann in sorted_announcements:
    pinned_badge = '<span class="pin-badge">📌 고정</span>' if ann.get('pinned') else ''
    
    st.markdown(f"""
    <div class="announcement-card {'pinned' if ann.get('pinned') else ''}">
        <div class="announcement-header">
            <h3 class="announcement-title">{ann.get('title', '제목 없음')}</h3>
            <div class="announcement-meta">
                <span class="announcement-tag">{ann.get('tag', '기타')}</span>
                {pinned_badge}
                <span class="announcement-date">{ann.get('created_at', '')[:10]}</span>
            </div>
        </div>
        <div class="announcement-content">{ann.get('content', '')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 액션 버튼
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📋 복사", key=f"copy_{ann.get('id')}"):
            st.code(f"{ann.get('title')}\n\n{ann.get('content')}", language=None)
            st.success("위 내용을 복사해서 텔레그램에 붙여넣기 하세요!")
    with col2:
        if "과제" in str(ann.get('next_actions', [])):
            if st.button("📤 과제방", key=f"hw_{ann.get('id')}"):
                st.switch_page("pages/03_homework.py")
    with col3:
        if "교육" in str(ann.get('next_actions', [])):
            if st.button("📚 교육", key=f"edu_{ann.get('id')}"):
                st.switch_page("pages/09_content_library.py")
    with col4:
        if st.button("🎫 티켓", key=f"ticket_{ann.get('id')}"):
            st.switch_page("pages/01_cs_chat.py")

if not sorted_announcements:
    st.info("해당하는 공지가 없습니다.")

# 면책 문구
st.markdown("""
<div class="disclaimer">
    ⚠️ 본 공지는 교육 및 정보 제공 목적입니다. 매매 추천, 가격 예측, 종목 추천이 아니며 투자 권유가 아닙니다.
</div>
""", unsafe_allow_html=True)

# 네비게이션
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 홈", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("💬 CS 챗봇", use_container_width=True):
        st.switch_page("pages/01_cs_chat.py")
with col3:
    if st.button("📚 교육 콘텐츠", use_container_width=True):
        st.switch_page("pages/09_content_library.py")
