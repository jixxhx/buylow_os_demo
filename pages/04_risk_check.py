import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="리스크 체크 - BuyLow", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
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
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
    
    .page-header { padding: 2rem 0; animation: fadeInUp 0.6s ease-out; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    .page-subtitle { font-family: 'Noto Sans KR', sans-serif; font-size: 1rem; color: var(--text-secondary); margin-top: 0.25rem; }
    
    .form-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .form-label { font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.75rem; }
    
    .score-display { background: var(--bg-card); border: 2px solid; border-radius: 20px; padding: 2rem; text-align: center; margin: 1.5rem 0; animation: fadeInUp 0.5s ease-out; }
    .score-low { border-color: var(--success); }
    .score-medium { border-color: var(--warning); }
    .score-high { border-color: var(--danger); animation: pulse 1.5s ease-in-out infinite; }
    .score-number { font-family: 'Space Mono', monospace; font-size: 3.5rem; font-weight: 700; }
    .score-label { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 600; margin-top: 0.25rem; }
    
    .alert-item { display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; margin: 0.5rem 0; border-radius: 12px; animation: fadeInUp 0.4s ease-out backwards; }
    .alert-danger { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); }
    .alert-warning { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); }
    .alert-success { background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); }
    .alert-icon { font-size: 1.25rem; }
    .alert-content { flex: 1; }
    .alert-title { font-family: 'Outfit', sans-serif; font-weight: 600; margin: 0 0 0.25rem 0; }
    .alert-desc { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); margin: 0; }
    
    .routine-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; display: flex; align-items: center; gap: 1rem; transition: all 0.3s ease; }
    .routine-card:hover { border-color: var(--accent-primary); transform: translateX(8px); }
    .routine-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
    .routine-content { flex: 1; }
    .routine-title { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin: 0; }
    .routine-desc { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-secondary); margin: 0; }
    
    .mini-course { background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.05)); border: 2px solid rgba(239,68,68,0.3); border-radius: 16px; padding: 1.5rem; margin: 1.5rem 0; }
    .mini-course-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--danger); margin-bottom: 1rem; }
    .course-card { background: var(--bg-card); border-radius: 12px; padding: 1.25rem; margin: 0.75rem 0; }
    .course-step { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--accent-primary); margin-bottom: 0.5rem; }
    .course-content { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.7; }
    
    .warning-history { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin: 1rem 0; }
    .warning-item { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--border); }
    .warning-item:last-child { border-bottom: none; }
    .warning-name { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); }
    .warning-count { font-family: 'Space Mono', monospace; font-size: 0.9rem; padding: 0.2rem 0.6rem; border-radius: 8px; }
    .count-danger { background: rgba(239,68,68,0.2); color: var(--danger); }
    .count-warning { background: rgba(245,158,11,0.2); color: var(--warning); }
    .count-safe { background: rgba(34,197,94,0.2); color: var(--success); }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin: 1rem 0; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 900px; }
</style>
""", unsafe_allow_html=True)

# 데이터 경로
RISK_HISTORY_PATH = Path("data/risk_history.json")
LOGS_PATH = Path("data/logs.json")

def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

EMOTIONS = ["😐 보통", "😊 자신감", "😰 불안", "😤 분노/좌절", "🤩 과한 흥분", "😔 우울/무기력"]

WARNING_TYPES = {
    "손절가 미설정": {"key": "no_stop_loss", "points": 30},
    "과도한 레버리지": {"key": "high_leverage", "points": 25},
    "과도한 포지션 비중": {"key": "high_position", "points": 20},
    "진입 근거 부족": {"key": "no_reason", "points": 15},
    "감정적 상태 위험": {"key": "emotional", "points": 20}
}

# 미니 코스 콘텐츠
MINI_COURSE = [
    {
        "title": "손절 없는 매매가 왜 위험한가",
        "content": """손절가 없이 진입하면:
• 작은 손실이 큰 손실로 확대됩니다
• "조금만 더 기다리면" 심리가 작동합니다
• 계좌 전체를 날릴 수 있습니다

✅ 해결책: 진입 전 반드시 손절가를 정하고, 그 가격에 도달하면 무조건 청산합니다."""
    },
    {
        "title": "포지션 비중이 커지면 왜 망가지나",
        "content": """큰 포지션의 문제:
