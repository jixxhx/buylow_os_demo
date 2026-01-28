import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from ui.sidebar import render_sidebar

st.set_page_config(page_title="채점 보조 - BuyLow", page_icon="✏️", layout="wide", initial_sidebar_state="collapsed")
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
    
    .filter-bar { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0; padding: 1rem; background: var(--bg-card); border-radius: 12px; }
    
    .submission-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; animation: fadeInUp 0.5s ease-out; }
    .submission-card.reviewed { border-left: 4px solid var(--success); }
    .submission-card.pending { border-left: 4px solid var(--warning); }
    
    .submission-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
    .submission-info { flex: 1; }
    .submission-nickname { font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 700; color: var(--text-primary); }
    .submission-meta { font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem; }
    .topic-badge { font-family: 'Noto Sans KR', sans-serif; font-size: 0.75rem; padding: 0.3rem 0.75rem; border-radius: 12px; background: rgba(99,102,241,0.2); color: var(--accent-primary); }
    
    .submission-content { font-family: 'Noto Sans KR', sans-serif; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.7; background: var(--bg-dark); border-radius: 8px; padding: 1rem; margin: 1rem 0; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }
    
    .checklist-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 0.75rem; margin: 1rem 0; }
    .check-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: var(--bg-dark); border-radius: 8px; }
    .check-label { font-family: 'Noto Sans KR', sans-serif; font-size: 0.85rem; color: var(--text-secondary); }
    
    .result-summary { display: flex; gap: 1rem; align-items: center; padding: 1rem; background: var(--bg-dark); border-radius: 8px; margin: 1rem 0; }
    .result-score { font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; }
    
    .stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-primary); border-radius: 10px; font-size: 0.85rem; transition: all 0.3s ease; }
    .stButton > button:hover { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-color: transparent; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

SUBMISSIONS_PATH = Path("data/homework_submissions.json")
REVIEWS_PATH = Path("data/homework_reviews.json")
PROFILES_PATH = Path("data/member_profiles.json")
UNLOCKS_PATH = Path("data/unlocks.json")

def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if 'submissions' in str(path) or 'reviews' in str(path) else {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 헤더
st.markdown("""
<div class="page-header">
    <h1 class="page-title">✏️ 과제 채점 보조</h1>
</div>
""", unsafe_allow_html=True)

submissions = load_json(SUBMISSIONS_PATH)
reviews = load_json(REVIEWS_PATH)

# 필터
col1, col2 = st.columns(2)
with col1:
    topic_filter = st.selectbox("주제 필터", ["전체", "다이버전스", "지지저항", "SRL", "아래꼬리"])
with col2:
    status_filter = st.selectbox("상태 필터", ["미채점", "전체", "채점완료"])

# 필터링
filtered = submissions
if topic_filter != "전체":
    filtered = [s for s in filtered if s.get('topic') == topic_filter]
if status_filter == "미채점":
    filtered = [s for s in filtered if not s.get('reviewed')]
elif status_filter == "채점완료":
    filtered = [s for s in filtered if s.get('reviewed')]

st.markdown(f"**{len(filtered)}개의 제출물**")

# 제출물 표시
for sub in filtered:
    reviewed = sub.get('reviewed', False)
    card_class = "reviewed" if reviewed else "pending"
    status_text = "✅ 채점완료" if reviewed else "⏳ 대기중"
    
    st.markdown(f"""
    <div class="submission-card {card_class}">
        <div class="submission-header">
            <div class="submission-info">
                <p class="submission-nickname">👤 {sub.get('nickname', '익명')}</p>
                <p class="submission-meta">{sub.get('submitted_at', '')} | {status_text}</p>
            </div>
            <span class="topic-badge">{sub.get('topic', '기타')}</span>
        </div>
        <div class="submission-content">{sub.get('content', '내용 없음')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not reviewed:
        with st.expander(f"📋 채점하기 (#{sub.get('id')})"):
            st.markdown("**체크리스트:**")
            
            c1 = st.checkbox("다이버전스가 어디서 보였는지 설명했는가", key=f"c1_{sub.get('id')}")
            c2 = st.checkbox("지지/저항 또는 SRL 구간을 근거로 썼는가", key=f"c2_{sub.get('id')}")
            c3 = st.checkbox("손절 기준이 명확한가", key=f"c3_{sub.get('id')}")
            c4 = st.checkbox("포지션 비중과 레버리지가 적절한가", key=f"c4_{sub.get('id')}")
            c5 = st.checkbox("감정 상태를 기록했는가", key=f"c5_{sub.get('id')}")
            
            feedback = st.text_area("피드백 (선택)", placeholder="피드백을 입력하세요...", key=f"fb_{sub.get('id')}")
            
            passed = sum([c1, c2, c3, c4, c5])
            score_color = "#22c55e" if passed >= 4 else "#f59e0b" if passed >= 2 else "#ef4444"
            
            st.markdown(f"""
            <div class="result-summary">
                <span class="result-score" style="color: {score_color};">{passed}/5</span>
                <span style="font-family: 'Noto Sans KR', sans-serif; color: var(--text-secondary);">항목 통과</span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💾 채점 저장", key=f"save_{sub.get('id')}", type="primary"):
                # 리뷰 저장
                review = {
                    "submission_id": sub.get('id'),
                    "reviewer": "operator",
                    "reviewed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "checklist": {
                        "divergence_explained": c1,
                        "support_resistance_mentioned": c2,
                        "stop_loss_clear": c3,
                        "position_size_appropriate": c4,
                        "emotion_recorded": c5
                    },
                    "passed_count": passed,
                    "total_count": 5,
                    "feedback": feedback
                }
                reviews.append(review)
                save_json(REVIEWS_PATH, reviews)
                
                # 제출물 상태 업데이트
                for s in submissions:
                    if s.get('id') == sub.get('id'):
                        s['reviewed'] = True
                        s['review_result'] = {"passed": passed, "total": 5}
                save_json(SUBMISSIONS_PATH, submissions)
                
                # 멤버 프로필 업데이트 (과제 카운트, 언락)
                profiles = load_json(PROFILES_PATH)
                nickname = sub.get('nickname')
                if nickname and nickname in profiles:
                    profiles[nickname]['homework_count'] = profiles[nickname].get('homework_count', 0) + 1
                    save_json(PROFILES_PATH, profiles)
                
                # 언락 체크
                unlocks = load_json(UNLOCKS_PATH)
                topic = sub.get('topic')
                if nickname and nickname in unlocks:
                    topic_map = {
                        '다이버전스': ('divergence_lesson', 'divergence_advanced'),
                        '지지저항': ('support_resistance_lesson', 'support_resistance_advanced'),
                        'SRL': ('srl_lesson', 'srl_advanced'),
                        '아래꼬리': ('tail_candle_lesson', 'tail_candle_advanced')
                    }
                    if topic in topic_map:
                        lesson_key, advanced_key = topic_map[topic]
                        # 첫 제출 -> 해설 언락
                        topic_submissions = [s for s in submissions if s.get('nickname') == nickname and s.get('topic') == topic]
                        if len(topic_submissions) >= 1:
                            unlocks[nickname][lesson_key] = True
                        if len(topic_submissions) >= 2:
                            unlocks[nickname][advanced_key] = True
                        save_json(UNLOCKS_PATH, unlocks)
                
                st.success("✅ 채점이 저장되었습니다!")
                st.rerun()
    else:
        # 이미 채점된 경우 결과 표시
        review = next((r for r in reviews if r.get('submission_id') == sub.get('id')), None)
        if review:
            passed = review.get('passed_count', 0)
            total = review.get('total_count', 5)
            st.markdown(f"**채점 결과:** {passed}/{total} 통과")
            if review.get('feedback'):
                st.caption(f"피드백: {review.get('feedback')}")

if not filtered:
    st.info("해당하는 제출물이 없습니다.")

# 네비게이션
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 홈", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📊 운영자 대시보드", use_container_width=True):
        st.switch_page("pages/08_operator_dashboard.py")
with col3:
    if st.button("⚙️ 관리자", use_container_width=True):
        st.switch_page("pages/05_admin.py")
