import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="과제 제출 - BuyLow", page_icon="📤", layout="wide", initial_sidebar_state="expanded")
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
    
    .topic-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
    .topic-card { background: var(--bg-card); border: 2px solid var(--border); border-radius: 16px; padding: 1.25rem; cursor: pointer; transition: all 0.3s ease; animation: fadeInUp 0.5s ease-out backwards; }
    .topic-card:hover { border-color: var(--accent-primary); transform: translateY(-4px); }
    .topic-card.selected { border-color: var(--accent-primary); background: rgba(99,102,241,0.1); }
    .topic-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .topic-name { font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 700; color: var(--text-primary); }
    .topic-desc { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }
    
    .unlock-preview { background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.05)); border: 1px solid rgba(34,197,94,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; }
    .unlock-title { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 600; color: var(--success); margin-bottom: 0.5rem; }
    .unlock-item { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); padding: 0.25rem 0; }
    
    .form-section { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .form-label { font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.75rem; }
    
    .hint-box { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 1rem; margin: 0.75rem 0; }
    .hint-title { font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; color: var(--accent-primary); margin-bottom: 0.5rem; }
    .hint-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); }
    
    .checklist-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; }
    .check-icon { font-size: 1rem; }
    .check-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; }
    .check-pass { color: var(--success); }
    .check-fail { color: var(--danger); }
    .check-warn { color: var(--warning); }
    
    .char-counter { font-family: 'Space Mono', monospace; font-size: 0.8rem; color: var(--text-muted); text-align: right; margin-top: 0.5rem; }
    
    .result-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .result-score { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    .stTextArea > div > div > textarea { font-family: 'Noto Sans KR', sans-serif; background: var(--bg-dark); border: 1px solid var(--border); border-radius: 12px; color: var(--text-primary); min-height: 200px; }
    
    .disclaimer { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 0.75rem 1rem; margin: 1rem 0; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 900px; }
</style>
""", unsafe_allow_html=True)

# 데이터 경로
SUBMISSIONS_PATH = Path("data/homework_submissions.json")
PROFILES_PATH = Path("data/member_profiles.json")
UNLOCKS_PATH = Path("data/unlocks.json")
LOGS_PATH = Path("data/logs.json")

def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if 'submissions' in str(path) or 'logs' in str(path) else {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 과제 주제
TOPICS = {
    "다이버전스": {
        "icon": "📊",
        "desc": "RSI/MACD 다이버전스 분석",
        "hints": ["가격과 지표 방향 비교", "일반 vs 히든 구분", "추세 약화 신호 해석"],
        "unlock_1": "다이버전스 해설 페이지",
        "unlock_2": "다이버전스 심화 문제"
    },
    "지지저항": {
        "icon": "📉",
        "desc": "지지선과 저항선 분석",
        "hints": ["과거 반등/저항 구간", "거래량 집중 구간", "심리적 가격대"],
        "unlock_1": "지지저항 해설 페이지",
        "unlock_2": "지지저항 심화 문제"
    },
    "SRL": {
        "icon": "📈",
        "desc": "SRL 지표 설정과 해석",
        "hints": ["트레이딩뷰 설정", "구간 해석", "다른 지표와 조합"],
        "unlock_1": "SRL 해설 페이지",
        "unlock_2": "SRL 심화 문제"
    },
    "아래꼬리": {
        "icon": "🕯️",
        "desc": "아래꼬리 캔들 패턴 분석",
        "hints": ["꼬리와 몸통 비율", "거래량 확인", "위치와 맥락"],
        "unlock_1": "아래꼬리 해설 페이지",
        "unlock_2": "아래꼬리 심화 문제"
    }
}

FORBIDDEN = ["추천", "매수하세요", "매도하세요", "사세요", "파세요", "무조건", "100%", "확실", "수익 보장"]
REQUIRED = {
    "risk": ["손절", "리스크", "위험", "관리", "스탑"],
    "position": ["포지션", "비중", "사이징", "%"],
    "reason": ["근거", "이유", "분석", "판단", "확인"]
}

def evaluate(content, topic):
    results = []
    
    # 금지 표현 체크
    forbidden_found = [kw for kw in FORBIDDEN if kw in content]
    if forbidden_found:
        results.append({"status": "fail", "text": f"금지 표현 발견: {', '.join(forbidden_found[:2])}"})
    else:
        results.append({"status": "pass", "text": "투자 권유 표현 없음"})
    
    # 주제별 키워드 체크
    topic_kw = {"다이버전스": ["다이버전스", "rsi", "macd", "괴리"], "지지저항": ["지지", "저항", "구간", "레벨"], "SRL": ["srl", "지표", "구간"], "아래꼬리": ["꼬리", "캔들", "망치", "윅"]}
    if any(kw in content.lower() for kw in topic_kw.get(topic, [])):
        results.append({"status": "pass", "text": f"{topic} 관련 내용 포함"})
    else:
        results.append({"status": "warn", "text": f"{topic} 관련 키워드 부족"})
    
    # 리스크 관리 체크
    if any(kw in content for kw in REQUIRED['risk']):
        results.append({"status": "pass", "text": "리스크 관리 언급"})
    else:
        results.append({"status": "warn", "text": "리스크 관리 언급 부족"})
    
    # 근거 체크
    if any(kw in content for kw in REQUIRED['reason']) and len(content) >= 100:
        results.append({"status": "pass", "text": "충분한 근거 제시"})
    else:
        results.append({"status": "warn", "text": "근거 보강 필요"})
    
    # 분량 체크
    if len(content) >= 150:
        results.append({"status": "pass", "text": f"충분한 분량 ({len(content)}자)"})
    elif len(content) >= 80:
        results.append({"status": "warn", "text": f"분량 다소 부족 ({len(content)}자)"})
    else:
        results.append({"status": "fail", "text": f"분량 부족 ({len(content)}자)"})
    
    return results

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📤 과제 제출</h1>
    <p class="page-subtitle">주제별 과제를 제출하고 추가 콘텐츠를 언락하세요</p>
</div>
""", unsafe_allow_html=True)

