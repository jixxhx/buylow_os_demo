import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
from ui.sidebar import render_sidebar

st.set_page_config(page_title="운영자 대시보드 - BuyLow", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
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
        --danger: #ef4444;
    }
    
    .stApp { background: var(--bg-dark); background-image: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.12), transparent); }
    
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .page-header { padding: 1.5rem 0; animation: fadeInUp 0.6s ease-out; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    
    .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
    .summary-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; text-align: center; animation: fadeInUp 0.5s ease-out backwards; }
    .summary-value { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; }
    .summary-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }
    
    .section-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .section-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
    
    .topic-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--bg-dark); border-radius: 8px; margin: 0.5rem 0; }
    .topic-name { font-family: 'Noto Sans KR', sans-serif; font-size: 0.95rem; color: var(--text-primary); }
    .topic-count { font-family: 'Space Mono', monospace; font-size: 0.9rem; color: var(--accent-primary); background: rgba(99,102,241,0.15); padding: 0.25rem 0.75rem; border-radius: 12px; }
    
    .streak-bar { display: flex; gap: 0.5rem; margin: 0.5rem 0; }
    .streak-item { flex: 1; text-align: center; padding: 0.75rem 0.5rem; background: var(--bg-dark); border-radius: 8px; }
    .streak-num { font-family: 'Space Mono', monospace; font-size: 1.25rem; font-weight: 700; color: var(--accent-primary); }
    .streak-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.7rem; color: var(--text-muted); }
    
    .action-suggest { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
    .action-text { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
    
    .template-box { background: var(--bg-dark); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); white-space: pre-wrap; margin: 0.5rem 0; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 10px; font-size: 0.85rem; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 1200px; }
</style>
""", unsafe_allow_html=True)

# 데이터 로드 함수들
def load_json(path):
    if Path(path).exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if path.endswith('.json') and 'tickets' in path else {}

def count_keywords(texts, keywords):
    counts = Counter()
    for text in texts:
        text_lower = text.lower()
        for kw in keywords:
            if kw in text_lower:
                counts[kw] += 1
    return counts

KEYWORDS = ["다이버전스", "지지", "저항", "srl", "아래꼬리", "손절", "레버리지", "익절", "비중", "포지션", "rsi", "캔들"]

# 데이터 로드
logs = load_json("data/logs.json") if Path("data/logs.json").exists() else []
tickets = load_json("data/tickets.json") if Path("data/tickets.json").exists() else []
submissions = load_json("data/homework_submissions.json") if Path("data/homework_submissions.json").exists() else []
reviews = load_json("data/homework_reviews.json") if Path("data/homework_reviews.json").exists() else []
risk_history = load_json("data/risk_history.json") if Path("data/risk_history.json").exists() else {}
profiles = load_json("data/member_profiles.json") if Path("data/member_profiles.json").exists() else {}

# 오늘/이번주 계산
today = datetime.now().strftime("%Y-%m-%d")
week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

today_tickets = [t for t in tickets if t.get('timestamp', '').startswith(today)]
open_tickets = [t for t in tickets if t.get('status') == 'open']
today_submissions = [s for s in submissions if s.get('submitted_at', '').startswith(today)]
week_submissions = [s for s in submissions if s.get('submitted_at', '') >= week_ago]

# 고위험 리스크 카운트
high_risk_today = 0
for user_data in risk_history.values():
    if isinstance(user_data, dict):
        high_risk_today += user_data.get('high_risk_count', 0)

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📊 운영자 대시보드</h1>
</div>
""", unsafe_allow_html=True)

# 한 줄 요약
cs_logs = [l for l in logs if l.get('type') == 'cs_query']
week_cs = [l for l in cs_logs if l.get('timestamp', '') >= week_ago]
top_topic = "없음"
if week_cs:
    texts = [l.get('query', '') for l in week_cs]
    keyword_counts = count_keywords(texts, KEYWORDS)
    if keyword_counts:
        top_topic = keyword_counts.most_common(1)[0][0]

st.markdown(f"""
<div class="summary-grid">
    <div class="summary-card"><p class="summary-value" style="color: #ef4444;">{len(today_tickets)}</p><p class="summary-label">오늘 새 티켓</p></div>
    <div class="summary-card"><p class="summary-value" style="color: #f59e0b;">{len(open_tickets)}</p><p class="summary-label">미해결 티켓</p></div>
    <div class="summary-card"><p class="summary-value" style="color: #22c55e;">{len(today_submissions)}</p><p class="summary-label">오늘 과제</p></div>
    <div class="summary-card"><p class="summary-value" style="color: #ef4444;">{high_risk_today}</p><p class="summary-label">고위험 누적</p></div>
    <div class="summary-card"><p class="summary-value" style="color: #6366f1;">{top_topic}</p><p class="summary-label">이번주 핫토픽</p></div>
</div>
""", unsafe_allow_html=True)

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["🔥 막힌 포인트", "📝 과제 지표", "📢 공지 템플릿", "🎫 티켓 관리"])

