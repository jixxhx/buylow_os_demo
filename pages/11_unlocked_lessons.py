import streamlit as st
import json
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="해설 콘텐츠 - BuyLow", page_icon="🔓", layout="wide", initial_sidebar_state="expanded")
render_sidebar()

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
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
    
    .lesson-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; transition: all 0.3s ease; }
    .lesson-card.unlocked { border-left: 4px solid var(--success); }
    .lesson-card.locked { border-left: 4px solid var(--text-muted); opacity: 0.7; }
    
    .lesson-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
    .lesson-title { font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0; }
    .status-badge { font-family: 'Noto Sans KR', sans-serif; font-size: 0.75rem; padding: 0.3rem 0.75rem; border-radius: 12px; }
    .status-unlocked { background: rgba(34,197,94,0.2); color: var(--success); }
    .status-locked { background: rgba(255,255,255,0.1); color: var(--text-muted); }
    
    .unlock-condition { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--warning); background: rgba(245,158,11,0.1); border-radius: 8px; padding: 0.5rem 0.75rem; margin: 0.5rem 0; }
    
    .lesson-content { font-family: 'Noto Sans KR', sans-serif; font-size: 0.95rem; color: var(--text-secondary); line-height: 1.8; white-space: pre-wrap; background: var(--bg-dark); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; }
    
    .tip-box { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 1rem; margin: 1rem 0; }
    .tip-title { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 700; color: var(--accent-primary); margin-bottom: 0.5rem; }
    .tip-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); }
    
    .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin: 1rem 0; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 900px; }
</style>
""", unsafe_allow_html=True)

UNLOCKS_PATH = Path("data/unlocks.json")

def load_unlocks():
    if UNLOCKS_PATH.exists():
        with open(UNLOCKS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 해설 콘텐츠 데이터
LESSONS = {
    "divergence_lesson": {
        "title": "📊 다이버전스 심화 해설",
        "topic": "다이버전스",
        "unlock_condition": "다이버전스 과제 1회 제출",
        "content": """다이버전스 심화 해설

1. 다이버전스의 핵심
다이버전스는 가격과 지표(RSI, MACD 등)의 방향이 다른 현상입니다.
- 상승 다이버전스: 가격 저점 하락 + 지표 저점 상승 → 하락 약화 신호
- 하락 다이버전스: 가격 고점 상승 + 지표 고점 하락 → 상승 약화 신호

2. 히든 다이버전스
- 히든 상승: 가격 저점 상승 + 지표 저점 하락 → 추세 지속 신호
- 히든 하락: 가격 고점 하락 + 지표 고점 상승 → 추세 지속 신호

3. 실전 활용 주의점
- 다이버전스만으로 진입하지 말 것
- 반드시 지지/저항, 캔들 패턴과 함께 확인
- 손절가를 반드시 설정하고 진입

⚠️ 주의: 다이버전스는 '가능성'을 보여줄 뿐, 확정이 아닙니다.""",
        "tips": ["4시간봉 이상에서 신뢰도 높음", "거래량 동반 확인 필수", "추세 반전보다 조정 관점으로 접근"]
    },
    "support_resistance_lesson": {
        "title": "📉 지지/저항 심화 해설",
        "topic": "지지저항",
        "unlock_condition": "지지저항 과제 1회 제출",
        "content": """지지와 저항 심화 해설

1. 지지선의 특징
- 과거에 가격이 멈추고 반등한 구간
- 매수 세력이 집중된 가격대
- 깨지면 저항으로 전환될 수 있음

2. 저항선의 특징
- 과거에 가격이 멈추고 하락한 구간
- 매도 세력이 집중된 가격대
- 돌파하면 지지로 전환될 수 있음

3. 강한 지지/저항 찾기
- 여러 번 터치된 구간
- 거래량이 집중된 구간
- 심리적 가격대 (정수 가격)
- 피보나치 레벨과 겹치는 구간

4. 활용 전략
- 지지선 근처에서 반등 시 롱 고려
- 저항선 근처에서 하락 시 숏 고려
- 돌파 후 리테스트에서 진입 고려

⚠️ 주의: 지지/저항은 '구간'이지 정확한 '가격'이 아닙니다.""",
        "tips": ["일봉 이상에서 먼저 확인", "구간으로 생각하기 (정확한 가격 X)", "돌파 여부는 종가 기준으로 판단"]
    },
    "srl_lesson": {
        "title": "📈 SRL 지표 심화 해설",
        "topic": "SRL",
        "unlock_condition": "SRL 과제 1회 제출",
        "content": """SRL 지표 심화 해설

