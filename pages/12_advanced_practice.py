import streamlit as st
import json
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="심화 문제 - BuyLow", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")
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
        --danger: #ef4444;
    }
    
    .stApp { background: var(--bg-dark); background-image: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.12), transparent); }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .page-header { padding: 2rem 0; animation: fadeInUp 0.6s ease-out; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    .page-subtitle { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-secondary); margin-top: 0.25rem; }
    
    .practice-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .practice-card.unlocked { border-left: 4px solid var(--success); }
    .practice-card.locked { border-left: 4px solid var(--text-muted); opacity: 0.7; }
    
    .practice-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
    .practice-title { font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0; }
    .difficulty-badge { font-family: 'Noto Sans KR', sans-serif; font-size: 0.7rem; padding: 0.25rem 0.6rem; border-radius: 8px; }
    .diff-hard { background: rgba(239,68,68,0.2); color: var(--danger); }
    .diff-medium { background: rgba(245,158,11,0.2); color: var(--warning); }
    
    .status-badge { font-family: 'Noto Sans KR', sans-serif; font-size: 0.75rem; padding: 0.3rem 0.75rem; border-radius: 12px; }
    .status-unlocked { background: rgba(34,197,94,0.2); color: var(--success); }
    .status-locked { background: rgba(255,255,255,0.1); color: var(--text-muted); }
    
    .unlock-condition { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--warning); background: rgba(245,158,11,0.1); border-radius: 8px; padding: 0.5rem 0.75rem; margin: 0.5rem 0; }
    
    .question-box { background: var(--bg-dark); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; margin: 1rem 0; }
    .question-text { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-primary); line-height: 1.7; margin-bottom: 1rem; }
    
    .scenario-box { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 1rem; margin: 0.75rem 0; }
    .scenario-title { font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 0.5rem; }
    .scenario-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; }
    
    .answer-reveal { background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); border-radius: 8px; padding: 1rem; margin: 1rem 0; }
    .answer-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.7; }
    
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

# 심화 문제 데이터
ADVANCED_PROBLEMS = {
    "divergence_advanced": {
        "title": "📊 다이버전스 심화 문제",
        "topic": "다이버전스",
        "difficulty": "hard",
        "unlock_condition": "다이버전스 과제 2회 제출",
        "scenario": """BTC 4시간 차트에서 다음 상황이 발생했습니다:
- 가격: 45,000 → 46,500 → 47,200 (고점 상승 중)
- RSI: 75 → 72 → 68 (고점 하락 중)
- 현재 45,800 지지 구간 위에 위치
- 거래량은 점점 감소 중""",
        "question": "이 상황에서 어떤 판단을 할 수 있으며, 만약 진입한다면 손절과 포지션 비중은 어떻게 설정하겠습니까?",
        "answer": """분석 포인트:
1. 가격 고점 상승 + RSI 고점 하락 = 하락 다이버전스 발생
2. 거래량 감소 = 상승 모멘텀 약화 확인
3. 단, 다이버전스는 '가능성'이지 확정이 아님

진입 시 고려사항:
- 숏 진입 고려 가능하나, 45,800 지지 이탈 확인 후 진입이 안전
- 손절: 47,200 고점 위 1% (약 47,700)
- 포지션: 5% 이하 권장 (불확실성 고려)
- 레버리지: 3x 이하 권장

⚠️ 이것은 교육용 분석 예시이며, 실제 매매 추천이 아닙니다."""
    },
    "support_resistance_advanced": {
        "title": "📉 지지/저항 심화 문제",
        "topic": "지지저항",
        "difficulty": "medium",
        "unlock_condition": "지지저항 과제 2회 제출",
        "scenario": """ETH 일봉 차트에서 다음 상황입니다:
- 2,800 구간: 과거 3번 반등한 강한 지지
- 3,200 구간: 과거 4번 저항받은 강한 저항
- 현재 가격: 3,180 (저항 직전)
- RSI: 65 (과매수 아님)
- 거래량 증가 중""",
        "question": "현재 가격대에서 가능한 시나리오 2가지를 제시하고, 각 시나리오별 대응 전략을 설명하세요.",
        "answer": """시나리오 1: 저항 돌파
- 조건: 3,200 일봉 종가 돌파 + 거래량 동반
- 대응: 돌파 후 3,200 리테스트에서 롱 진입 고려
- 손절: 3,100 (이전 저항=새 지지 아래)
- 목표: 다음 저항 구간 탐색

시나리오 2: 저항에서 하락
- 조건: 3,200 부근에서 긴 윗꼬리 캔들 발생
- 대응: 2,800 지지 근처까지 관망 또는 숏 고려
- 손절: 3,250 (저항 위)
- 목표: 2,800 지지 구간

⚠️ 이것은 교육용 분석 예시이며, 실제 매매 추천이 아닙니다."""
    },
    "srl_advanced": {
        "title": "📈 SRL 심화 문제",
        "topic": "SRL",
        "difficulty": "medium",
        "unlock_condition": "SRL 과제 2회 제출",
        "scenario": """SOL 4시간 차트에서 SRL 지표가 다음을 표시합니다:
- 빨간 저항: 105-108 구간
- 초록 지지: 95-98 구간
- 현재 가격: 101
- 일봉 SRL에서도 비슷한 구간 확인
- RSI 다이버전스 없음""",
        "question": "SRL과 다른 지표를 조합하여 진입 계획을 세운다면 어떻게 하겠습니까?",
        "answer": """진입 계획:

롱 시나리오 (지지 근처):
- 95-98 지지 구간 도달 시 관찰
- 아래꼬리 캔들 또는 RSI 과매도(30 이하) 확인 후 롱 고려
- 손절: 94 (지지 구간 아래)
- 목표: 105 저항 전 청산 (R:R 약 1:2)

숏 시나리오 (저항 근처):
- 105-108 저항 도달 시 관찰
- 윗꼬리 캔들 또는 RSI 과매수(70 이상) 확인 후 숏 고려
- 손절: 110 (저항 위)
- 목표: 98 지지 전 청산

핵심: 구간 중간(현재 101)에서는 관망이 유리

⚠️ 이것은 교육용 분석 예시이며, 실제 매매 추천이 아닙니다."""
    },
    "tail_candle_advanced": {
        "title": "🕯️ 아래꼬리 캔들 심화 문제",
        "topic": "아래꼬리",
        "difficulty": "hard",
        "unlock_condition": "아래꼬리 과제 2회 제출",
        "scenario": """AVAX 4시간 차트 상황:
- 하락 추세 진행 중 (고점/저점 낮아지는 중)
- 25달러 지지 구간에서 긴 아래꼬리 캔들 발생
- 꼬리 길이가 몸통의 3배
- 해당 봉 거래량 평소의 2배
- RSI: 28 (과매도)""",
        "question": "이 아래꼬리 캔들을 어떻게 해석하며, 진입한다면 구체적인 계획은?",
        "answer": """해석:
1. 강한 지지 구간(25)에서 긴 아래꼬리 = 매수 세력 유입 신호
2. 거래량 2배 동반 = 신뢰도 상승
3. RSI 과매도 = 반등 가능성 높아짐
4. 단, 하락 추세 중이므로 '반전'보다 '반등' 관점

진입 계획:
- 진입: 다음 봉에서 아래꼬리 캔들 고점(약 26) 돌파 시
- 손절: 아래꼬리 저점 아래 (약 24)
- 1차 목표: 28 (최근 저항)
- 포지션: 5% 이하 (추세 역행이므로 보수적)
- 레버리지: 2x 이하

리스크 관리:
- 손익비: 약 1:2 (2달러 리스크 / 4달러 수익)
- 진입 후 원금 일부 청산 전략 고려

⚠️ 이것은 교육용 분석 예시이며, 실제 매매 추천이 아닙니다."""
    }
}

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">🎯 심화 문제</h1>
    <p class="page-subtitle">과제 2회 제출로 언락되는 고급 시나리오 문제</p>
