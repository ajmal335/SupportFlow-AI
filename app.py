
import os
import requests
import streamlit as st

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SupportFlow AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv(
    "SUPPORTFLOW_API_URL",
    "http://127.0.0.1:8000"
)

# =====================================================
# 2. SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None

if "admin_token" not in st.session_state:
    st.session_state.admin_token = ""

# =====================================================
# 3. ADMIN LOGOUT
# =====================================================

def logout_admin():
    st.session_state.admin_token = ""
    st.session_state.admin_token_input = ""

# =====================================================
# 4. PREMIUM DARK SAAS STYLING
# =====================================================

st.markdown("""
<style>

/* =========================================
   GLOBAL APPLICATION
========================================= */

.stApp {
    background-color: #0B1120;
    color: #F1F5F9;
}

/* Main content width */

section[data-testid="stMain"] .block-container {
    max-width: 1500px;
    width: 100%;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* =========================================
   SIDEBAR
========================================= */

section[data-testid="stSidebar"] {
    background-color: #111B2E;
    border-right: 1px solid #26354D;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* Sidebar headings */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F1F5F9;
}

/* Sidebar text */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] label {
    color: #CBD5E1;
}

/* Sidebar buttons */

section[data-testid="stSidebar"] .stButton > button {
    background-color: #1E293B;
    color: #F1F5F9;
    border: 1px solid #334155;
    border-radius: 9px;
    min-height: 42px;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #2563EB;
    border-color: #3B82F6;
    color: white;
}

/* Sidebar input */

section[data-testid="stSidebar"] .stTextInput input {
    background-color: #0B1120;
    color: #F1F5F9;
    border: 1px solid #334155;
    border-radius: 8px;
}

/* Sidebar dividers */

section[data-testid="stSidebar"] hr {
    border-color: #26354D;
}

/* Brand panel */

.sidebar-brand {
    padding: 18px 14px;
    background: linear-gradient(135deg, #172B49, #111B2E);
    border: 1px solid #2B4263;
    border-radius: 14px;
    margin-bottom: 18px;
}

.sidebar-brand-title {
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 750;
    letter-spacing: -0.5px;
}

.sidebar-brand-subtitle {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 5px;
}

/* Sidebar section labels */

.sidebar-section-label {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin: 12px 0 10px 0;
}

/* Capability cards */

.sidebar-capability {
    color: #CBD5E1;
    background: #172438;
    border: 1px solid #26354D;
    border-radius: 8px;
    padding: 9px 10px;
    margin-bottom: 7px;
    font-size: 13px;
}

/* Technology badges */

.sidebar-tech {
    display: inline-block;
    color: #BFDBFE;
    background: #172D4B;
    border: 1px solid #294B75;
    border-radius: 6px;
    padding: 5px 8px;
    margin: 3px 3px 3px 0;
    font-size: 11px;
    font-weight: 600;
}

/* =========================================
   MAIN HEADER
========================================= */

.main-title {
    color: #F8FAFC;
    font-size: 38px;
    font-weight: 750;
    letter-spacing: -1.2px;
    margin-bottom: 5px;
}

.main-subtitle {
    color: #94A3B8;
    font-size: 16px;
    margin-top: 0;
    line-height: 1.6;
}

/* =========================================
   CHAT MESSAGES
========================================= */

[data-testid="stChatMessage"] {
    background-color: #111B2E;
    border: 1px solid #26354D;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
    width: 100%;
}

[data-testid="stChatMessage"] p {
    color: #E2E8F0;
    font-size: 15px;
    line-height: 1.7;
}

/* =========================================
   CHAT INPUT
========================================= */

[data-testid="stChatInput"] {
    max-width: 100%;
}

[data-testid="stChatInput"] textarea {
    background-color: #111B2E;
    color: #F1F5F9;
    border: 1px solid #334155;
    border-radius: 12px;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #3B82F6;
}

/* =========================================
   BUTTONS
========================================= */

.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
}

/* =========================================
   ALERTS AND DIVIDERS
========================================= */

[data-testid="stAlert"] {
    border-radius: 10px;
}

.stApp hr {
    border-color: #26354D;
}

/* =========================================
   RESPONSIVE DESIGN
========================================= */

@media (max-width: 768px) {

    section[data-testid="stMain"] .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.5rem;
    }

    .main-title {
        font-size: 29px;
    }

    [data-testid="stChatMessage"] {
        padding: 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 5. PREMIUM SIDEBAR
# =====================================================

with st.sidebar:

    # Brand

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">
            ✦ SupportFlow AI
        </div>
        <div class="sidebar-brand-subtitle">
            Intelligent Customer Support Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Admin Access

    st.markdown(
        '<div class="sidebar-section-label">Admin Access</div>',
        unsafe_allow_html=True
    )

    st.text_input(
        "Admin Token",
        type="password",
        key="admin_token_input",
        placeholder="Enter your admin token"
    )

    st.session_state.admin_token = (
        st.session_state.admin_token_input
    )

    if st.session_state.admin_token:
        st.success("Admin token entered")
    else:
        st.warning(
            "Admin access required for refund decisions."
        )

    st.button(
        "Logout Admin",
        use_container_width=True,
        on_click=logout_admin
    )

    st.divider()

    # Platform Capabilities

    st.markdown(
        '<div class="sidebar-section-label">Platform Capabilities</div>',
        unsafe_allow_html=True
    )

    capabilities = [
        "✦ AI Customer Support",
        "↗ Order Status Tracking",
        "▤ Return & Refund Policies",
        "◈ Refund Eligibility Checking",
        "✓ Human-in-the-Loop Approval"
    ]

    for capability in capabilities:
        st.markdown(
            f'<div class="sidebar-capability">{capability}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # Technology Stack

    st.markdown(
        '<div class="sidebar-section-label">Powered By</div>',
        unsafe_allow_html=True
    )

    technologies = [
        "LangChain",
        "LangGraph",
        "Gemini",
        "FastAPI",
        "Streamlit",
        "SQLite"
    ]

    tech_html = "".join(
        f'<span class="sidebar-tech">{technology}</span>'
        for technology in technologies
    )

    st.markdown(
        tech_html,
        unsafe_allow_html=True
    )

    st.divider()

    # Session Controls

    st.markdown(
        '<div class="sidebar-section-label">Session Controls</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Clear Chat History",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.pending_approval = None
        st.rerun()

    st.caption("SupportFlow AI · Portfolio Demo")

# =====================================================
# 6. MAIN DASHBOARD HEADER
# =====================================================

st.markdown(
    """
    <h1 class="main-title">
        🤖 SupportFlow AI
    </h1>
    <p class="main-subtitle">
        Intelligent AI-powered customer support
        with automated workflows and human oversight.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# 7. DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# 8. CUSTOMER CHAT
# =====================================================

user_message = st.chat_input(
    "Ask about orders, refunds, returns or customer support..."
)

if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):

        with st.spinner(
            "SupportFlow AI is processing your request..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": user_message},
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                if data["status"] == "pending_approval":

                    review = data["review"]

                    assistant_message = (
                        f"Your refund request for order "
                        f"**{review['order_id']}** meets the "
                        f"eligibility requirements.\n\n"
                        f"Refund amount: **PKR "
                        f"{review['eligibility']['refund_amount']:,}**\n\n"
                        f"Your request is waiting for human approval."
                    )

                    st.session_state.pending_approval = {
                        "thread_id": data["thread_id"],
                        "order_id": review["order_id"],
                        "amount": review["eligibility"]["refund_amount"]
                    }

                else:

                    assistant_message = data.get(
                        "response",
                        "No response received."
                    )

                st.markdown(assistant_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })

            except requests.RequestException as error:

                assistant_message = (
                    "I couldn't connect to the SupportFlow API. "
                    "Please check whether the backend server is running."
                )

                st.error(f"API error: {error}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })

# =====================================================
# 9. HUMAN REFUND REVIEW
# =====================================================

pending = st.session_state.pending_approval

if pending:

    st.divider()

    st.subheader("🛡️ Human Refund Review")

    st.info(
        f"Order: {pending['order_id']}\n\n"
        f"Refund amount: PKR {pending['amount']:,}\n\n"
        "This refund requires human approval."
    )

    if not st.session_state.admin_token:

        st.warning(
            "Only an authenticated admin can approve or reject "
            "this refund. Enter your admin token in the sidebar."
        )

    else:

        col1, col2 = st.columns(2)

        headers = {
            "X-Admin-Token": st.session_state.admin_token
        }

        # Approve Refund

        with col1:

            if st.button(
                "Approve Refund",
                use_container_width=True
            ):

                try:

                    with st.spinner("Processing approval..."):

                        response = requests.post(
                            f"{API_URL}/approve/{pending['thread_id']}",
                            json={"decision": "approve"},
                            headers=headers,
                            timeout=120
                        )

                        response.raise_for_status()

                        data = response.json()

                    result = data["response"]

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"✅ {result}"
                    })

                    st.session_state.pending_approval = None

                    st.rerun()

                except requests.RequestException as error:

                    st.error(f"Approval failed: {error}")

        # Reject Refund

        with col2:

            if st.button(
                "Reject Refund",
                use_container_width=True
            ):

                try:

                    with st.spinner("Processing rejection..."):

                        response = requests.post(
                            f"{API_URL}/approve/{pending['thread_id']}",
                            json={"decision": "reject"},
                            headers=headers,
                            timeout=120
                        )

                        response.raise_for_status()

                        data = response.json()

                    result = data["response"]

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"❌ {result}"
                    })

                    st.session_state.pending_approval = None

                    st.rerun()

                except requests.RequestException as error:

                    st.error(f"Rejection failed: {error}")