1. SRL이란?
Support and Resistance Levels의 약자로,
자동으로 지지/저항 구간을 표시해주는 지표입니다.

2. 트레이딩뷰 설정
- 지표 검색에서 'Support Resistance' 검색
- 설정에서 기간(Period)과 감도(Sensitivity) 조정
- 너무 많이 표시되면 감도 낮추기

3. 해석 방법
- 빨간 구간: 저항 구간
- 초록 구간: 지지 구간
- 구간 너비: 신뢰도 (넓을수록 강함)

4. 다른 지표와 조합
- RSI 과매수/과매도 + SRL
- 다이버전스 + SRL 구간
- 캔들 패턴 + SRL 구간

⚠️ 주의: SRL은 보조 도구일 뿐, 맹신하지 마세요.""",
        "tips": ["일봉에서 큰 그림 먼저 확인", "여러 타임프레임에서 겹치는 구간 주목", "실시간으로 변할 수 있음을 인지"]
    },
    "tail_candle_lesson": {
        "title": "🕯️ 아래꼬리 캔들 심화 해설",
        "topic": "아래꼬리",
        "unlock_condition": "아래꼬리 과제 1회 제출",
        "content": """아래꼬리 캔들 심화 해설

1. 아래꼬리 캔들이란?
캔들의 아래쪽에 긴 꼬리(그림자)가 있는 형태입니다.
- 한때 가격이 크게 하락했다가 회복됨을 의미
- 매수 세력의 유입 신호일 수 있음

2. 의미 있는 아래꼬리
- 꼬리 길이가 몸통의 2배 이상
- 중요 지지 구간에서 발생
- 거래량 동반 상승

3. 망치형 vs 역망치형
- 망치형: 하락 추세 바닥에서 아래꼬리 → 반전 신호
- 역망치형: 위꼬리가 긴 형태 → 다른 해석 필요

4. 진입 시점
- 아래꼬리 확인 후 다음 봉에서 확인
- 고점 돌파 시 진입 고려
- 아래꼬리 저점 아래에 손절 설정

⚠️ 주의: 단일 캔들만으로 판단하지 말고 맥락을 보세요.""",
        "tips": ["4시간봉 이상에서 신뢰도 높음", "지지 구간에서 나온 것이 중요", "다음 봉의 확인이 필수"]
    }
}

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">🔓 해설 콘텐츠</h1>
    <p class="page-subtitle">과제 제출로 언락된 심화 해설을 확인하세요</p>
</div>
""", unsafe_allow_html=True)

# 닉네임 입력
if 'nickname' not in st.session_state:
    st.session_state.nickname = ''

nickname = st.text_input("닉네임 입력", value=st.session_state.nickname, placeholder="온보딩에서 사용한 닉네임")

if nickname:
    st.session_state.nickname = nickname
    unlocks = load_unlocks()
    
    # 새 유저면 초기화
    if nickname not in unlocks:
        unlocks[nickname] = {key: False for key in LESSONS.keys()}
    
    user_unlocks = unlocks.get(nickname, {})
    
    # 면책 문구 (항상 표시)
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 본 해설은 교육 및 정보 제공 목적입니다. 매매 추천, 가격 예측, 종목 추천이 아니며 투자 권유가 아닙니다. 모든 투자 결정은 본인 책임입니다.
    </div>
    """, unsafe_allow_html=True)
    
    # 해설 카드 표시
    for key, lesson in LESSONS.items():
        is_unlocked = user_unlocks.get(key, False)
        card_class = "unlocked" if is_unlocked else "locked"
        status_class = "status-unlocked" if is_unlocked else "status-locked"
        status_text = "🔓 열림" if is_unlocked else "🔒 잠김"
        
        st.markdown(f"""
        <div class="lesson-card {card_class}">
            <div class="lesson-header">
                <h3 class="lesson-title">{lesson['title']}</h3>
                <span class="status-badge {status_class}">{status_text}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if is_unlocked:
            st.markdown(f"""
            <div class="lesson-content">{lesson['content']}</div>
            <div class="tip-box">
                <p class="tip-title">💡 실전 팁</p>
                {"".join([f'<p class="tip-text">• {tip}</p>' for tip in lesson['tips']])}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="unlock-condition">🔐 언락 조건: {lesson['unlock_condition']}</div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📤 {lesson['topic']} 과제 제출하러 가기", key=f"goto_{key}"):
                st.switch_page("pages/03_homework.py")
        
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("닉네임을 입력하면 언락 상태를 확인할 수 있습니다.")

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
    if st.button("🚀 심화 문제", use_container_width=True):
        st.switch_page("pages/12_advanced_practice.py")