• 한 번의 손실로 회복이 어려워집니다
• 작은 변동에도 감정이 흔들립니다
• 냉정한 판단이 불가능해집니다

✅ 해결책: 한 포지션에 총 자금의 5-10% 이하만 투입합니다.
예: 1000만원 계좌 → 한 포지션 50-100만원"""
    },
    {
        "title": "복구매매 신호 자가진단",
        "content": """복구매매 위험 신호:
□ 손실 직후 바로 다시 진입하고 싶다
□ "이번엔 꼭 되찾겠다"는 생각이 든다
□ 평소보다 큰 금액으로 진입하려 한다
□ 충분한 분석 없이 급하게 진입한다

✅ 해결책: 손실 후 최소 1시간 휴식, 감정이 안정된 후에만 매매"""
    }
]

def check_violations(data):
    violations = []
    
    if not data.get('stop_loss') or data['stop_loss'] <= 0:
        violations.append({"type": "손절가 미설정", "icon": "🚨", "desc": "손절가 없이 진입하면 손실이 무한정 커질 수 있습니다", "level": "danger", "points": 30})
    
    if data.get('leverage', 1) > 10:
        violations.append({"type": "과도한 레버리지", "icon": "⚠️", "desc": f"{data['leverage']}x 레버리지는 청산 위험이 매우 높습니다", "level": "danger", "points": 25})
    elif data.get('leverage', 1) > 5:
        violations.append({"type": "과도한 레버리지", "icon": "⚠️", "desc": f"{data['leverage']}x 레버리지는 신중한 관리가 필요합니다", "level": "warning", "points": 15})
    
    if data.get('position_size', 0) > 30:
        violations.append({"type": "과도한 포지션 비중", "icon": "🚨", "desc": f"{data['position_size']}% 비중은 한 번의 손실로 큰 타격입니다", "level": "danger", "points": 20})
    elif data.get('position_size', 0) > 20:
        violations.append({"type": "과도한 포지션 비중", "icon": "⚠️", "desc": f"{data['position_size']}% 비중은 분산이 필요합니다", "level": "warning", "points": 10})
    
    if len(data.get('reason', '')) < 30:
        violations.append({"type": "진입 근거 부족", "icon": "⚠️", "desc": "충분한 분석 없이 진입하는 것은 위험합니다", "level": "warning", "points": 15})
    
    emotion = data.get('emotion', '')
    if emotion in ["😤 분노/좌절", "🤩 과한 흥분"]:
        violations.append({"type": "감정적 상태 위험", "icon": "🚨", "desc": "현재 감정 상태에서는 매매를 쉬는 것이 좋습니다", "level": "danger", "points": 20})
    elif emotion in ["😰 불안", "😔 우울/무기력"]:
        violations.append({"type": "감정적 상태 위험", "icon": "⚠️", "desc": "감정이 안정된 후 매매하는 것을 권장합니다", "level": "warning", "points": 10})
    
    return violations

def get_routines(score):
    if score >= 50:
        return [
            {"icon": "⏸️", "title": "매매 일시 중단", "desc": "새로운 포지션 진입을 자제하세요"},
            {"icon": "📝", "title": "매매일지 복기", "desc": "최근 매매를 돌아보세요"},
            {"icon": "🧘", "title": "휴식", "desc": "10분 이상 산책하거나 쉬세요"}
        ]
    elif score >= 30:
        return [
            {"icon": "🛡️", "title": "포지션 축소", "desc": "비중을 10% 이하로 줄이세요"},
            {"icon": "📊", "title": "손절가 재확인", "desc": "모든 포지션의 손절가를 체크하세요"},
            {"icon": "🎯", "title": "진입 근거 보강", "desc": "3가지 이상의 근거를 확보하세요"}
        ]
    else:
        return [
            {"icon": "✅", "title": "계획대로 진행", "desc": "리스크 관리가 양호합니다"},
            {"icon": "📓", "title": "매매일지 기록", "desc": "오늘 진입을 기록하세요"},
            {"icon": "🔔", "title": "알림 설정", "desc": "손절가/익절가에 알림을 설정하세요"}
        ]

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">🛡️ 리스크 매니저</h1>
    <p class="page-subtitle">매매 전 위험 요소를 점검하세요</p>
</div>
""", unsafe_allow_html=True)

