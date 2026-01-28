import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="진단 퀴즈 - BuyLow", page_icon="📚", layout="wide", initial_sidebar_state="expanded")
render_sidebar()

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #0f0f14;
        --bg-card: #18181f;
        --bg-card-hover: #1e1e28;
        --border: rgba(255,255,255,0.08);
        --text-primary: #ffffff;
        --text-secondary: rgba(255,255,255,0.6);
        --text-muted: rgba(255,255,255,0.4);
        --accent-primary: #6366f1;
        --accent-secondary: #8b5cf6;
        --accent-glow: rgba(99, 102, 241, 0.3);
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    }
    
    .stApp {
        background: var(--bg-dark);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.12), transparent),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.08), transparent);
    }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes scaleIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
    @keyframes confetti { 0%, 100% { transform: translateY(0) rotate(0); } 50% { transform: translateY(-10px) rotate(5deg); } }
    
    .page-header {
        padding: 2rem 0;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .page-title {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(1.75rem, 4vw, 2.5rem);
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .page-subtitle {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 1rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }
    
    .quiz-info {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .quiz-badge {
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        color: var(--accent-primary);
        background: rgba(99,102,241,0.15);
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }
    
    .question-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.25rem 0;
        animation: fadeInUp 0.5s ease-out backwards;
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        border-color: rgba(99,102,241,0.3);
    }
    
    .question-number {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: var(--accent-primary);
        margin-bottom: 0.75rem;
    }
    
    .question-text {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    .result-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        animation: scaleIn 0.6s ease-out;
    }
    
    .score-circle {
        width: 140px;
        height: 140px;
        background: var(--gradient-primary);
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        box-shadow: 0 20px 50px var(--accent-glow);
        animation: confetti 2s ease-in-out infinite;
    }
    
    .score-value {
        font-family: 'Space Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    .score-label {
        font-family: 'Outfit', sans-serif;
        font-size: 0.8rem;
        color: rgba(255,255,255,0.8);
    }
    
    .level-badge {
        display: inline-block;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        margin: 1rem 0;
    }
    
    .level-advanced { background: rgba(34, 197, 94, 0.2); color: var(--success); border: 1px solid var(--success); }
    .level-intermediate { background: rgba(245, 158, 11, 0.2); color: var(--warning); border: 1px solid var(--warning); }
    .level-beginner { background: rgba(239, 68, 68, 0.2); color: var(--danger); border: 1px solid var(--danger); }
    
    .result-message {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin: 1rem 0;
    }
    
    .task-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out backwards;
    }
    
    .task-card:hover {
        border-color: var(--accent-primary);
        transform: translateX(8px);
    }
    
    .task-icon {
        width: 40px;
        height: 40px;
        background: var(--gradient-primary);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .task-content { flex: 1; }
    
    .task-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.25rem 0;
    }
    
    .task-desc {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin: 0;
    }
    
    .priority-tag {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    
    .priority-high { background: rgba(239, 68, 68, 0.2); color: var(--danger); }
    .priority-medium { background: rgba(245, 158, 11, 0.2); color: var(--warning); }
    
    .feedback-correct {
        background: rgba(34, 197, 94, 0.1);
        border-left: 3px solid var(--success);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Noto Sans KR', sans-serif;
        color: var(--success);
    }
    
    .feedback-incorrect {
        background: rgba(239, 68, 68, 0.1);
        border-left: 3px solid var(--danger);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Noto Sans KR', sans-serif;
        color: var(--danger);
    }
    
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-primary);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--gradient-primary);
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px var(--accent-glow);
    }
    
    .stRadio > label { font-family: 'Noto Sans KR', sans-serif; }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid var(--border);
    }
    
    .footer p {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.8rem;
        color: var(--text-muted);
        margin: 0.25rem 0;
    }
    
    @media (max-width: 768px) {
        .question-card { padding: 1.25rem; }
        .result-container { padding: 1.5rem; }
        .score-circle { width: 120px; height: 120px; }
        .score-value { font-size: 2rem; }
        .task-card { flex-direction: column; gap: 0.75rem; }
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 900px; }
    @media (max-width: 768px) { .block-container { padding: 0.5rem 1rem; } }
