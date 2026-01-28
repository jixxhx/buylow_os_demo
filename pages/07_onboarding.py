import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="온보딩 - BuyLow", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")
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
    
    .page-header { padding: 2rem 0; animation: fadeInUp 0.6s ease-out; text-align: center; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    .page-subtitle { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-secondary); margin-top: 0.5rem; }
    
    .progress-container { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; animation: fadeInUp 0.5s ease-out; }
    .progress-bar { height: 12px; background: var(--bg-dark); border-radius: 6px; overflow: hidden; margin: 1rem 0; }
    .progress-fill { height: 100%; background: linear-gradient(90deg, #6366f1, #22c55e); border-radius: 6px; transition: width 0.5s ease; }
    .progress-text { font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; color: var(--accent-primary); }
    
    .checklist-section { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out backwards; }
    .section-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
    .section-title span { font-size: 1.25rem; }
    
    .checklist-item { display: flex; align-items: center; gap: 1rem; padding: 0.75rem 0; border-bottom: 1px solid var(--border); }
    .checklist-item:last-child { border-bottom: none; }
    .check-icon { font-size: 1.25rem; }
    .check-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.95rem; color: var(--text-secondary); flex: 1; }
    .check-text.completed { color: var(--success); text-decoration: line-through; }
    
    .grade-preview { background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05)); border: 1px solid var(--accent-primary); border-radius: 16px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; }
    .grade-title { font-family: 'Outfit', sans-serif; font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem; }
    .grade-name { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: var(--warning); }
    .grade-desc { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1.5rem; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 800px; }
</style>
""", unsafe_allow_html=True)

PROFILES_PATH = Path("data/member_profiles.json")

def load_profiles():
    if PROFILES_PATH.exists():
        with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(PROFILES_PATH, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">🚀 온보딩</h1>
    <p class="page-subtitle">BuyLow에 오신 것을 환영합니다!<br>첫날 해야 할 것들을 확인해보세요.</p>
</div>
""", unsafe_allow_html=True)

# 닉네임 입력 (데모용 식별)
if 'nickname' not in st.session_state:
    st.session_state.nickname = ''

nickname = st.text_input("닉네임을 입력하세요 (데모용)", value=st.session_state.nickname, placeholder="예: trader_kim")

if nickname:
    st.session_state.nickname = nickname
    
    profiles = load_profiles()
    
    # 새 멤버 생성
    if nickname not in profiles:
        profiles[nickname] = {
            "nickname": nickname,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "onboarding_completed": False,
            "onboarding_checklist": {
                "membership_confirmed": False,
                "education_order_checked": False,
                "homework_method_checked": False,
                "nickname_rule_checked": False,
                "faq_checked": False,
                "cs_rule_checked": False
            },
            "grade": "브론즈",
            "points": 0,
            "homework_count": 0,
            "homework_streak": 0,
            "last_homework_date": None,
            "risk_violations": 0,
            "self_resolved_ratio": 0
        }
        save_profiles(profiles)
    
    profile = profiles[nickname]
    checklist = profile.get('onboarding_checklist', {})
    
    # 진행률 계산
    total_items = 6
    completed_items = sum(1 for v in checklist.values() if v)
    progress_pct = int((completed_items / total_items) * 100)
    
    st.markdown(f"""
    <div class="progress-container">
        <p class="progress-text">{progress_pct}% 완료</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_pct}%;"></div>
        </div>
        <p style="font-family: 'Noto Sans KR', sans-serif; color: var(--text-muted); font-size: 0.85rem;">{completed_items}/{total_items} 항목 완료</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 첫날 해야 할 것 (3가지)
    st.markdown("""
    <div class="checklist-section" style="animation-delay: 0.1s;">
        <div class="section-title"><span>📋</span> 첫날 해야 할 것</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        c1 = st.checkbox("", value=checklist.get('membership_confirmed', False), key="c1")
    with col2:
        st.markdown(f"**멤버십 입장 확인** {'✅' if c1 else ''}")
        st.caption("텔레그램 채널과 그룹에 입장되었는지 확인하세요")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        c2 = st.checkbox("", value=checklist.get('education_order_checked', False), key="c2")
    with col2:
        st.markdown(f"**교육 자료 읽는 순서 확인** {'✅' if c2 else ''}")
        st.caption("Trading 2 → 다이버전스 → 지지저항 → SRL → 아래꼬리 캔들 순서로 학습")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        c3 = st.checkbox("", value=checklist.get('homework_method_checked', False), key="c3")
    with col2:
        st.markdown(f"**과제 제출 방법 확인** {'✅' if c3 else ''}")
        st.caption("웹에서 주제 선택 후 분석 내용 작성, 제출 시 추가 콘텐츠 언락")
    
    # 계정 세팅
    st.markdown("""
    <div class="checklist-section" style="animation-delay: 0.2s;">
        <div class="section-title"><span>⚙️</span> 계정 세팅</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        c4 = st.checkbox("", value=checklist.get('nickname_rule_checked', False), key="c4")
    with col2:
        st.markdown(f"**닉네임 규칙 확인** {'✅' if c4 else ''}")
        st.caption("텔레그램과 웹에서 동일한 닉네임 사용 권장")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        c5 = st.checkbox("", value=checklist.get('faq_checked', False), key="c5")
    with col2:
        st.markdown(f"**질문 전 확인할 공지 읽기** {'✅' if c5 else ''}")
        st.caption("공지 허브에서 자주 묻는 질문 먼저 확인")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        c6 = st.checkbox("", value=checklist.get('cs_rule_checked', False), key="c6")
    with col2:
        st.markdown(f"**CS 티켓 규칙 확인** {'✅' if c6 else ''}")
        st.caption("CS 챗봇 → FAQ 확인 → 해결 안 되면 티켓 생성")
    
    # 저장
    if st.button("💾 진행상황 저장", type="primary", use_container_width=True):
        checklist['membership_confirmed'] = c1
        checklist['education_order_checked'] = c2
        checklist['homework_method_checked'] = c3
        checklist['nickname_rule_checked'] = c4
        checklist['faq_checked'] = c5
        checklist['cs_rule_checked'] = c6
        
        profile['onboarding_checklist'] = checklist
        profile['onboarding_completed'] = all(checklist.values())
        
        profiles[nickname] = profile
        save_profiles(profiles)
        st.success("✅ 저장되었습니다!")
        st.rerun()
    
    # 등급 미리보기
    st.markdown(f"""
    <div class="grade-preview">
        <p class="grade-title">현재 등급</p>
        <p class="grade-name">🥉 {profile.get('grade', '브론즈')}</p>
        <p class="grade-desc">과제 제출과 리스크 관리로 등급을 올릴 수 있어요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 온보딩 완료 시 축하
    if profile.get('onboarding_completed'):
        st.balloons()
        st.success("🎉 온보딩 완료! 이제 교육을 시작해보세요.")

else:
    st.info("닉네임을 입력하면 온보딩 체크리스트가 표시됩니다.")

# 면책 문구
st.markdown("""
<div class="disclaimer">
    ⚠️ 본 시스템은 교육 목적입니다. 매매 추천, 가격 예측, 종목 추천이 아니며 투자 권유가 아닙니다.
</div>
""", unsafe_allow_html=True)

# 네비게이션
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 홈", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📢 공지 허브", use_container_width=True):
        st.switch_page("pages/06_announcements.py")
with col3:
    if st.button("📚 교육 시작", use_container_width=True):
        st.switch_page("pages/09_content_library.py")