# 닉네임 입력
if 'nickname' not in st.session_state:
    st.session_state.nickname = ''
if 'risk_checked' not in st.session_state:
    st.session_state.risk_checked = False
if 'show_mini_course' not in st.session_state:
    st.session_state.show_mini_course = False

nickname = st.text_input("닉네임", value=st.session_state.nickname, placeholder="온보딩에서 사용한 닉네임")
st.session_state.nickname = nickname

# 경고 누적 기록 확인
risk_history = load_json(RISK_HISTORY_PATH)
if nickname and nickname in risk_history:
    user_history = risk_history[nickname]
    warnings = user_history.get('warnings', [])
    
    # 3회 이상 누적된 경고 체크
    high_count_warnings = [w for w in warnings if w.get('count', 0) >= 3]
    
    if high_count_warnings and not user_history.get('mini_course_completed', False):
        st.session_state.show_mini_course = True

# 미니 코스 표시
if st.session_state.show_mini_course and nickname:
    st.markdown("""
    <div class="mini-course">
        <p class="mini-course-title">🚨 미니 리스크 코스 (필수)</p>
        <p style="font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary);">
            동일한 리스크 경고가 3회 이상 누적되었습니다. 아래 내용을 확인해주세요.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, course in enumerate(MINI_COURSE):
        st.markdown(f"""
        <div class="course-card">
            <p class="course-step">STEP {i+1}/3</p>
            <p style="font-family: 'Outfit', sans-serif; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">{course['title']}</p>
            <p class="course-content">{course['content']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("✅ 코스 완료 - 리스크 체크로 이동", type="primary", use_container_width=True):
        risk_history[nickname]['mini_course_completed'] = True
        save_json(RISK_HISTORY_PATH, risk_history)
        st.session_state.show_mini_course = False
        st.rerun()

elif not st.session_state.risk_checked:
    # 경고 누적 기록 표시
    if nickname and nickname in risk_history:
        user_history = risk_history[nickname]
        warnings = user_history.get('warnings', [])
        if warnings:
            st.markdown("### 📊 내 경고 누적 기록")
            st.markdown('<div class="warning-history">', unsafe_allow_html=True)
            for w in warnings:
                count = w.get('count', 0)
                count_class = "count-danger" if count >= 3 else "count-warning" if count >= 1 else "count-safe"
                st.markdown(f"""
                <div class="warning-item">
                    <span class="warning-name">{w.get('type', '')}</span>
                    <span class="warning-count {count_class}">{count}회</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 리스크 체크 폼
    st.markdown('<div class="form-card"><div class="form-label">📈 기본 정보</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.text_input("종목/코인", placeholder="예: BTC, ETH")
    with col2:
        direction = st.selectbox("방향", ["Long (매수)", "Short (매도)"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        entry_price = st.number_input("진입가", min_value=0.0, step=0.01, format="%.4f")
    with col2:
        stop_loss = st.number_input("손절가", min_value=0.0, step=0.01, format="%.4f")
    with col3:
        take_profit = st.number_input("익절 목표", min_value=0.0, step=0.01, format="%.4f")
    
    st.markdown('<div class="form-card"><div class="form-label">⚙️ 리스크 설정</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        leverage = st.slider("레버리지", 1, 100, 1)
    with col2:
        position_size = st.slider("포지션 비중 (%)", 1, 100, 10)
    
    st.markdown('<div class="form-card"><div class="form-label">📝 진입 근거</div></div>', unsafe_allow_html=True)
    reason = st.text_area("", placeholder="진입 이유를 작성하세요...", height=100, label_visibility="collapsed")
    
    emotion = st.selectbox("현재 감정 상태", EMOTIONS)
    
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 본 시스템은 규칙 위반 점검용입니다. 매매 추천이나 가격 예측이 아닙니다.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛡️ 리스크 체크", type="primary", use_container_width=True):
        data = {"symbol": symbol, "direction": direction, "entry_price": entry_price, "stop_loss": stop_loss, "take_profit": take_profit, "leverage": leverage, "position_size": position_size, "reason": reason, "emotion": emotion}
        
        violations = check_violations(data)
        score = min(sum(v['points'] for v in violations), 100)
        
        # 경고 누적 저장
        if nickname:
            if nickname not in risk_history:
                risk_history[nickname] = {"warnings": [], "mini_course_completed": False, "total_checks": 0, "high_risk_count": 0}
            
            # 기존 경고 업데이트
            for v in violations:
                found = False
                for w in risk_history[nickname].get('warnings', []):
                    if w['type'] == v['type']:
                        w['count'] = w.get('count', 0) + 1
                        w['last_occurred'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        found = True
                        break
                if not found:
                    risk_history[nickname]['warnings'].append({
                        "type": v['type'],
                        "count": 1,
                        "last_occurred": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            risk_history[nickname]['total_checks'] = risk_history[nickname].get('total_checks', 0) + 1
            if score >= 50:
                risk_history[nickname]['high_risk_count'] = risk_history[nickname].get('high_risk_count', 0) + 1
            
            # 3회 누적 시 미니 코스 리셋
            for w in risk_history[nickname].get('warnings', []):
                if w.get('count', 0) >= 3:
                    risk_history[nickname]['mini_course_completed'] = False
            
            save_json(RISK_HISTORY_PATH, risk_history)
        
        # 로그 저장
        logs = load_json(LOGS_PATH) if LOGS_PATH.exists() else []
        logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "risk_check",
            "symbol": symbol,
            "direction": direction,
            "leverage": leverage,
            "position_size": position_size,
            "risk_score": score,
            "violation_count": len(violations)
        })
        save_json(LOGS_PATH, logs)
        
        st.session_state.risk_checked = True
        st.session_state.risk_score = score
        st.session_state.risk_violations = violations
        st.session_state.risk_data = data
        st.rerun()

else:
    score = st.session_state.risk_score
    violations = st.session_state.risk_violations
    data = st.session_state.risk_data
    
    if score < 30:
        score_class, score_color, score_label = "score-low", "#22c55e", "✓ 안전"
    elif score < 50:
        score_class, score_color, score_label = "score-medium", "#f59e0b", "⚠️ 주의"
    else:
        score_class, score_color, score_label = "score-high", "#ef4444", "🚨 위험"
    
    st.markdown(f"""
    <div class="score-display {score_class}">
        <p class="score-number" style="color: {score_color};">{score}</p>
        <p class="score-label" style="color: {score_color};">{score_label}</p>
        <p style="font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-muted); margin-top: 0.5rem;">
            {data['symbol']} | {data['direction']} | {data['leverage']}x | {data['position_size']}%
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if violations:
        st.markdown("### ⚠️ 위반 사항")
        for i, v in enumerate(violations):
            alert_class = f"alert-{v['level']}"
            title_color = "#ef4444" if v['level'] == 'danger' else "#f59e0b"
            st.markdown(f"""
            <div class="alert-item {alert_class}" style="animation-delay: {i*0.1}s;">
                <span class="alert-icon">{v['icon']}</span>
                <div class="alert-content">
                    <p class="alert-title" style="color: {title_color};">{v['type']}</p>
                    <p class="alert-desc">{v['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-item alert-success">
            <span class="alert-icon">✅</span>
            <div class="alert-content">
                <p class="alert-title" style="color: #22c55e;">규칙 준수</p>
                <p class="alert-desc">위반 사항이 없습니다!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 오늘의 리스크 루틴")
    routines = get_routines(score)
    for r in routines:
        st.markdown(f"""
        <div class="routine-card">
            <div class="routine-icon">{r['icon']}</div>
            <div class="routine-content">
                <p class="routine-title">{r['title']}</p>
                <p class="routine-desc">{r['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 새로 입력", use_container_width=True):
            st.session_state.risk_checked = False
            st.rerun()
    with col2:
        if st.button("📤 과제 제출", use_container_width=True):
            st.switch_page("pages/03_homework.py")
    with col3:
        if st.button("🏠 홈", use_container_width=True):
            st.switch_page("Home.py")