</div>
""", unsafe_allow_html=True)

# 닉네임 입력
if 'nickname' not in st.session_state:
    st.session_state.nickname = ''

nickname = st.text_input("닉네임 입력", value=st.session_state.nickname, placeholder="온보딩에서 사용한 닉네임")

if nickname:
    st.session_state.nickname = nickname
    unlocks = load_unlocks()
    
    if nickname not in unlocks:
        unlocks[nickname] = {key: False for key in ADVANCED_PROBLEMS.keys()}
    
    user_unlocks = unlocks.get(nickname, {})
    
    # 면책 문구
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 본 심화 문제는 교육 및 학습 목적입니다. 매매 추천, 가격 예측, 종목 추천이 아니며 투자 권유가 아닙니다. 모든 투자 결정은 본인 책임입니다.
    </div>
    """, unsafe_allow_html=True)
    
    for key, problem in ADVANCED_PROBLEMS.items():
        is_unlocked = user_unlocks.get(key, False)
        card_class = "unlocked" if is_unlocked else "locked"
        status_class = "status-unlocked" if is_unlocked else "status-locked"
        status_text = "🔓 열림" if is_unlocked else "🔒 잠김"
        diff_class = "diff-hard" if problem['difficulty'] == 'hard' else "diff-medium"
        diff_text = "상급" if problem['difficulty'] == 'hard' else "중급"
        
        st.markdown(f"""
        <div class="practice-card {card_class}">
            <div class="practice-header">
                <h3 class="practice-title">{problem['title']}</h3>
                <div style="display: flex; gap: 0.5rem;">
                    <span class="difficulty-badge {diff_class}">{diff_text}</span>
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if is_unlocked:
            st.markdown(f"""
            <div class="scenario-box">
                <p class="scenario-title">📋 시나리오</p>
                <p class="scenario-text">{problem['scenario']}</p>
            </div>
            <div class="question-box">
                <p class="question-text">❓ <strong>문제:</strong> {problem['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"💡 해설 보기", key=f"reveal_{key}"):
                st.markdown(f"""
                <div class="answer-reveal">
                    <p class="answer-text">{problem['answer']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="unlock-condition">🔐 언락 조건: {problem['unlock_condition']}</div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📤 {problem['topic']} 과제 제출하러 가기", key=f"goto_{key}"):
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
    if st.button("🔓 해설 모음", use_container_width=True):
        st.switch_page("pages/11_unlocked_lessons.py")