</style>
""", unsafe_allow_html=True)

LOGS_PATH = Path("data/logs.json")

def save_quiz_log(score, total, recommendations):
    try:
        logs = []
        if LOGS_PATH.exists():
            with open(LOGS_PATH, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        logs.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "type": "quiz_result", "score": score, "total": total, "percentage": round((score/total)*100, 1), "recommendations": recommendations})
        with open(LOGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except: pass

QUIZ = [
    {"q": "RSI 지표가 70 이상일 때 의미하는 것은?", "opts": ["과매도 구간", "과매수 구간으로 조정 가능성", "추세 강도 약함", "거래량 감소"], "ans": 1, "exp": "RSI 70 이상은 과매수 구간으로 조정 가능성을 염두에 두어야 합니다."},
    {"q": "손절가 설정의 가장 중요한 원칙은?", "opts": ["진입 후 설정", "진입 전 반드시 설정하고 준수", "손실 시 하향", "수익 시 제거"], "ans": 1, "exp": "손절가는 진입 전 반드시 설정하고 준수해야 합니다."},
    {"q": "레버리지 사용 시 가장 주의해야 할 점은?", "opts": ["수익 배수 증가", "손실도 배수로 증가 + 청산 위험", "높을수록 유리", "수수료와 무관"], "ans": 1, "exp": "레버리지는 손실도 배수로 확대되며 청산 위험이 증가합니다."},
    {"q": "포지션 사이징 결정 시 가장 중요한 요소는?", "opts": ["총 보유 자금", "허용 손실액과 손절 거리", "과거 수익률", "타인 추천"], "ans": 1, "exp": "포지션 크기는 허용 손실액을 손절 거리로 나누어 계산합니다."},
    {"q": "다이버전스 패턴의 의미는?", "opts": ["가격과 지표 동일 방향", "가격과 지표 반대 방향", "거래량 급증", "이평선 교차"], "ans": 1, "exp": "다이버전스는 가격과 지표의 방향이 다른 현상으로 추세 약화 신호입니다."},
    {"q": "지지선 하단 이탈 시 올바른 대응은?", "opts": ["저렴한 매수 기회", "손절 또는 관망", "레버리지 상향", "무조건 보유"], "ans": 1, "exp": "지지선 이탈은 추가 하락 가능성이므로 손절 규칙을 따릅니다."},
    {"q": "과매매 방지법이 아닌 것은?", "opts": ["일일 거래 제한", "매매일지 작성", "손실 후 즉시 재진입으로 만회", "근거 없는 진입 금지"], "ans": 2, "exp": "손실 후 즉시 재진입은 복구매매로 과매매의 전형입니다."},
    {"q": "트레이딩에서 가장 중요한 요소는?", "opts": ["높은 승률", "빠른 진입", "리스크 관리와 규율 준수", "많은 거래"], "ans": 2, "exp": "리스크 관리와 규율이 장기적 성공의 핵심입니다."}
]

def get_recommendations(score, total):
    pct = (score/total)*100
    if pct >= 87.5:
        return "상급", "level-advanced", "🎉 훌륭해요! 기본 개념을 잘 이해하고 있습니다.", [
            {"icon": "📊", "title": "고급 차트 패턴 학습", "desc": "헤드앤숄더, 삼각수렴 등 고급 패턴", "priority": "medium"},
            {"icon": "📝", "title": "실전 매매일지 작성", "desc": "Risk Check에서 매일 기록 및 분석", "priority": "high"},
            {"icon": "🔬", "title": "백테스팅 연습", "desc": "과거 차트에서 전략 시뮬레이션", "priority": "medium"}
        ]
    elif pct >= 62.5:
        return "중급", "level-intermediate", "👍 좋아요! 기본기는 탄탄합니다.", [
            {"icon": "🛡️", "title": "리스크 관리 복습", "desc": "손절, 포지션 사이징, 레버리지 관리", "priority": "high"},
            {"icon": "📈", "title": "지표 조합 연습", "desc": "RSI + 이동평균 + 지지저항 복합 분석", "priority": "medium"},
            {"icon": "📓", "title": "감정 일지 작성", "desc": "매매 전후 감정 상태 기록", "priority": "high"}
        ]
    else:
        return "초급", "level-beginner", "💪 시작이 반입니다! 기초부터 함께해요.", [
            {"icon": "📊", "title": "RSI 지표 기초 학습", "desc": "CS 챗봇에서 'RSI' 검색하여 개념 습득", "priority": "high"},
            {"icon": "🛡️", "title": "손절과 포지션 사이징", "desc": "리스크 관리의 핵심 개념 필수 숙지", "priority": "high"},
            {"icon": "📉", "title": "지지선과 저항선 이해", "desc": "차트에서 지지/저항 구간 찾기 연습", "priority": "medium"}
        ]

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title"><span style="font-size:1.5rem;">📚</span> 진단 퀴즈</h1>
    <p class="page-subtitle">트레이딩 기초 지식을 점검해보세요</p>
</div>
""", unsafe_allow_html=True)

