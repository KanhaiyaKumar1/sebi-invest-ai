import streamlit as st
import requests
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

st.set_page_config(
    page_title="InvestAI — SEBI Adviser",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #080c10 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 16px !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,212,170,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,170,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1a2332 !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

/* Labels */
.stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label {
    font-size: 16px !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    background: #0d1117 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 6px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 16px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #00d4aa !important;
    box-shadow: 0 0 0 2px rgba(0,212,170,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00d4aa, #00a88a) !important;
    color: #080c10 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00ffcc, #00d4aa) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,212,170,0.3) !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: #0d1117 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"]:hover { border-color: #00d4aa !important; }

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, rgba(0,212,170,0.12), rgba(0,212,170,0.06));
    border: 1px solid rgba(0,212,170,0.25);
    border-radius: 14px 14px 2px 14px;
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0 0.5rem 4rem;
    font-size: 16px;
    line-height: 1.7;
    color: #e2e8f0;
}
.chat-ai {
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-radius: 14px 14px 14px 2px;
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 4rem 0.5rem 0;
    font-size: 16px;
    line-height: 1.7;
    color: #cbd5e1;
}
.chat-label-user {
    text-align: right;
    font-size: 12px;
    color: #00d4aa;
    margin-bottom: 0.2rem;
    letter-spacing: 0.1em;
}
.chat-label-ai {
    font-size: 12px;
    color: #4a6741;
    margin-bottom: 0.2rem;
    letter-spacing: 0.1em;
}

/* Page title */
.page-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.page-sub {
    font-size: 13px;
    color: #4a6741;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
}

/* Disclaimer */
.disclaimer {
    background: #0d1a0d;
    border: 1px solid #1a3a1a;
    border-left: 3px solid #22c55e;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 14px;
    color: #4ade80;
    margin-bottom: 1.2rem;
    line-height: 1.5;
}

/* Card */
.card {
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-radius: 10px;
    padding: 1.3rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    color: #4a6741;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

/* Quick Q */
.quick-q {
    display: block;
    width: 100%;
    text-align: left;
    background: #111820;
    border: 1px solid #1e2d3d;
    border-radius: 6px;
    color: #64748b;
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    padding: 0.55rem 0.8rem;
    cursor: pointer;
    margin-bottom: 0.4rem;
    transition: all 0.15s;
}
.quick-q:hover { border-color: #00d4aa; color: #00d4aa; }

/* Table */
table { width: 100%; border-collapse: collapse; font-size: 15px; }
th {
    background: #111820;
    color: #4a6741;
    font-weight: 500;
    padding: 0.6rem 0.8rem;
    text-align: left;
    letter-spacing: 0.06em;
    font-size: 13px;
    text-transform: uppercase;
    border-bottom: 1px solid #1e2d3d;
}
td { padding: 0.6rem 0.8rem; border-bottom: 1px solid #111820; color: #cbd5e1; }
tr:hover td { background: #0a1628; }

/* SIP result */
.sip-result {
    background: linear-gradient(135deg, #0d2018, #0d1a2a);
    border: 1px solid #1a3a2a;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
}
.sip-amount {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #00d4aa;
    letter-spacing: -0.04em;
}

/* Alloc bar */
.alloc-bg { background: #1e2d3d; border-radius: 4px; height: 8px; overflow: hidden; margin: 0.3rem 0 0.8rem; }
.alloc-fill { height: 100%; border-radius: 4px; }

/* Logo */
.logo-text {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.2rem;
    color: #00d4aa;
}
.logo-sub { font-size: 11px; color: #4a6741; letter-spacing: 0.18em; margin-top: 0.2rem; }

/* Login */
.login-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    color: #00d4aa;
    text-align: center;
    letter-spacing: -0.04em;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1e2d3d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00d4aa; }
</style>
""", unsafe_allow_html=True)

# ─── SEBI SYSTEM PROMPT ────────────────────────────────────────────────────────
SEBI_PROMPT = """You are a SEBI (Securities and Exchange Board of India) registered Investment Adviser AI assistant named InvestAI. You help Indian investors with:

1. Investment planning and portfolio analysis
2. Mutual funds, stocks, bonds, gold information
3. SIP (Systematic Investment Plan) guidance
4. Tax-saving investments (ELSS, PPF, NPS)
5. Financial goal planning (retirement, education, home)
6. Risk assessment and portfolio diversification

STRICT RULES:
- Always add disclaimer: "⚠️ Investments are subject to market risks. Please consult a registered SEBI adviser before investing."
- Never give direct buy/sell recommendations for specific stocks
- Never promise guaranteed returns
- Always mention past performance is not indicative of future returns
- Be helpful, friendly, and use simple Hindi/English mix when appropriate
- Give educational information, not personalized advice

Always respond in a helpful, professional manner."""

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
for key, val in {
    'logged_in': False, 'user': None, 'page': 'login',
    'messages': [], 'history': [], 'holdings': []
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── USERS ─────────────────────────────────────────────────────────────────────
USERS = {
    "kumar@sebi.com": {"password": "password123", "name": "Kumar Sharma", "role": "CLIENT"},
    "admin@sebi.com": {"password": "admin123", "name": "Admin User", "role": "ADMIN"},
    "viewer@sebi.com": {"password": "viewer123", "name": "Viewer User", "role": "VIEWER"},
}

# ─── GROQ AI ───────────────────────────────────────────────────────────────────
def ask_groq(user_message, history=[]):
    try:
        pass
        messages = [{"role": "system", "content": SEBI_PROMPT}]
        for h in history[-6:]:
            messages.append(h)
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Groq Error: {str(e)}\n\nKripya API key check karein."

def fmt(v): return f"₹{v:,.0f}"

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:1.5rem;border-bottom:1px solid #1a2332;">
            <div class="logo-text">📈 InvestAI</div>
            <div class="logo-sub">SEBI REGISTERED ADVISER</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.user:
            u = st.session_state.user
            st.markdown(f"""
            <div style="padding:1rem 1.5rem;border-bottom:1px solid #1a2332;">
                <div style="width:38px;height:38px;background:linear-gradient(135deg,#00d4aa,#00a88a);
                    border-radius:50%;display:flex;align-items:center;justify-content:center;
                    font-weight:700;color:#080c10;font-size:1rem;margin-bottom:0.5rem;">
                    {u['name'][0].upper()}
                </div>
                <div style="font-size:15px;color:#e2e8f0;font-weight:500;">{u['name']}</div>
                <div style="font-size:13px;color:#4a6741;margin-top:0.1rem;">{u['email']}</div>
                <div style="display:inline-block;margin-top:0.4rem;padding:0.15rem 0.6rem;
                    background:#0a1a28;border:1px solid #1e2d3d;border-radius:3px;
                    font-size:12px;color:#00d4aa;letter-spacing:0.1em;">
                    {u['role']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            pages = [("💬", "Chat", "chat"), ("📊", "Portfolio", "portfolio"), ("🧮", "SIP Calculator", "sip")]
            for icon, label, key in pages:
                if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
                    st.session_state.page = key
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Logout", use_container_width=True):
                for k in ['logged_in','user','page','messages','history','holdings']:
                    st.session_state[k] = False if k=='logged_in' else (None if k=='user' else ('login' if k=='page' else []))
                st.rerun()

        st.markdown("""
        <div style="position:fixed;bottom:1rem;left:0;width:220px;padding:0 1.5rem;">
            <div style="font-size:12px;color:#1e2d3d;line-height:1.6;">
                SEBI Reg. No: INA000000000<br>© 2026 InvestAI Advisory
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── LOGIN PAGE ─────────────────────────────────────────────────────────────────
def page_login():
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("""
        <div style="background:#0d1117;border:1px solid #1e2d3d;border-radius:16px;
            padding:2.5rem;margin-top:3rem;box-shadow:0 0 60px rgba(0,212,170,0.06);">
            <div class="login-logo">📈 InvestAI</div>
            <div style="text-align:center;font-size:12px;color:#4a6741;
                letter-spacing:0.18em;margin-bottom:2rem;">SEBI REGISTERED INVESTMENT ADVISER</div>
        """, unsafe_allow_html=True)

        # Quick fill buttons BEFORE inputs
        st.markdown('<div style="font-size:14px;color:#4a6741;margin-bottom:0.4rem;">Quick Fill:</div>', unsafe_allow_html=True)
        qa, qb, qc = st.columns(3)
        with qa:
            if st.button("👤 Client", use_container_width=True, key="qf_client"):
                st.session_state['_qf_email'] = "kumar@sebi.com"
                st.session_state['_qf_pass'] = "password123"
        with qb:
            if st.button("🔑 Admin", use_container_width=True, key="qf_admin"):
                st.session_state['_qf_email'] = "admin@sebi.com"
                st.session_state['_qf_pass'] = "admin123"
        with qc:
            if st.button("👁️ Viewer", use_container_width=True, key="qf_viewer"):
                st.session_state['_qf_email'] = "viewer@sebi.com"
                st.session_state['_qf_pass'] = "viewer123"

        email = st.text_input("Email", value=st.session_state.get('_qf_email',''), placeholder="kumar@sebi.com")
        password = st.text_input("Password", value=st.session_state.get('_qf_pass',''), type="password", placeholder="••••••••")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔐  Login", use_container_width=True):
            if email in USERS and USERS[email]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user = {"name": USERS[email]['name'], "email": email, "role": USERS[email]['role']}
                st.session_state.page = 'chat'
                st.session_state['_qf_email'] = ''
                st.session_state['_qf_pass'] = ''
                st.rerun()
            else:
                st.error("❌ Email ya password galat hai!")

        st.markdown("""
        <div style="margin-top:1.2rem;padding:0.8rem;background:#0a0e14;
            border:1px solid #1e2d3d;border-radius:6px;font-size:13px;color:#4a6741;line-height:1.6;">
            ⚠️ SEBI compliant platform. Educational purpose only.
        </div>
        </div>
        """, unsafe_allow_html=True)

# ─── CHAT PAGE ──────────────────────────────────────────────────────────────────
def page_chat():
    st.markdown('<div class="page-title">AI Chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">SEBI COMPLIANT INVESTMENT ADVISORY · POWERED BY GROQ AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="disclaimer">⚠️ Investments are subject to market risks. Please read all scheme related documents carefully before investing. Past performance is not indicative of future returns.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2.2, 1])

    with col2:
        st.markdown('<div class="card"><div class="card-title">💡 Quick Questions</div>', unsafe_allow_html=True)
        quick_qs = [
            "SIP ke baare mein batao",
            "Tax saving investment kya hain?",
            "Portfolio diversification explain karo",
            "ELSS vs PPF comparison",
            "Market crash mein kya karein?",
            "Mutual fund kaise choose karein?",
        ]
        for q in quick_qs:
            if st.button(f"→ {q}", key=f"qq_{q}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                with st.spinner("⏳ AI soch raha hai..."):
                    reply = ask_groq(q, st.session_state.history)
                st.session_state.messages.append({"role": "ai", "content": reply})
                st.session_state.history.extend([
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": reply}
                ])
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">📁 Portfolio Context</div>', unsafe_allow_html=True)
        with st.expander(f"Holdings ({len(st.session_state.holdings)})", expanded=False):
            h_name = st.text_input("Name", placeholder="RELIANCE", key="ch_name")
            c1h, c2h = st.columns(2)
            with c1h:
                h_qty = st.number_input("Qty", min_value=0, key="ch_qty")
                h_buy = st.number_input("Buy ₹", min_value=0.0, key="ch_buy")
            with c2h:
                h_curr = st.number_input("Current ₹", min_value=0.0, key="ch_curr")
                h_type = st.selectbox("Type", ["Equity","Debt","Gold","Others"], key="ch_type")
            if st.button("➕ Add", use_container_width=True, key="ch_add"):
                if h_name:
                    st.session_state.holdings.append({"name":h_name,"qty":h_qty,"buy_price":h_buy,"current_price":h_curr,"asset_type":h_type})
                    st.rerun()
        if st.session_state.holdings:
            for h in st.session_state.holdings:
                pnl = (h['current_price']-h['buy_price'])*h['qty']
                c = "#22c55e" if pnl>=0 else "#ef4444"
                a = "▲" if pnl>=0 else "▼"
                st.markdown(f'<div style="background:#111820;border:1px solid #1e2d3d;border-radius:6px;padding:0.45rem 0.7rem;margin:0.25rem 0;font-size:14px;display:flex;justify-content:space-between;"><span>{h["name"]}</span><span style="color:{c};">{a} {fmt(pnl)}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        if not st.session_state.messages:
            name = st.session_state.user['name']
            st.session_state.messages.append({"role":"ai","content":f"Namaste {name}! 🙏\n\nMain aapka SEBI-registered AI Investment Adviser hoon — **Groq AI** se powered!\n\nMain aapko investment planning, portfolio analysis, aur financial goals mein madad kar sakta hoon.\n\n**Aaj kya jaanna chahte ho?**"})

        chat_html = '<div style="max-height:430px;overflow-y:auto;padding:0.5rem;margin-bottom:1rem;">'
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                chat_html += f'<div class="chat-label-user">YOU</div><div class="chat-user">{msg["content"]}</div>'
            else:
                content = msg['content'].replace('\n','<br>').replace('**','<strong>').replace('**','</strong>')
                chat_html += f'<div class="chat-label-ai">🤖 INVESTAI</div><div class="chat-ai">{content}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        ic1, ic2 = st.columns([5,1])
        with ic1:
            user_input = st.text_input("", placeholder="Investment ke baare mein poochho...", key="chat_inp", label_visibility="collapsed")
        with ic2:
            send = st.button("Send ➤", use_container_width=True)

        if send and user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            with st.spinner("⏳ AI soch raha hai..."):
                reply = ask_groq(user_input, st.session_state.history)
            st.session_state.messages.append({"role":"ai","content":reply})
            st.session_state.history.extend([{"role":"user","content":user_input},{"role":"assistant","content":reply}])
            st.rerun()

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.history = []
            st.rerun()

# ─── PORTFOLIO PAGE ─────────────────────────────────────────────────────────────
def page_portfolio():
    st.markdown('<div class="page-title">Portfolio Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">AI-POWERED PORTFOLIO ANALYSIS · GROQ AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="disclaimer">⚠️ Investments are subject to market risks. Past performance is not indicative of future returns.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1.8])

    with col2:
        st.markdown('<div class="card"><div class="card-title">➕ Add Holding</div>', unsafe_allow_html=True)
        p_name = st.text_input("Stock / Fund Name", placeholder="RELIANCE", key="p_name")
        c1p, c2p = st.columns(2)
        with c1p:
            p_qty = st.number_input("Quantity", min_value=0, step=1, key="p_qty")
            p_buy = st.number_input("Buy Price ₹", min_value=0.0, key="p_buy")
        with c2p:
            p_curr = st.number_input("Current ₹", min_value=0.0, key="p_curr")
            p_type = st.selectbox("Asset Type", ["Equity","Debt","Gold","Others"], key="p_type")
        if st.button("➕ Add to Portfolio", use_container_width=True):
            if p_name and p_qty > 0:
                st.session_state.holdings.append({"name":p_name,"qty":p_qty,"buy_price":p_buy,"current_price":p_curr,"asset_type":p_type})
                st.success(f"✅ {p_name} added!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("📋 Sample Portfolio Load Karo", use_container_width=True):
            st.session_state.holdings = [
                {"name":"RELIANCE","qty":10,"buy_price":2400,"current_price":2850,"asset_type":"Equity"},
                {"name":"TCS","qty":5,"buy_price":3500,"current_price":3920,"asset_type":"Equity"},
                {"name":"HDFC NIFTY 50","qty":100,"buy_price":180,"current_price":220,"asset_type":"Equity"},
                {"name":"SBI LIQUID FUND","qty":500,"buy_price":3200,"current_price":3350,"asset_type":"Debt"},
                {"name":"GOLD ETF","qty":20,"buy_price":5500,"current_price":6200,"asset_type":"Gold"},
            ]
            st.rerun()

    with col1:
        if not st.session_state.holdings:
            st.markdown('<div style="text-align:center;padding:3rem;background:#0d1117;border:1px dashed #1e2d3d;border-radius:10px;"><div style="font-size:3rem;margin-bottom:1rem;">📊</div><div style="color:#4a6741;font-size:15px;">Right side se holdings add karo</div></div>', unsafe_allow_html=True)
        else:
            total_inv = sum(h['qty']*h['buy_price'] for h in st.session_state.holdings)
            total_curr = sum(h['qty']*h['current_price'] for h in st.session_state.holdings)
            pnl = total_curr - total_inv
            pnl_pct = (pnl/total_inv*100) if total_inv>0 else 0

            m1,m2,m3,m4 = st.columns(4)
            with m1: st.metric("💰 Invested", fmt(total_inv))
            with m2: st.metric("📈 Current", fmt(total_curr))
            with m3: st.metric("💹 P&L", fmt(pnl), f"{pnl_pct:.1f}%")
            with m4: st.metric("📌 Holdings", len(st.session_state.holdings))

            # Asset allocation
            eq = sum(h['qty']*h['current_price'] for h in st.session_state.holdings if h['asset_type']=='Equity')
            dt = sum(h['qty']*h['current_price'] for h in st.session_state.holdings if h['asset_type']=='Debt')
            gd = sum(h['qty']*h['current_price'] for h in st.session_state.holdings if h['asset_type']=='Gold')
            ot = total_curr - eq - dt - gd

            st.markdown('<div class="card"><div class="card-title">Asset Allocation</div>', unsafe_allow_html=True)
            for name, val, color in [("Equity",eq,"#00d4aa"),("Debt",dt,"#3b82f6"),("Gold",gd,"#f59e0b"),("Others",ot,"#8b5cf6")]:
                pct = (val/total_curr*100) if total_curr>0 else 0
                if pct > 0:
                    st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:0.2rem;"><span style="color:#94a3b8;">{name}</span><span style="color:{color};">{pct:.1f}%</span></div><div class="alloc-bg"><div class="alloc-fill" style="width:{pct}%;background:{color};"></div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Holdings table
            st.markdown('<div class="card"><div class="card-title">Holdings</div>', unsafe_allow_html=True)
            tbl = "<table><tr><th>Name</th><th>Type</th><th>Qty</th><th>Buy ₹</th><th>Current ₹</th><th>P&L</th></tr>"
            for h in st.session_state.holdings:
                inv = h['qty']*h['buy_price']; val = h['qty']*h['current_price']
                pl = val-inv; pp = (pl/inv*100) if inv>0 else 0
                c = "#22c55e" if pl>=0 else "#ef4444"; a = "▲" if pl>=0 else "▼"
                tbl += f"<tr><td style='color:#e2e8f0;font-weight:500;'>{h['name']}</td><td style='color:#64748b;'>{h['asset_type']}</td><td>{h['qty']}</td><td>{fmt(h['buy_price'])}</td><td>{fmt(h['current_price'])}</td><td style='color:{c};'>{a} {fmt(pl)} ({pp:.1f}%)</td></tr>"
            tbl += "</table>"
            st.markdown(tbl, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            b1,b2 = st.columns(2)
            with b1:
                if st.button("🤖 AI Analysis Karo", use_container_width=True):
                    portfolio_text = "\n".join([f"{h['name']}: {h['qty']} shares, buy ₹{h['buy_price']}, current ₹{h['current_price']}, type: {h['asset_type']}" for h in st.session_state.holdings])
                    prompt = f"Analyze this portfolio and give recommendations:\n{portfolio_text}\n\nTotal invested: {fmt(total_inv)}, Current value: {fmt(total_curr)}, P&L: {fmt(pnl)} ({pnl_pct:.1f}%)"
                    with st.spinner("🤖 AI portfolio analyze kar raha hai..."):
                        analysis = ask_groq(prompt, [])
                    st.markdown(f'<div class="card" style="border-color:#1a3a2a;background:#0a160a;"><div class="card-title" style="color:#4ade80;">🤖 AI Analysis</div><div style="font-size:15px;line-height:1.75;color:#94a3b8;">{analysis.replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)
            with b2:
                if st.button("🗑️ Clear Portfolio", use_container_width=True):
                    st.session_state.holdings = []
                    st.rerun()

# ─── SIP PAGE ───────────────────────────────────────────────────────────────────
def page_sip():
    st.markdown('<div class="page-title">SIP Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">SYSTEMATIC INVESTMENT PLAN CALCULATOR</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown('<div class="card"><div class="card-title">⚙️ SIP Parameters</div>', unsafe_allow_html=True)
        monthly = st.number_input("Monthly Investment (₹)", min_value=500, max_value=1000000, value=10000, step=500)
        rate = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.5)
        years = st.slider("Investment Duration (Years)", min_value=1, max_value=40, value=20)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🧮 Calculate Returns", use_container_width=True):
            r = rate/100/12; n = years*12
            maturity = monthly*((1+r)**n-1)/r*(1+r)
            invested = monthly*n; gains = maturity-invested
            st.markdown(f"""
            <div class="sip-result">
                <div style="font-size:13px;color:#4a6741;letter-spacing:0.15em;margin-bottom:0.5rem;">MATURITY VALUE</div>
                <div class="sip-amount">{fmt(maturity)}</div>
                <div style="margin-top:1.5rem;display:flex;gap:2rem;justify-content:center;">
                    <div><div style="font-size:12px;color:#4a6741;">INVESTED</div><div style="font-size:1.2rem;color:#e2e8f0;font-weight:600;">{fmt(invested)}</div></div>
                    <div><div style="font-size:12px;color:#4a6741;">GAINS</div><div style="font-size:1.2rem;color:#22c55e;font-weight:600;">{fmt(gains)}</div></div>
                    <div><div style="font-size:12px;color:#4a6741;">RETURNS</div><div style="font-size:1.2rem;color:#00d4aa;font-weight:600;">{((gains/invested)*100):.0f}%</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">📊 Rate Comparison</div>', unsafe_allow_html=True)
        invested_total = monthly*years*12
        tbl = f"<table><tr><th>Rate</th><th>{years}yr Maturity</th><th>Gains</th></tr>"
        for rv in [6,8,10,12,15,18]:
            r=rv/100/12; n=years*12
            mat=monthly*((1+r)**n-1)/r*(1+r); g=mat-invested_total
            c="#00d4aa" if rv==12 else "#e2e8f0"
            tbl+=f"<tr><td style='color:{c};font-weight:{'600' if rv==12 else '400'}'>{rv}%</td><td style='color:{c};'>{fmt(mat)}</td><td style='color:#22c55e;'>{fmt(g)}</td></tr>"
        tbl+="</table>"
        st.markdown(tbl, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">💡 SIP Tips</div>', unsafe_allow_html=True)
        tips = ["📅 Monthly SIP — discipline zaroori hai","📈 Long term mein compounding ka jaadu","🔄 Har saal SIP 10-15% step-up karo","🎯 Alag goals ke liye alag SIP","⚠️ Market crash mein SIP band mat karo"]
        for t in tips:
            st.markdown(f'<div style="padding:0.45rem 0;font-size:14px;color:#94a3b8;border-bottom:1px solid #111820;">{t}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── MAIN ──────────────────────────────────────────────────────────────────────
render_sidebar()

if not st.session_state.logged_in:
    page_login()
else:
    if st.session_state.page == 'chat': page_chat()
    elif st.session_state.page == 'portfolio': page_portfolio()
    elif st.session_state.page == 'sip': page_sip()
    else: page_chat()
