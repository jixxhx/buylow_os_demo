import streamlit as st
from datetime import datetime
import time
import textwrap
import streamlit.components.v1 as components

st.set_page_config(
    page_title="BuyLow OS",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 오프닝 애니메이션 (첫 방문 시에만)
if 'intro_shown' not in st.session_state:
    st.session_state.intro_shown = False

if not st.session_state.intro_shown:
    # 오프닝 애니메이션 (components.html로 안정 렌더링)
    # 오프닝 동안 사이드바 숨김
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
            html, body { height: 100%; overflow: hidden !important; }
            .stApp, [data-testid="stAppViewContainer"] {
                height: 100vh;
                overflow: hidden !important;
            }
            .block-container { padding: 0 !important; max-width: 100% !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    opening_html = textwrap.dedent("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500&display=swap');
        
        /* Streamlit 기본 요소 숨기기 */
        header, footer, .stDeployButton, [data-testid="stHeader"], [data-testid="stSidebar"] {
            display: none !important;
        }
        
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        .stApp {
            background: #0a0a0f !important;
        }
        
        /* 오프닝 컨테이너 */
        .opening-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0a0f 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            overflow: hidden;
        }
        
        /* 배경 그라디언트 오브 */
        .bg-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(90px);
            opacity: 0.25;
        }
        
        .orb-1 {
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
            top: 20%;
            left: 15%;
            animation: orbPulse 10s ease-in-out infinite;
        }
        
        .orb-2 {
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
            bottom: 20%;
            right: 15%;
            animation: orbPulse 12s ease-in-out infinite 2s;
        }
        
        @keyframes orbPulse {
            0%, 100% { 
                opacity: 0.25; 
                transform: translate(0, 0) scale(1); 
            }
            50% { 
                opacity: 0.55; 
                transform: translate(20px, -10px) scale(1.08); 
            }
        }
        
        /* 로고 컨테이너 */
        .opening-logo {
            position: relative;
            text-align: center;
            z-index: 10;
            opacity: 0;
            transform: translateY(10px);
            animation: logoAppear 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0.2s forwards,
                       logoFloat 6s ease-in-out 2.2s infinite;
        }

        @keyframes logoAppear {
            0% { opacity: 0; transform: translateY(12px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes logoFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
        }
        
        /* 외부 프레임 */
        .opening-frame {
            display: inline-block;
            padding: 3rem 4rem;
            position: relative;
            border: 1px solid rgba(148, 163, 184, 0);
            animation: frameFadeIn 1.8s cubic-bezier(0.22, 1, 0.36, 1) 0.4s forwards;
        }
        
        @keyframes frameFadeIn {
            0% { 
                border-color: rgba(148, 163, 184, 0);
                transform: scale(0.97);
            }
            100% { 
                border-color: rgba(148, 163, 184, 0.25);
                transform: scale(1);
            }
        }
        
        /* 프레임 코너 장식 */
        .frame-corner {
            position: absolute;
            width: 20px;
            height: 20px;
            border: 2px solid #64748b;
            opacity: 0;
            animation: cornerReveal 1s cubic-bezier(0.22, 1, 0.36, 1) 1.3s forwards;
        }
        
        .corner-tl {
            top: -8px;
            left: -8px;
            border-right: none;
            border-bottom: none;
        }
        
        .corner-br {
            bottom: -8px;
            right: -8px;
            border-left: none;
            border-top: none;
        }
        
        @keyframes cornerReveal {
            0% { 
                opacity: 0;
                transform: scale(0);
            }
            100% { 
                opacity: 1;
                transform: scale(1);
            }
        }
        
        /* 메인 타이틀 */
        .opening-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(3rem, 10vw, 5rem);
            font-weight: 600;
            letter-spacing: 0.2em;
            color: #d1d9e5;
            margin: 0;
            opacity: 0;
            text-shadow: 0 0 40px rgba(148, 163, 184, 0.25);
            animation: titleReveal 1.4s cubic-bezier(0.22, 1, 0.36, 1) 0.6s forwards;
        }
        
        @keyframes titleReveal {
            0% {
                opacity: 0;
                transform: translateY(18px);
                letter-spacing: 0.35em;
                filter: blur(6px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
                letter-spacing: 0.2em;
                filter: blur(0);
            }
        }
        
        /* 디바이더 라인 */
        .opening-line {
            height: 1px;
            background: linear-gradient(90deg, transparent, #64748b 20%, #64748b 80%, transparent);
            margin: 1.5rem auto;
            width: 0;
            opacity: 0;
            animation: lineExpand 1.2s cubic-bezier(0.22, 1, 0.36, 1) 1.2s forwards;
        }
        
        @keyframes lineExpand {
            0% {
                width: 0;
                opacity: 0;
            }
            100% {
                width: 70%;
                opacity: 1;
            }
        }
        
        /* 서브타이틀 */
        .opening-subtitle {
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(1rem, 3vw, 1.4rem);
            font-weight: 400;
            letter-spacing: 0.6em;
            color: #64748b;
            margin: 0;
            opacity: 0;
            animation: subtitleReveal 1.2s cubic-bezier(0.22, 1, 0.36, 1) 1.5s forwards;
        }
        
        @keyframes subtitleReveal {
            0% {
                opacity: 0;
                transform: translateY(10px);
                letter-spacing: 1em;
            }
            100% {
                opacity: 1;
                transform: translateY(0);
                letter-spacing: 0.6em;
            }
        }
        
        /* 로딩 인디케이터 */
        .opening-loader {
            position: absolute;
            bottom: 20%;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            opacity: 0;
            animation: loaderReveal 0.8s ease-out 2.1s forwards;
        }
        
        @keyframes loaderReveal {
            0% {
                opacity: 0;
                transform: translateX(-50%) translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
        
        .loader-bar-container {
            width: 200px;
            height: 2px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 2px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .loader-bar {
            width: 0;
            height: 100%;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);
            border-radius: 2px;
            animation: progressBar 2.8s cubic-bezier(0.4, 0, 0.2, 1) 2.2s forwards;
        }
        
        @keyframes progressBar {
            0% { width: 0; }
            100% { width: 100%; }
        }
        
        .loader-text {
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            color: #475569;
            letter-spacing: 0.2em;
        }
        
        /* 면책 문구 */
        .opening-disclaimer {
            position: absolute;
            bottom: 8%;
            left: 50%;
            transform: translateX(-50%);
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.65rem;
            color: rgba(255, 255, 255, 0.2);
            text-align: center;
            opacity: 0;
            animation: disclaimerReveal 1s ease-out 2.6s forwards;
            white-space: nowrap;
        }
        
        @keyframes disclaimerReveal {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        
        /* 반응형 */
        @media (max-width: 768px) {
            .opening-frame {
                padding: 2rem 3rem;
            }
            
            .opening-title {
                font-size: clamp(2.5rem, 12vw, 3.5rem);
            }
            
            .opening-subtitle {
                font-size: clamp(0.8rem, 3vw, 1rem);
                letter-spacing: 0.4em;
            }
            
            .loader-bar-container {
                width: 150px;
            }
            
            .opening-loader {
                bottom: 15%;
            }
            
            .opening-disclaimer {
                bottom: 5%;
                font-size: 0.55rem;
            }
            
            .bg-orb {
                filter: blur(60px);
            }
        }
</style>
</head>
<body>
<div class="opening-screen">
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>

    <div class="opening-logo">
        <div class="opening-frame">
            <div class="frame-corner corner-tl"></div>
            <div class="frame-corner corner-br"></div>

            <h1 class="opening-title">BUYLOW</h1>
            <div class="opening-line"></div>
            <p class="opening-subtitle">STRATEGY OS</p>
        </div>
    </div>

    <div class="opening-loader">
        <div class="loader-bar-container">
            <div class="loader-bar"></div>
        </div>
        <div class="loader-text">LOADING...</div>
    </div>

    <div class="opening-disclaimer">
        Trading Education Platform · Not Investment Advice
    </div>
</div>
</body>
</html>
""")
    components.html(opening_html, height=720, scrolling=False)
    
    # 4.5초 후 메인 화면으로 전환
    time.sleep(4.5)
    st.session_state.intro_shown = True
    st.rerun()


# 미래지향적 + 대중친화적 CSS (진입 애니메이션 포함)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #0f0f14;
        --bg-card: #18181f;
        --bg-card-hover: #1e1e28;
        --border: rgba(255,255,255,0.08);
        --border-hover: rgba(255,255,255,0.15);
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
        --gradient-card: linear-gradient(145deg, rgba(99,102,241,0.05) 0%, rgba(139,92,246,0.02) 100%);
    }
    
    * { box-sizing: border-box; }
    
    .stApp {
        background: var(--bg-dark);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.15), transparent),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.1), transparent);
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg-card);
        border-right: 1px solid var(--border);
    }
    
    /* 애니메이션 정의 */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes lineExpand {
        from { width: 0; opacity: 0; }
        to { width: 60%; opacity: 1; }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.2); }
        50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }
    }
    
    /* 페이지 진입 애니메이션 */
    .stApp > section > div {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* 메인 헤더 */
    .main-header {
        text-align: center;
        padding: 3rem 1rem;
        animation: scaleIn 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* BuyLow Strategy Inc. 스타일 로고 */
    .logo-frame {
        display: inline-block;
        padding: 2rem 3rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        margin-bottom: 1.5rem;
        position: relative;
        animation: scaleIn 1.2s cubic-bezier(0.16, 1, 0.3, 1), glow 4s ease-in-out infinite 1.2s;
        background: rgba(15, 15, 20, 0.5);
        backdrop-filter: blur(10px);
    }
    
    .logo-frame::before,
    .logo-frame::after {
        content: '';
        position: absolute;
        width: 12px;
        height: 12px;
        border: 2px solid #64748b;
        animation: fadeIn 0.5s ease-out 0.6s both;
    }
    
    .logo-frame::before {
        top: -6px;
        left: -6px;
        border-right: none;
        border-bottom: none;
    }
    
    .logo-frame::after {
        bottom: -6px;
        right: -6px;
        border-left: none;
        border-top: none;
    }
    
    .logo-main-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 600;
        letter-spacing: 0.15em;
        color: #c8d0dc;
        margin: 0;
        line-height: 1;
        text-transform: uppercase;
        text-shadow: 0 0 40px rgba(148, 163, 184, 0.4);
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
    }
    
    .logo-sub-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(0.9rem, 2.5vw, 1.3rem);
        font-weight: 500;
        letter-spacing: 0.4em;
        color: #64748b;
        margin: 0.75rem 0 0 0;
        text-transform: uppercase;
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
    }
    
    .logo-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #64748b, transparent);
        margin: 0.75rem auto;
        animation: lineExpand 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both;
    }
    
    .main-subtitle {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: clamp(1rem, 2.5vw, 1.25rem);
        color: var(--text-secondary);
        font-weight: 400;
        margin: 1.5rem 0 0 0;
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.7s both;
    }
    
    /* 섹션 타이틀 */
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(1.25rem, 3vw, 1.5rem);
        font-weight: 700;
        color: var(--text-primary);
        margin: 2.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.8s both;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 24px;
        background: var(--gradient-primary);
        border-radius: 2px;
    }
    
    /* 카드 그리드 - 반응형 */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.25rem;
        margin: 1.5rem 0;
    }
    
    /* 기능 카드 */
    .feature-card {
        background: var(--bg-card);
        background-image: var(--gradient-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.75rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) backwards;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:nth-child(1) { animation-delay: 0.9s; }
    .feature-card:nth-child(2) { animation-delay: 1.0s; }
    .feature-card:nth-child(3) { animation-delay: 1.1s; }
    .feature-card:nth-child(4) { animation-delay: 1.2s; }
    .feature-card:nth-child(5) { animation-delay: 1.3s; }
    .feature-card:nth-child(6) { animation-delay: 1.4s; }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-hover);
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 60px var(--accent-glow);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .card-icon {
        width: 56px;
        height: 56px;
        background: var(--gradient-primary);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 20px var(--accent-glow);
    }
    
    .card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .card-desc {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin: 0;
    }
    
    /* 통계 그리드 */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out backwards;
    }
    
    .stat-card:nth-child(1) { animation-delay: 0.15s; }
    .stat-card:nth-child(2) { animation-delay: 0.25s; }
    .stat-card:nth-child(3) { animation-delay: 0.35s; }
    .stat-card:nth-child(4) { animation-delay: 0.45s; }
    
    .stat-card:hover {
        border-color: var(--accent-primary);
        transform: scale(1.02);
    }
    
    .stat-value {
        font-family: 'Space Mono', monospace;
        font-size: clamp(1.5rem, 4vw, 2rem);
        font-weight: 700;
        color: var(--accent-primary);
        margin: 0;
    }
    
    .stat-label {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }
    
    /* 공지사항 */
    .notice-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out backwards;
    }
    
    .notice-card:hover {
        border-color: var(--border-hover);
        transform: translateX(8px);
    }
    
    .notice-badge {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent-primary);
        background: rgba(99,102,241,0.15);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        white-space: nowrap;
    }
    
    .notice-text {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.95rem;
        color: var(--text-secondary);
        flex: 1;
    }
    
    /* 경고 박스 */
    .warning-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1.5rem 0;
        animation: fadeIn 0.5s ease-out;
    }
    
    .warning-box p {
        font-family: 'Noto Sans KR', sans-serif;
        color: #fca5a5;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--gradient-primary);
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px var(--accent-glow);
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        padding: 3rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border);
        animation: fadeIn 0.8s ease-out;
    }
    
    .footer-brand {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.5rem 0;
    }
    
    .footer-text {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.85rem;
        color: var(--text-muted);
        margin: 0.25rem 0;
    }
    
    /* 반응형 */
    @media (max-width: 768px) {
        .main-header { padding: 2rem 1rem; }
        .logo-frame { padding: 1.5rem 2rem; }
        .logo-main-text { letter-spacing: 0.1em; }
        .logo-sub-text { letter-spacing: 0.25em; font-size: 0.75rem; }
        .card-grid { grid-template-columns: 1fr; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .feature-card { padding: 1.25rem; }
        .notice-card { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
    }
    
    /* Streamlit 요소 숨김/스타일링 */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1200px;
    }
    
    @media (max-width: 768px) {
        .block-container { padding: 0.5rem 1rem 1rem 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header">
    <div class="logo-frame">
        <h1 class="logo-main-text">BUYLOW</h1>
        <div class="logo-divider"></div>
        <p class="logo-sub-text">STRATEGY OS</p>
    </div>
    <p class="main-subtitle">트레이딩 팀 운영 · 교육 · 리스크 관리 플랫폼</p>
</div>
""", unsafe_allow_html=True)

# 경고
st.markdown("""
<div class="warning-box">
    <p>⚠️ 이 시스템은 매수/매도 추천, 가격 예측, 종목 추천을 제공하지 않습니다. 교육 목적으로만 사용됩니다.</p>
</div>
""", unsafe_allow_html=True)

# 기능 카드
st.markdown('<h2 class="section-title">주요 기능</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="card-grid">
    <div class="feature-card">
        <div class="card-icon">💬</div>
        <h3 class="card-title">CS 챗봇</h3>
        <p class="card-desc">키워드 기반 질문 응답 시스템으로 32개 지식베이스 문서에서 답변을 찾아드립니다.</p>
    </div>
    <div class="feature-card">
        <div class="card-icon">📚</div>
        <h3 class="card-title">교육 시스템</h3>
        <p class="card-desc">8문항 진단 퀴즈와 맞춤형 학습 추천, 과제 제출 및 피드백을 제공합니다.</p>
    </div>
    <div class="feature-card">
        <div class="card-icon">🛡️</div>
        <h3 class="card-title">리스크 매니저</h3>
        <p class="card-desc">매매일지 작성 및 규칙 위반 자동 감지, 위험 점수 산출로 리스크를 관리합니다.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 신규 멤버 / 공지 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 온보딩 시작 (신규 멤버)", use_container_width=True, type="primary"):
        st.switch_page("pages/07_onboarding.py")
with col2:
    if st.button("📢 공지 허브", use_container_width=True):
        st.switch_page("pages/06_announcements.py")

# 주요 기능 버튼
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💬 CS 챗봇", use_container_width=True):
        st.switch_page("pages/01_cs_chat.py")
with col2:
    if st.button("📚 퀴즈 시작", use_container_width=True):
        st.switch_page("pages/02_quiz.py")
with col3:
    if st.button("🛡️ 리스크 체크", use_container_width=True):
        st.switch_page("pages/04_risk_check.py")

# 통계
st.markdown('<h2 class="section-title">시스템 현황</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <p class="stat-value">47</p>
        <p class="stat-label">활성 멤버</p>
    </div>
    <div class="stat-card">
        <p class="stat-value">32</p>
        <p class="stat-label">KB 문서</p>
    </div>
    <div class="stat-card">
        <p class="stat-value">8</p>
        <p class="stat-label">퀴즈 문항</p>
    </div>
    <div class="stat-card">
        <p class="stat-value" style="color: #22c55e;">●</p>
        <p class="stat-label">시스템 정상</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 공지사항
st.markdown('<h2 class="section-title">공지사항</h2>', unsafe_allow_html=True)

notices = [
    ("2026.01.27", "BuyLow OS v3.0 출시 — 새로운 UI와 모바일 최적화"),
    ("2026.01.25", "매주 화/목 20:00 라이브 교육 진행"),
    ("2026.01.20", "커뮤니티 규칙 업데이트: 종목 추천 및 투자 권유 금지"),
]

for date, text in notices:
    st.markdown(f"""
    <div class="notice-card">
        <span class="notice-badge">{date}</span>
        <span class="notice-text">{text}</span>
    </div>
    """, unsafe_allow_html=True)

# 퀵 액세스
st.markdown('<h2 class="section-title">바로가기</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📤 과제 제출", use_container_width=True, key="q1"):
        st.switch_page("pages/03_homework.py")
with col2:
    if st.button("📚 교육 콘텐츠", use_container_width=True, key="q2"):
        st.switch_page("pages/09_content_library.py")
with col3:
    if st.button("🔓 해설 모음", use_container_width=True, key="q3"):
        st.switch_page("pages/11_unlocked_lessons.py")
with col4:
    if st.button("🎯 심화 문제", use_container_width=True, key="q4"):
        st.switch_page("pages/12_advanced_practice.py")

# 운영자용
st.markdown('<h2 class="section-title">운영자 전용</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⚙️ 관리자", use_container_width=True, key="a1"):
        st.switch_page("pages/05_admin.py")
with col2:
    if st.button("📊 대시보드", use_container_width=True, key="a2"):
        st.switch_page("pages/08_operator_dashboard.py")
with col3:
    if st.button("✏️ 채점 보조", use_container_width=True, key="a3"):
        st.switch_page("pages/10_grading_assistant.py")
with col4:
    if st.button("📢 공지 관리", use_container_width=True, key="a4"):
        st.switch_page("pages/06_announcements.py")

# 푸터
st.markdown("""
<div class="footer">
    <p class="footer-brand" style="font-family: 'Cormorant Garamond', serif; letter-spacing: 0.1em;">BUYLOW STRATEGY</p>
    <p class="footer-text">⚠️ 교육 목적 시스템 | 투자 권유 아님 | 모든 결정은 본인 책임</p>
    <p class="footer-text">© 2026 BuyLow Strategy Inc.</p>
</div>
""", unsafe_allow_html=True)

