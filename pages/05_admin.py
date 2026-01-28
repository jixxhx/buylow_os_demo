import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="관리자 - BuyLow", page_icon="⚙️", layout="wide", initial_sidebar_state="collapsed")
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
    
    .page-header { padding: 1.5rem 0; animation: fadeInUp 0.6s ease-out; }
    .page-title { font-family: 'Outfit', sans-serif; font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; color: var(--text-primary); margin: 0; }
    
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin: 1rem 0; }
    .stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; text-align: center; animation: fadeInUp 0.5s ease-out backwards; transition: all 0.3s ease; }
    .stat-card:hover { border-color: var(--accent-primary); }
    .stat-value { font-family: 'Space Mono', monospace; font-size: 1.75rem; font-weight: 700; }
    .stat-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }
    
    .section-header { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: 0.5rem; }
    .section-header::before { content: ''; width: 4px; height: 18px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 2px; }
    
    .ticket-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; animation: fadeInUp 0.4s ease-out; }
    .ticket-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
    .ticket-id { font-family: 'Space Mono', monospace; font-size: 0.8rem; color: var(--accent-primary); background: rgba(99,102,241,0.15); padding: 0.2rem 0.6rem; border-radius: 12px; }
    .ticket-status { font-family: 'Noto Sans KR', sans-serif; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 12px; }
    .status-open { background: rgba(239,68,68,0.2); color: var(--danger); }
    .status-closed { background: rgba(34,197,94,0.2); color: var(--success); }
    .ticket-query { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-primary); }
    .ticket-meta { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: var(--text-muted); margin-top: 0.25rem; }
    
    .template-section { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
    .template-output { background: var(--bg-dark); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); white-space: pre-wrap; margin: 1rem 0; max-height: 300px; overflow-y: auto; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 10px; font-size: 0.85rem; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    .stTabs [data-baseweb="tab-list"] { background: var(--bg-card); border-radius: 12px; padding: 0.25rem; }
    .stTabs [data-baseweb="tab"] { font-family: 'Outfit', sans-serif; font-weight: 600; color: var(--text-secondary); border-radius: 8px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

# 데이터 경로
LOGS_PATH = Path("data/logs.json")
TICKETS_PATH = Path("data/tickets.json")
ANNOUNCEMENTS_PATH = Path("data/announcements.json")

def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">⚙️ 관리자 페이지</h1>
</div>
""", unsafe_allow_html=True)

logs = load_json(LOGS_PATH)
tickets = load_json(TICKETS_PATH)
announcements = load_json(ANNOUNCEMENTS_PATH)

today = datetime.now().strftime("%Y-%m-%d")
today_logs = [l for l in logs if l.get('timestamp', '').startswith(today)]
open_tickets = [t for t in tickets if t.get('status') == 'open']

cs_logs = [l for l in logs if l.get('type') == 'cs_query']
homework_logs = [l for l in logs if l.get('type') == 'homework_submission']
risk_logs = [l for l in logs if l.get('type') == 'risk_check']

# 통계
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card"><p class="stat-value" style="color: #6366f1;">{len(logs)}</p><p class="stat-label">전체 로그</p></div>
    <div class="stat-card"><p class="stat-value" style="color: #22c55e;">{len(today_logs)}</p><p class="stat-label">오늘 로그</p></div>
    <div class="stat-card"><p class="stat-value" style="color: {'#ef4444' if open_tickets else '#22c55e'};">{len(open_tickets)}</p><p class="stat-label">미처리 티켓</p></div>
    <div class="stat-card"><p class="stat-value" style="color: #f59e0b;">{len(announcements)}</p><p class="stat-label">공지 수</p></div>
</div>
""", unsafe_allow_html=True)

# 빠른 링크
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 운영자 대시보드", use_container_width=True):
        st.switch_page("pages/08_operator_dashboard.py")
with col2:
    if st.button("✏️ 채점 보조", use_container_width=True):
        st.switch_page("pages/10_grading_assistant.py")

# 탭
tab1, tab2, tab3, tab4 = st.tabs(["📢 공지 템플릿", "🎫 티켓", "📋 로그", "📊 통계"])

with tab1:
    st.markdown('<p class="section-header">공지 템플릿 생성기</p>', unsafe_allow_html=True)
    
    template_type = st.selectbox("공지 타입", ["교육 공지", "이벤트 공지", "주간 브리핑", "주의사항 공지", "과제 안내"])
    
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("공지 제목", placeholder="제목을 입력하세요")
    with col2:
        tag = st.selectbox("태그", ["교육 일정", "이벤트", "브리핑", "주의사항", "과제 안내", "멤버십 안내"])
    
    # 템플릿별 입력 필드
    if template_type == "교육 공지":
        schedule = st.text_input("일정", placeholder="예: 화요일 20:00")
        condition = st.text_input("참여 조건", placeholder="예: 기초 과제 1회 이상 제출")
        content = st.text_area("교육 내용", placeholder="교육 내용을 입력하세요")
        
        template = f"""📚 [{title}] 교육 안내

📅 일정: {schedule}
👥 참여 조건: {condition}

📋 내용:
{content}

📖 교육 자료 읽는 순서:
1. 다이버전스 기초
2. 지지와 저항
3. SRL 지표 설정
4. 아래꼬리 캔들 분석

📤 과제 제출 방법:
웹에서 주제 선택 후 분석 내용 작성 → 제출 시 추가 콘텐츠 언락

❓ 자주 묻는 질문: CS 챗봇 또는 공지 허브 확인

⚠️ 본 교육은 매매 추천, 가격 예측, 종목 추천이 아니며, 교육 및 정보 제공 목적입니다."""

    elif template_type == "이벤트 공지":
        period = st.text_input("기간", placeholder="예: 1/27 ~ 2/3")
        benefit = st.text_input("혜택", placeholder="예: 과제 제출 시 추가 포인트")
        method = st.text_area("참여 방법", placeholder="참여 방법을 입력하세요")
        
        template = f"""🎉 [{title}] 이벤트 안내

📅 기간: {period}
🎁 혜택: {benefit}

📋 참여 방법:
{method}

⚠️ 유의사항:
- 이벤트는 예고 없이 변경될 수 있습니다
- 부정 참여 시 혜택이 취소될 수 있습니다

⚠️ 본 이벤트는 교육 참여 독려 목적이며, 투자 권유가 아닙니다."""

    elif template_type == "주간 브리핑":
        week = st.text_input("주차", placeholder="예: 1월 4주차")
        participation = st.text_input("참여율", placeholder="예: 78")
        completed = st.text_input("과제 완료", placeholder="예: 45")
        hot_topic = st.text_input("핫토픽", placeholder="예: 다이버전스")
        next_schedule = st.text_area("다음 주 일정", placeholder="다음 주 일정")
        comment = st.text_area("운영자 코멘트", placeholder="코멘트")
        
        template = f"""📊 [{week}] 주간 브리핑

✅ 이번 주 요약:
- 참여율: {participation}%
- 과제 완료: {completed}건
- 핫토픽: {hot_topic}

📚 다음 주 일정:
{next_schedule}

💡 운영자 코멘트:
{comment}

⚠️ 본 브리핑은 교육 현황 공유 목적이며, 투자 권유가 아닙니다."""

    elif template_type == "주의사항 공지":
        warning_content = st.text_area("주의 내용", placeholder="주의 내용을 입력하세요")
        check1 = st.text_input("확인사항 1", placeholder="예: 손절가 설정 여부")
        check2 = st.text_input("확인사항 2", placeholder="예: 포지션 비중 확인")
        check3 = st.text_input("확인사항 3", placeholder="예: 감정 상태 체크")
        
        template = f"""🚨 [{title}] 주의사항 안내

⚠️ 중요 내용:
{warning_content}

✅ 확인해주세요:
- {check1}
- {check2}
- {check3}

❓ 문의: CS 챗봇 또는 티켓 생성

⚠️ 본 내용은 교육 및 정보 제공 목적이며, 매매 추천이나 가격 예측이 아닙니다."""

    else:  # 과제 안내
        topic = st.selectbox("과제 주제", ["다이버전스", "지지저항", "SRL", "아래꼬리"])
        deadline = st.text_input("제출 기한", placeholder="예: 이번 주 일요일까지")
        requirement = st.text_area("요구사항", placeholder="과제 요구사항")
        
        template = f"""📝 [{title}] 과제 안내

📋 주제: {topic} 실습
⏰ 제출 기한: {deadline}

✅ 요구사항:
{requirement}

📤 제출 방법:
웹 → 과제 제출 → '{topic}' 선택 → 분석 내용 작성 → 제출

🔓 제출 혜택:
- 1회 제출: {topic} 해설 페이지 언락
- 2회 제출: {topic} 심화 문제 언락

⚠️ 본 과제는 학습 목적입니다. 매매 추천이나 종목 추천을 포함하지 마세요."""
    
    st.markdown(f'<div class="template-output">{template}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 텔레그램용 복사", use_container_width=True):
            st.code(template, language=None)
            st.success("위 내용을 복사해서 텔레그램에 붙여넣기 하세요!")
    
    with col2:
        pinned = st.checkbox("상단 고정")
        if st.button("💾 공지로 저장", use_container_width=True):
            if title:
                new_id = len(announcements) + 1
                announcements.append({
                    "id": new_id,
                    "title": title,
                    "tag": tag,
                    "content": template,
                    "pinned": pinned,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "related_faq": [],
                    "next_actions": []
                })
                save_json(ANNOUNCEMENTS_PATH, announcements)
                st.success(f"✅ 공지 #{new_id} 저장 완료!")
            else:
                st.error("제목을 입력해주세요")

with tab2:
    st.markdown('<p class="section-header">티켓 관리</p>', unsafe_allow_html=True)
    
    ticket_filter = st.radio("상태", ["미처리", "전체", "완료"], horizontal=True)
    
    if ticket_filter == "미처리":
        filtered_tickets = open_tickets
    elif ticket_filter == "완료":
        filtered_tickets = [t for t in tickets if t.get('status') == 'closed']
    else:
        filtered_tickets = tickets
    
    if filtered_tickets:
        for ticket in filtered_tickets[:15]:
            status_class = "status-open" if ticket.get('status') == 'open' else "status-closed"
            status_text = "미처리" if ticket.get('status') == 'open' else "완료"
            
            st.markdown(f"""
            <div class="ticket-card">
                <div class="ticket-header">
                    <span class="ticket-id">#{ticket.get('id', 0):04d}</span>
                    <span class="ticket-status {status_class}">{status_text}</span>
                </div>
                <p class="ticket-query">{ticket.get('query', '내용 없음')[:60]}...</p>
                <p class="ticket-meta">{ticket.get('timestamp', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if ticket.get('status') == 'open':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✓ 처리 완료", key=f"close_{ticket.get('id')}"):
                        for t in tickets:
                            if t.get('id') == ticket.get('id'):
                                t['status'] = 'closed'
                                t['closed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_json(TICKETS_PATH, tickets)
                        st.rerun()
                with col2:
                    if st.button("📋 알림 복사", key=f"notify_{ticket.get('id')}"):
                        notify = f"🎫 티켓 #{ticket.get('id')} 처리 완료\n질문: {ticket.get('query', '')[:30]}..."
                        st.code(notify, language=None)
    else:
        st.info("해당하는 티켓이 없습니다")

with tab3:
    st.markdown('<p class="section-header">최근 로그</p>', unsafe_allow_html=True)
    
    log_filter = st.selectbox("유형", ["전체", "CS", "과제", "리스크"])
    
    if log_filter == "CS":
        filtered = cs_logs
    elif log_filter == "과제":
        filtered = homework_logs
    elif log_filter == "리스크":
        filtered = risk_logs
    else:
        filtered = logs
    
    if filtered:
        df_data = []
        for l in filtered[-30:][::-1]:
            log_type = l.get('type', 'unknown')
            type_labels = {'cs_query': '💬', 'quiz_result': '📚', 'homework_submission': '📤', 'risk_check': '🛡️'}
            
            summary = ""
            if log_type == 'cs_query':
                summary = l.get('query', '')[:30]
            elif log_type == 'homework_submission':
                summary = l.get('topic', '')
            elif log_type == 'risk_check':
                summary = f"{l.get('symbol', '')} {l.get('risk_score', 0)}점"
            
            df_data.append({"시간": l.get('timestamp', '')[:16], "유형": type_labels.get(log_type, '?'), "내용": summary})
        
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, height=350)
    else:
        st.info("로그가 없습니다")

with tab4:
    st.markdown('<p class="section-header">통계</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**기능별 사용량**")
        usage = pd.DataFrame({"기능": ["CS", "과제", "리스크"], "횟수": [len(cs_logs), len(homework_logs), len(risk_logs)]})
        st.bar_chart(usage.set_index("기능"))
    
    with col2:
        if risk_logs:
            st.markdown("**리스크 점수 분포**")
            high = len([l for l in risk_logs if l.get('risk_score', 0) >= 50])
            med = len([l for l in risk_logs if 30 <= l.get('risk_score', 0) < 50])
            low = len([l for l in risk_logs if l.get('risk_score', 0) < 30])
            st.metric("🔴 고위험", high)
            st.metric("🟡 주의", med)
            st.metric("🟢 안전", low)

# 네비게이션
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 홈", use_container_width=True, key="n1"):
        st.switch_page("Home.py")
with col2:
    if st.button("📢 공지 허브", use_container_width=True, key="n2"):
        st.switch_page("pages/06_announcements.py")
with col3:
    if st.button("📊 대시보드", use_container_width=True, key="n3"):
        st.switch_page("pages/08_operator_dashboard.py")
with col4:
    if st.button("✏️ 채점", use_container_width=True, key="n4"):
        st.switch_page("pages/10_grading_assistant.py")