with tab1:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">🔥 이번 주 가장 많이 막힌 주제 Top 5</div>
    </div>
    """, unsafe_allow_html=True)
    
    all_texts = [l.get('query', '') for l in week_cs]
    all_texts += [s.get('content', '') for s in week_submissions]
    all_texts += [t.get('query', '') for t in tickets if t.get('timestamp', '') >= week_ago]
    
    keyword_counts = count_keywords(all_texts, KEYWORDS)
    top_5 = keyword_counts.most_common(5)
    
    if top_5:
        for kw, count in top_5:
            col1, col2, col3 = st.columns([3, 1, 2])
            with col1:
                st.markdown(f"**{kw}**")
            with col2:
                st.markdown(f"**{count}회**")
            with col3:
                if st.button(f"📝 공지 초안", key=f"draft_{kw}"):
                    st.session_state[f'show_draft_{kw}'] = True
            
            if st.session_state.get(f'show_draft_{kw}'):
                template = f"""📢 [{kw}] 관련 안내

최근 '{kw}' 관련 질문이 많아 안내드립니다.

✅ 확인해주세요:
- 교육 콘텐츠에서 '{kw}' 섹션 복습
- 과제 제출 시 관련 근거 명확히 작성

❓ 추가 질문은 CS 챗봇 또는 티켓으로 문의해주세요.

