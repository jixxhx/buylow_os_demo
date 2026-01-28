import streamlit as st
import json
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="교육 콘텐츠 - BuyLow", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
render_sidebar()

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #0f0f14;
        --bg-card: #18181f;
        --border: rgba(255,255,255,0.08);
        --text-primary: #ffffff;
        --text-secondary: rgba(255,255,255,0.6);
        --text-muted: rgba(255,255,255,0.4);
        --accent-primary: #6366f1;
        --success: #22c55e;
        --warning: #f59e0b;
    }
    
    .stApp { background: var(--bg-dark); background-image: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.12), transparent); }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .page-header { padding: 2rem 0; animation: fadeInUp 0.6s ease-out; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    .page-subtitle { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-secondary); margin-top: 0.25rem; }
    
    .chapter-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .chapter-title { font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
    
    .content-item { background: var(--bg-dark); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; margin: 0.75rem 0; transition: all 0.3s ease; }
    .content-item:hover { border-color: var(--accent-primary); transform: translateX(8px); }
    
    .content-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem; }
    .content-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin: 0; }
    .content-meta { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
    .version-badge { font-family: 'Space Mono', monospace; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 8px; background: rgba(99,102,241,0.2); color: var(--accent-primary); }
    .date-badge { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: var(--text-muted); }
    
    .changelog { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--warning); background: rgba(245,158,11,0.1); border-radius: 8px; padding: 0.5rem 0.75rem; margin: 0.5rem 0; }
    
    .sections-list { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0; }
    .section-tag { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-secondary); background: var(--bg-card); padding: 0.35rem 0.75rem; border-radius: 16px; border: 1px solid var(--border); }
    
    .homework-link { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--success); margin-top: 0.5rem; }
    
    .learning-order { background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05)); border: 1px solid var(--accent-primary); border-radius: 16px; padding: 1.5rem; margin: 1.5rem 0; }
    .order-title { font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; }
    .order-item { display: flex; align-items: center; gap: 1rem; padding: 0.5rem 0; }
    .order-num { font-family: 'Space Mono', monospace; font-size: 1rem; font-weight: 700; color: var(--accent-primary); width: 28px; height: 28px; background: rgba(99,102,241,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .order-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.95rem; color: var(--text-secondary); }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1.5rem; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 1000px; }
</style>
""", unsafe_allow_html=True)

CONTENT_PATH = Path("data/content_versions.json")

def load_contents():
    if CONTENT_PATH.exists():
        with open(CONTENT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📚 교육 콘텐츠 라이브러리</h1>
    <p class="page-subtitle">버전 관리되는 교육 자료를 확인하세요</p>
</div>
""", unsafe_allow_html=True)

# 학습 순서 안내
st.markdown("""
<div class="learning-order">
    <p class="order-title">📋 권장 학습 순서</p>
    <div class="order-item"><span class="order-num">1</span><span class="order-text">다이버전스 기초</span></div>
    <div class="order-item"><span class="order-num">2</span><span class="order-text">지지와 저항</span></div>
    <div class="order-item"><span class="order-num">3</span><span class="order-text">SRL 지표 설정</span></div>
    <div class="order-item"><span class="order-num">4</span><span class="order-text">아래꼬리 캔들 분석</span></div>
    <div class="order-item"><span class="order-num">5</span><span class="order-text">손절과 포지션 사이징</span></div>
</div>
""", unsafe_allow_html=True)

contents = load_contents()

# 챕터별 그룹화
chapters = {}
for content in contents:
    chapter = content.get('chapter', '기타')
    if chapter not in chapters:
        chapters[chapter] = []
    chapters[chapter].append(content)

# 콘텐츠 표시
for chapter, items in chapters.items():
    st.markdown(f"""
    <div class="chapter-card">
        <p class="chapter-title">📖 {chapter}</p>
    </div>
    """, unsafe_allow_html=True)
    
    for item in items:
        sections_html = ''.join([f'<span class="section-tag">{s}</span>' for s in item.get('sections', [])])
        homework_html = f'<p class="homework-link">📝 관련 과제: {item.get("related_homework")}</p>' if item.get('related_homework') else ''
        
        st.markdown(f"""
        <div class="content-item">
            <div class="content-header">
                <h3 class="content-title">{item.get('title', '제목 없음')}</h3>
                <div class="content-meta">
                    <span class="version-badge">v{item.get('version', '1.0')}</span>
                    <span class="date-badge">{item.get('uploaded_at', '')[:10]}</span>
                </div>
            </div>
            <div class="changelog">📌 변경점: {item.get('changelog', '없음')}</div>
            <div class="sections-list">{sections_html}</div>
            {homework_html}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if item.get('related_homework'):
                if st.button(f"📤 과제 제출", key=f"hw_{item.get('id')}"):
                    st.switch_page("pages/03_homework.py")
        with col2:
            if st.button(f"🔓 해설 보기", key=f"lesson_{item.get('id')}"):
                st.switch_page("pages/11_unlocked_lessons.py")

# 면책 문구
st.markdown("""
<div class="disclaimer">
    ⚠️ 본 교육 콘텐츠는 교육 및 정보 제공 목적입니다. 매매 추천, 가격 예측, 종목 추천이 아니며 투자 권유가 아닙니다. 모든 투자 결정은 본인 책임입니다.
</div>
""", unsafe_allow_html=True)

# 네비게이션
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 홈", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📤 과제 제출", use_container_width=True):
        st.switch_page("pages/03_homework.py")
with col3:
    if st.button("🔓 해설 모음", use_container_width=True):
        st.switch_page("pages/11_unlocked_lessons.py")