if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = [None] * len(QUIZ)
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

if not st.session_state.quiz_submitted:
    st.markdown("""
    <div class="quiz-info">
        <span class="quiz-badge">📝 8문항</span>
        <span class="quiz-badge">⏱️ 약 5분</span>
        <span class="quiz-badge">🎯 맞춤 추천</span>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(QUIZ):
        st.markdown(f"""
        <div class="question-card" style="animation-delay: {i*0.1}s;">
            <div class="question-number">Question {i+1:02d} / 08</div>
            <div class="question-text">{q['q']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.quiz_answers[i] = st.radio(f"q{i}", range(len(q['opts'])), format_func=lambda x, q=q: q['opts'][x], key=f"q_{i}", label_visibility="collapsed")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📤 제출하기", type="primary", use_container_width=True):
            st.session_state.quiz_submitted = True
            st.rerun()

else:
    score = sum(1 for i, q in enumerate(QUIZ) if st.session_state.quiz_answers[i] == q['ans'])
    total = len(QUIZ)
    level, level_class, message, tasks = get_recommendations(score, total)
    save_quiz_log(score, total, [t['title'] for t in tasks])
    
    st.markdown(f"""
    <div class="result-container">
        <div class="score-circle">
            <span class="score-value">{score}/{total}</span>
            <span class="score-label">점수</span>
        </div>
        <div class="level-badge {level_class}">{level}</div>
        <p class="result-message">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 문제별 결과 보기"):
        for i, q in enumerate(QUIZ):
            correct = st.session_state.quiz_answers[i] == q['ans']
            if correct:
                st.markdown(f'<div class="feedback-correct">✓ Q{i+1}: 정답!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-incorrect">✗ Q{i+1}: 오답 — 정답: {q["opts"][q["ans"]]}</div>', unsafe_allow_html=True)
            st.caption(f"💡 {q['exp']}")
    
    st.markdown("---")
    st.markdown("### 🎯 오늘의 미션")
    
    for i, t in enumerate(tasks):
        priority_class = "priority-high" if t['priority'] == "high" else "priority-medium"
        st.markdown(f"""
        <div class="task-card" style="animation-delay: {i*0.15}s;">
            <div class="task-icon">{t['icon']}</div>
            <div class="task-content">
                <p class="task-title">{t['title']} <span class="priority-tag {priority_class}">{t['priority'].upper()}</span></p>
                <p class="task-desc">{t['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 CS 챗봇", use_container_width=True):
            st.switch_page("pages/01_cs_chat.py")
    with col2:
        if st.button("📤 과제 제출", use_container_width=True):
            st.switch_page("pages/03_homework.py")
    with col3:
        if st.button("🛡️ 리스크 체크", use_container_width=True):
            st.switch_page("pages/04_risk_check.py")
    
    if st.button("🔄 다시 풀기", use_container_width=True):
        st.session_state.quiz_answers = [None] * len(QUIZ)
        st.session_state.quiz_submitted = False
        st.rerun()

st.markdown("""
<div class="footer">
    <p>📚 BuyLow 진단 퀴즈</p>
    <p>자가 진단용 | 능력 평가 아님</p>
</div>
""", unsafe_allow_html=True)