⚠️ 본 내용은 교육 목적이며, 매매 추천이나 가격 예측이 아닙니다."""
                st.code(template, language=None)
                if st.button("복사 완료", key=f"copied_{kw}"):
                    st.session_state[f'show_draft_{kw}'] = False
    else:
        st.info("이번 주 데이터가 없습니다.")
    
    st.markdown("""
    <div class="action-suggest">
        <p class="action-text">💡 추천 액션: 다음 라이브에서 Top 주제를 다루거나, FAQ 문서를 보강하세요.</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📝 이번 주 과제 지표")
    
    # 참여율/완료율
    total_members = len(profiles) if profiles else 1
    week_submitters = len(set(s.get('nickname') for s in week_submissions))
    participation_rate = int((week_submitters / total_members) * 100) if total_members > 0 else 0
    
    reviewed_count = len([s for s in week_submissions if s.get('reviewed')])
    completion_rate = int((reviewed_count / len(week_submissions)) * 100) if week_submissions else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("이번 주 참여율", f"{participation_rate}%")
    with col2:
        st.metric("이번 주 완료율", f"{completion_rate}%")
    
    # 주제별 제출 수
    st.markdown("**주제별 제출 수**")
    topic_counts = Counter(s.get('topic', '기타') for s in week_submissions)
    for topic, count in topic_counts.most_common():
        st.markdown(f"""
        <div class="topic-item">
            <span class="topic-name">{topic}</span>
            <span class="topic-count">{count}건</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 가장 많이 틀린 체크 항목
    st.markdown("**가장 많이 틀린 체크 항목 Top 5**")
    check_failures = Counter()
    for review in reviews:
        checklist = review.get('checklist', {})
        for item, passed in checklist.items():
            if not passed:
                check_failures[item] += 1
    
    check_names = {
        'divergence_explained': '다이버전스 설명',
        'support_resistance_mentioned': '지지/저항 언급',
        'stop_loss_clear': '손절 기준 명확',
        'position_size_appropriate': '포지션 비중 적절',
        'emotion_recorded': '감정 상태 기록'
    }
    
    for item, count in check_failures.most_common(5):
        name = check_names.get(item, item)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"❌ {name}")
        with col2:
            st.markdown(f"**{count}회**")
    
    # 스트릭 분포
    st.markdown("**스트릭 분포**")
    streaks = {'0일': 0, '1-2일': 0, '3-6일': 0, '7일+': 0}
    for profile in profiles.values():
        if isinstance(profile, dict):
            streak = profile.get('homework_streak', 0)
            if streak == 0:
                streaks['0일'] += 1
            elif streak <= 2:
                streaks['1-2일'] += 1
            elif streak <= 6:
                streaks['3-6일'] += 1
            else:
                streaks['7일+'] += 1
    
    st.markdown(f"""
    <div class="streak-bar">
        <div class="streak-item"><p class="streak-num">{streaks['0일']}</p><p class="streak-label">0일</p></div>
        <div class="streak-item"><p class="streak-num">{streaks['1-2일']}</p><p class="streak-label">1-2일</p></div>
        <div class="streak-item"><p class="streak-num">{streaks['3-6일']}</p><p class="streak-label">3-6일</p></div>
        <div class="streak-item"><p class="streak-num">{streaks['7일+']}</p><p class="streak-label">7일+</p></div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 📢 공지 템플릿 생성기")
    
    template_type = st.selectbox("공지 타입 선택", ["교육 공지", "이벤트 공지", "주간 브리핑", "주의사항 공지"])
    
    templates = {
        "교육 공지": """📚 [{제목}] 교육 안내

📅 일정: {일정}
👥 참여 조건: {조건}

📋 내용:
{내용}

⚠️ 주의사항:
- {주의1}
- {주의2}

❓ 자주 묻는 질문: CS 챗봇 또는 공지 허브 확인

⚠️ 본 교육은 매매 추천, 가격 예측, 종목 추천이 아니며, 교육 및 정보 제공 목적입니다.""",
        
        "이벤트 공지": """🎉 [{제목}] 이벤트 안내

📅 기간: {기간}
🎁 혜택: {혜택}

📋 참여 방법:
{방법}

⚠️ 유의사항:
- {유의1}
- {유의2}

⚠️ 본 이벤트는 교육 참여 독려 목적이며, 투자 권유가 아닙니다.""",
        
        "주간 브리핑": """📊 [{주차}] 주간 브리핑

✅ 이번 주 요약:
- 참여율: {참여율}%
- 과제 완료: {완료}건
- 핫토픽: {핫토픽}

📚 다음 주 일정:
{일정}

💡 운영자 코멘트:
{코멘트}

⚠️ 본 브리핑은 교육 현황 공유 목적이며, 투자 권유가 아닙니다.""",
        
        "주의사항 공지": """🚨 [{제목}] 주의사항 안내

⚠️ 중요 내용:
{내용}

✅ 확인해주세요:
- {확인1}
- {확인2}
- {확인3}

❓ 문의: CS 챗봇 또는 티켓 생성

⚠️ 본 내용은 교육 및 정보 제공 목적이며, 매매 추천이나 가격 예측이 아닙니다."""
    }
    
    st.markdown("**생성된 템플릿:**")
    st.code(templates[template_type], language=None)
    
    if st.button("📋 복사 (위 내용을 드래그하여 복사하세요)", use_container_width=True):
        st.success("템플릿을 복사해서 텔레그램에 붙여넣기 하세요!")

with tab4:
    st.markdown("### 🎫 티켓 관리")
    
    ticket_filter = st.radio("필터", ["미해결", "전체", "해결됨"], horizontal=True)
    
    if ticket_filter == "미해결":
        filtered_tickets = open_tickets
    elif ticket_filter == "해결됨":
        filtered_tickets = [t for t in tickets if t.get('status') == 'closed']
    else:
        filtered_tickets = tickets
    
    for ticket in filtered_tickets[:10]:
        status_color = "#ef4444" if ticket.get('status') == 'open' else "#22c55e"
        st.markdown(f"""
        <div class="topic-item">
            <span class="topic-name">#{ticket.get('id', 0)} - {ticket.get('query', '내용 없음')[:40]}...</span>
            <span class="topic-count" style="background: {status_color}20; color: {status_color};">{ticket.get('status', 'open')}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if ticket.get('status') == 'open':
            # 텔레그램 알림용 문구
            if st.button(f"📋 알림 문구 생성", key=f"notify_{ticket.get('id')}"):
                notify_text = f"🎫 새 티켓 #{ticket.get('id')}\n질문: {ticket.get('query', '')}\n시간: {ticket.get('timestamp', '')}"
                st.code(notify_text, language=None)
    
    if not filtered_tickets:
        st.info("해당하는 티켓이 없습니다.")

# 네비게이션
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 홈", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📢 공지 허브", use_container_width=True):
        st.switch_page("pages/06_announcements.py")
with col3:
    if st.button("✏️ 채점 보조", use_container_width=True):
        st.switch_page("pages/10_grading_assistant.py")
with col4:
    if st.button("⚙️ 관리자", use_container_width=True):
        st.switch_page("pages/05_admin.py")