# 닉네임 입력
if 'nickname' not in st.session_state:
    st.session_state.nickname = ''
if 'hw_submitted' not in st.session_state:
    st.session_state.hw_submitted = False

nickname = st.text_input("닉네임", value=st.session_state.nickname, placeholder="온보딩에서 사용한 닉네임")
st.session_state.nickname = nickname

if not st.session_state.hw_submitted:
    # 주제 선택
    st.markdown("### 📋 과제 주제 선택")
    
    selected_topic = st.radio("", list(TOPICS.keys()), format_func=lambda x: f"{TOPICS[x]['icon']} {x}", horizontal=True, label_visibility="collapsed")
    
    topic_data = TOPICS[selected_topic]
    
    st.markdown(f"""
    <div class="unlock-preview">
        <p class="unlock-title">🔓 제출 시 언락되는 콘텐츠</p>
        <p class="unlock-item">• 1회 제출: {topic_data['unlock_1']}</p>
        <p class="unlock-item">• 2회 제출: {topic_data['unlock_2']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 힌트
    st.markdown(f"""
    <div class="hint-box">
        <p class="hint-title">💡 작성 힌트</p>
        {"".join([f'<p class="hint-text">• {h}</p>' for h in topic_data['hints']])}
    </div>
    """, unsafe_allow_html=True)
    
    # 과제 작성
    st.markdown('<div class="form-section"><div class="form-label">📝 분석 내용</div></div>', unsafe_allow_html=True)
    
    content = st.text_area("", placeholder=f"{selected_topic} 분석 내용을 작성하세요...\n\n• 차트에서 발견한 패턴/신호\n• 판단 근거\n• 손절/리스크 관리 계획\n\n최소 80자 이상 권장", label_visibility="collapsed", height=250)
    
    st.markdown(f'<p class="char-counter">{len(content)} / 150+ 권장</p>', unsafe_allow_html=True)
    
    # 면책
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 과제는 학습 목적입니다. 매매 추천, 가격 예측, 종목 추천을 포함하지 마세요.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📤 제출하기", type="primary", use_container_width=True):
            if not nickname:
                st.error("닉네임을 입력해주세요")
            elif len(content.strip()) < 50:
                st.error("최소 50자 이상 작성해주세요")
            else:
                results = evaluate(content, selected_topic)
                
                # 제출 저장
                submissions = load_json(SUBMISSIONS_PATH)
                new_id = len(submissions) + 1
                submissions.append({
                    "id": new_id,
                    "nickname": nickname,
                    "topic": selected_topic,
                    "content": content,
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "reviewed": False,
                    "review_result": None
                })
                save_json(SUBMISSIONS_PATH, submissions)
                
                # 프로필 업데이트
                profiles = load_json(PROFILES_PATH)
                if nickname not in profiles:
                    profiles[nickname] = {"nickname": nickname, "homework_count": 0, "homework_streak": 0}
                profiles[nickname]['homework_count'] = profiles[nickname].get('homework_count', 0) + 1
                profiles[nickname]['last_homework_date'] = datetime.now().strftime("%Y-%m-%d")
                save_json(PROFILES_PATH, profiles)
                
                # 언락 체크
                unlocks = load_json(UNLOCKS_PATH)
                if nickname not in unlocks:
                    unlocks[nickname] = {}
                
                topic_submissions = [s for s in submissions if s.get('nickname') == nickname and s.get('topic') == selected_topic]
                topic_map = {
                    '다이버전스': ('divergence_lesson', 'divergence_advanced'),
                    '지지저항': ('support_resistance_lesson', 'support_resistance_advanced'),
                    'SRL': ('srl_lesson', 'srl_advanced'),
                    '아래꼬리': ('tail_candle_lesson', 'tail_candle_advanced')
                }
                if selected_topic in topic_map:
                    lesson_key, advanced_key = topic_map[selected_topic]
                    if len(topic_submissions) >= 1:
                        unlocks[nickname][lesson_key] = True
                    if len(topic_submissions) >= 2:
                        unlocks[nickname][advanced_key] = True
                    save_json(UNLOCKS_PATH, unlocks)
                
                # 로그 저장
                logs = load_json(LOGS_PATH)
                logs.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "homework_submission",
                    "topic": selected_topic,
                    "content_length": len(content)
                })
                save_json(LOGS_PATH, logs)
                
                st.session_state.hw_submitted = True
                st.session_state.hw_results = results
                st.session_state.hw_topic = selected_topic
                st.session_state.topic_count = len(topic_submissions)
                st.rerun()

else:
    results = st.session_state.hw_results
    topic = st.session_state.hw_topic
    topic_count = st.session_state.topic_count
    
    pass_count = sum(1 for r in results if r['status'] == 'pass')
    warn_count = sum(1 for r in results if r['status'] == 'warn')
    fail_count = sum(1 for r in results if r['status'] == 'fail')
    
    score_color = "#22c55e" if fail_count == 0 and warn_count <= 1 else "#f59e0b" if fail_count == 0 else "#ef4444"
    
    st.success(f"✅ {topic} 과제가 제출되었습니다!")
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <span style="font-family: 'Noto Sans KR', sans-serif; color: var(--text-secondary);">자동 체크 결과</span>
            <span class="result-score" style="color: {score_color};">{pass_count}/{len(results)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for r in results:
        icon = "✅" if r['status'] == 'pass' else "⚠️" if r['status'] == 'warn' else "❌"
        color_class = "check-pass" if r['status'] == 'pass' else "check-warn" if r['status'] == 'warn' else "check-fail"
        st.markdown(f"""
        <div class="checklist-item">
            <span class="check-icon">{icon}</span>
            <span class="check-text {color_class}">{r['text']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 언락 알림
    if topic_count == 1:
        st.success(f"🔓 '{TOPICS[topic]['unlock_1']}' 언락!")
    elif topic_count == 2:
        st.success(f"🔓 '{TOPICS[topic]['unlock_2']}' 언락!")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 새 과제", use_container_width=True):
            st.session_state.hw_submitted = False
            st.rerun()
    with col2:
        if st.button("🔓 해설 보기", use_container_width=True):
            st.switch_page("pages/11_unlocked_lessons.py")
    with col3:
        if st.button("🎯 심화 문제", use_container_width=True):
            st.switch_page("pages/12_advanced_practice.py")

# 네비게이션
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 홈", use_container_width=True, key="nav1"):
        st.switch_page("Home.py")
with col2:
    if st.button("📚 교육 콘텐츠", use_container_width=True, key="nav2"):
        st.switch_page("pages/09_content_library.py")
with col3:
    if st.button("🛡️ 리스크 체크", use_container_width=True, key="nav3"):
        st.switch_page("pages/04_risk_check.py")
