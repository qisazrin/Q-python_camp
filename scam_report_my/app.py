import streamlit as st
import requests
import pandas as pd

# ───────────── CONFIG ─────────────
API_URL = "https://scam-watch-sy14.onrender.com"

SCAM_TYPES = [
    "Phone Scam", "Email Phishing", "Online Shopping Fraud",
    "Investment Scam", "Romance Scam", "Job Scam",
    "Bank Fraud", "Social Media Scam", "Crypto Scam", "Other"
]

STATUS_LIST = ["pending", "verified", "rejected"]

st.set_page_config(
    page_title="ScamWatch",
    page_icon="🛡️",
    layout="wide"
)
# ───────────── GLOBAL BACKGROUND & THEME ─────────────
st.markdown("""<style>
/* ── Animated gradient background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #040408, #24243e);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Transparent sidebar with frosted glass ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* ── Main content cards feel ── */
[data-testid="stMain"] {
    background: rgba(255, 255, 255, 0.03);
}

/* ── Global text to white ── */
html, body, [class*="css"] {
    color: #f0f0f0 !important;
}

/* ── Inputs styling ── */
input, textarea, select {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, #200589, #c1121f) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    transition: transform 0.2s ease;
}
.stButton > button:hover {
    transform: scale(1.03);
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 12px;
    backdrop-filter: blur(6px);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    color: #aaa !important;
}
.stTabs [aria-selected="true"] {
    color: #e63946 !important;
    border-bottom: 2px solid #e63946 !important;
}

</style>""", unsafe_allow_html=True)


# ───────────── API HELPERS ─────────────
def api_get(path, params=None):
    try:
        r = requests.get(f"{API_URL}{path}", params=params)
        return r.json() if r.status_code == 200 else None
    except Exception:
        st.error("API connection failed")
        return None


def api_post(path, json=None, files=None, data=None):
    try:
        r = requests.post(f"{API_URL}{path}", json=json, files=files, data=data)
        if r.status_code not in (200, 201):
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text
            st.error(f"Error {r.status_code}: {detail}")
            return None
        return r.json()
    except Exception as e:
        st.error(str(e))
        return None


def api_put(path, json):
    try:
        r = requests.put(f"{API_URL}{path}", json=json)
        return r.json()
    except Exception:
        st.error("PUT request failed")
        return None


def api_delete(path):
    try:
        r = requests.delete(f"{API_URL}{path}")
        return r.json()
    except Exception:
        st.error("DELETE request failed")
        return None


# ───────────── SESSION STATE INIT ─────────────
for key, default in {
    "logged_in": False,
    "username": None,
    "role": None,
    "auth_mode": "login",    # "login" | "register"
    "page": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ───────────── AUTH PAGE ─────────────
def auth_page():
    st.markdown("""
    <style>
    .auth-title { font-size: 2.4rem; font-weight: 800; color: #white; margin-bottom: 0; }
    .auth-sub   { font-size: 1rem; color: #white; margin-bottom: 1.5rem; }
    .stTabs [data-baseweb="tab"] p { color: #ffffff !important; }
    .role-badge-admin { background:#e63946; color:#fff; padding:2px 10px; border-radius:20px; font-size:.8rem; font-weight:700; }
    .role-badge-user  { background:#457b9d; color:#fff; padding:2px 10px; border-radius:20px; font-size:.8rem; font-weight:700; }
    </style>
    """, unsafe_allow_html=True)

    col_center, _ = st.columns([1.2, 1])
    with col_center:
        st.markdown('<p class="auth-title">🛡️ ScamWatch</p>', unsafe_allow_html=True)
        st.markdown('<p class="auth-sub">Malaysia Scam Reporting Platform</p>', unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

        # ── LOGIN ──
        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    res = api_post("/auth/login", json={"username": username, "password": password})
                    if res:
                        st.session_state.logged_in = True
                        st.session_state.username = res["username"]
                        st.session_state.role = res["role"]
                        # Set default page based on role
                        if res["role"] == "admin":
                            st.session_state.page = "📊 Dashboard"
                        else:
                            st.session_state.page = "📊 My Analytics"
                        st.rerun()

        # ── REGISTER ──
        with tab_register:
            with st.form("register_form"):
                new_username = st.text_input("Choose a Username")
                new_password = st.text_input("Choose a Password (min 6 chars)", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                role_choice = st.selectbox("Account Type", ["User", "Admin"])
                admin_secret = ""
                if role_choice == "Admin":
                    admin_secret = st.text_input("Admin Secret Key", type="password",
                                                 help="Contact the system administrator for the secret key.")
                reg_submitted = st.form_submit_button("Create Account", use_container_width=True)

            if reg_submitted:
                if not new_username or not new_password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    payload = {
                        "username": new_username,
                        "password": new_password,
                        "role": role_choice.lower(),
                        "admin_secret": admin_secret if role_choice == "Admin" else None
                    }
                    res = api_post("/auth/register", json=payload)
                    if res:
                        st.success(f"Account created! You can now log in as **{res['role']}**.")


# ───────────── REPORT ID DROPDOWN HELPER ─────────────
def get_report_id_options(only_mine=False):
    params = {}
    if only_mine and st.session_state.username:
        params["reported_by"] = st.session_state.username
    reports = api_get("/reports", params=params)
    if not reports:
        return [], []
    reports_sorted = sorted(reports, key=lambda x: x["id"])
    labels = [f"ID {r['id']} — {r['title']} ({r['status']})" for r in reports_sorted]
    ids = [r["id"] for r in reports_sorted]
    return labels, ids


# ───────────── EVIDENCE RENDERER ─────────────
def render_evidence(report_id):
    evidence = api_get(f"/reports/{report_id}/evidence")
    if not evidence:
        return
    st.write("**Evidence:**")
    for ev in evidence:
        filename = ev["filename"]
        file_url = f"{API_URL}/uploads/{filename}"
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
            st.image(file_url, caption=filename, width=250)
        elif ext == "pdf":
            st.markdown(f"📄 [View PDF — {filename}]({file_url})", unsafe_allow_html=True)
        elif ext in ["mp4", "mov", "avi", "webm"]:
            st.video(file_url)
        elif ext in ["mp3", "wav", "ogg"]:
            st.audio(file_url)
        else:
            st.markdown(f"📎 [Download {filename}]({file_url})", unsafe_allow_html=True)


# ───────────── SIDEBAR ─────────────
def render_sidebar():
    with st.sidebar:
        st.title("🛡️ ScamWatch")

        role = st.session_state.role
        username = st.session_state.username

        # Role badge
        badge_color = "#e63946" if role == "admin" else "#457b9d"
        st.markdown(
            f'<div style="margin-bottom:1rem;">'
            f'👤 <b>{username}</b>&nbsp;&nbsp;'
            f'<span style="background:{badge_color};color:#fff;padding:2px 9px;'
            f'border-radius:20px;font-size:.75rem;font-weight:700;">'
            f'{role.upper()}</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Admin sees all pages; user sees limited set
        if role == "admin":
            pages = [
                "📊 Dashboard",
                "📋 All Reports",
                "➕ Submit Report",
                "🔍 Search",
                "✏️ Update",
                "🗑️ Delete",
                "👥 Users",
            ]
        else:
            pages = [
                "📊 My Analytics",
                "➕ Submit Report",
                "✏️ Update My Reports",
                "🗑️ Delete My Reports",
            ]

        for p in pages:
            if st.button(p, use_container_width=True):
                st.session_state.page = p
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["logged_in", "username", "role", "page"]:
                st.session_state[key] = None if key != "logged_in" else False
            st.session_state.page = None
            st.rerun()


# ─────────────────────────────────────────────────────
#  ADMIN PAGES
# ─────────────────────────────────────────────────────

def dashboard():
    st.title("📊 Dashboard")

    stats = api_get("/stats")
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", stats["total_reports"])
        col2.metric("Pending", stats["pending"])
        col3.metric("Verified", stats["verified"])
        col4.metric("Rejected", stats["rejected"])

        st.subheader("Reports by Scam Type")
        if stats["by_scam_type"]:
            df = pd.DataFrame(list(stats["by_scam_type"].items()), columns=["Type", "Count"])
            st.bar_chart(df.set_index("Type"))

    st.markdown("## 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Submit Report", use_container_width=True):
            st.session_state.page = "➕ Submit Report"; st.rerun()
    with col2:
        if st.button("📋 View Reports", use_container_width=True):
            st.session_state.page = "📋 All Reports"; st.rerun()
    with col3:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.page = "🔍 Search"; st.rerun()

    col4, col5 = st.columns(2)
    with col4:
        if st.button("✏️ Update", use_container_width=True):
            st.session_state.page = "✏️ Update"; st.rerun()
    with col5:
        if st.button("🗑️ Delete", use_container_width=True):
            st.session_state.page = "🗑️ Delete"; st.rerun()

    st.markdown("---")
    st.subheader("Recent Reports")
    reports = api_get("/reports")
    if reports:
        for r in reports[:5]:
            st.write(f"**ID {r['id']}** - {r['title']} - {r['scam_type']} ({r['status']})")


def all_reports():
    st.title("📋 All Reports")

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Status", ["All"] + STATUS_LIST)
    with col2:
        scam_filter = st.selectbox("Scam Type", ["All"] + SCAM_TYPES)

    params = {}
    if status_filter != "All":
        params["status_filter"] = status_filter
    if scam_filter != "All":
        params["scam_type"] = scam_filter

    reports = api_get("/reports", params=params)
    if reports:
        for r in reports:
            with st.expander(f"ID {r['id']} - {r['title']} ({r['status']})"):
                st.write("**Type:**", r["scam_type"])
                st.write("**Description:**", r["description"])
                st.write("**Reported By:**", r.get("reported_by", "Anonymous"))
                st.write("**Location:**", r.get("location"))
                st.write("**Amount Lost:**", r.get("amount_lost", 0))
                st.write("**Contact:**", r.get("scammer_contact"))
                render_evidence(r["id"])
    else:
        st.info("No reports found")


def admin_search():
    st.title("🔍 Search Report")
    labels, ids = get_report_id_options(only_mine=False)
    if not labels:
        st.info("No reports available.")
        return
    selected_label = st.selectbox("Select Report ID", labels)
    report_id = ids[labels.index(selected_label)]
    if st.button("Search"):
        r = api_get(f"/reports/{report_id}")
        if r:
            st.write("**ID:**", r["id"])
            st.write("**Title:**", r["title"])
            st.write("**Type:**", r["scam_type"])
            st.write("**Description:**", r["description"])
            st.write("**Status:**", r["status"])
            st.write("**Reported By:**", r.get("reported_by", "Anonymous"))
            st.write("**Location:**", r.get("location"))
            st.write("**Amount Lost:**", r.get("amount_lost", 0))
            st.write("**Contact:**", r.get("scammer_contact"))
            render_evidence(report_id)
        else:
            st.error("Report not found")


def admin_update():
    st.title("✏️ Update Report")
    labels, ids = get_report_id_options(only_mine=False)
    if not labels:
        st.info("No reports available.")
        return
    selected_label = st.selectbox("Select Report ID", labels)
    report_id = ids[labels.index(selected_label)]
    r = api_get(f"/reports/{report_id}")
    if r:
        st.markdown("#### Current Evidence")
        render_evidence(report_id)
        with st.form("update_form"):
            title = st.text_input("Title", value=r["title"])
            description = st.text_area("Description", value=r["description"])
            scammer_contact = st.text_input("Scammer Contact", value=r.get("scammer_contact", "") or "")
            amount_lost = st.number_input("Amount Lost", min_value=0.0, value=float(r.get("amount_lost") or 0))
            status = st.selectbox(
                "Status", STATUS_LIST,
                index=STATUS_LIST.index(r["status"]) if r["status"] in STATUS_LIST else 0
            )
            if st.form_submit_button("Update"):
                payload = {
                    "title": title, "description": description,
                    "scammer_contact": scammer_contact,
                    "amount_lost": amount_lost, "status": status
                }
                result = api_put(f"/reports/{report_id}", payload)
                if result:
                    st.success("Updated successfully!")
    else:
        st.warning("Could not load report.")

def admin_users():
    st.title("👥 Registered Users")
    users = api_get("/users")
    if not users:
        st.info("No users registered yet.")
        return

    total = len(users)
    admins = sum(1 for u in users if u.get("role") == "admin")
    regular = total - admins

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", total)
    col2.metric("Admins", admins)
    col3.metric("Regular Users", regular)

    st.markdown("---")
    for u in users:
        badge = "🔴 ADMIN" if u.get("role") == "admin" else "🔵 USER"
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.07);padding:10px 16px;'
            f'border-radius:10px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.1);">'
            f'👤 <b>{u["username"]}</b> &nbsp; {badge} &nbsp;&nbsp; '
            f'<span style="color:#aaa;font-size:0.85rem;">Joined: {u.get("created_at","N/A")}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

def admin_delete():
    st.title("🗑️ Delete Report")
    labels, ids = get_report_id_options(only_mine=False)
    if not labels:
        st.info("No reports available.")
        return
    selected_label = st.selectbox("Select Report ID to Delete", labels)
    report_id = ids[labels.index(selected_label)]
    r = api_get(f"/reports/{report_id}")
    if r:
        with st.expander("📄 Preview Report", expanded=True):
            st.write("**Title:**", r["title"])
            st.write("**Type:**", r["scam_type"])
            st.write("**Status:**", r["status"])
            st.write("**Description:**", r["description"])
            st.write("**Amount Lost:**", r.get("amount_lost", 0))
    st.warning(f"⚠️ You are about to delete **ID {report_id}**. This action cannot be undone.")
    if st.button("🗑️ Confirm Delete", type="primary"):
        res = api_delete(f"/reports/{report_id}")
        if res:
            st.success(f"Report ID {report_id} deleted successfully!")
            st.rerun()
        else:
            st.error("Failed to delete.")


# ─────────────────────────────────────────────────────
#  SHARED: SUBMIT REPORT  (both roles)
# ─────────────────────────────────────────────────────

def submit_report():
    st.title("➕ Submit Report")
    with st.form("report_form"):
        title = st.text_input("Title")
        scam_type = st.selectbox("Scam Type", SCAM_TYPES)
        description = st.text_area("Description")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location")
        with col2:
            scammer_contact = st.text_input("Scammer Contact")
            amount_lost = st.number_input("Amount Lost", min_value=0.0)
        files = st.file_uploader("Upload Evidence", accept_multiple_files=True)
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not title or not description:
            st.error("Title and Description are required!")
            return
        payload = {
            "title": title,
            "scam_type": scam_type,
            "description": description,
            "scammer_contact": scammer_contact,
            "amount_lost": amount_lost,
            "reported_by": st.session_state.username,
            "location": location
        }
        result = api_post("/reports", json=payload)
        if result:
            report_id = result["id"]
            st.success(f"Report created with ID: {report_id}")
            if files:
                for f in files:
                    api_post(
                        f"/reports/{report_id}/evidence",
                        files={"file": (f.name, f.getvalue(), f.type)}
                    )
                st.success(f"{len(files)} evidence file(s) uploaded.")


# ─────────────────────────────────────────────────────
#  USER-ONLY PAGES  (scoped to their own reports)
# ─────────────────────────────────────────────────────

def user_analytics():
    """Personal analytics dashboard for regular users."""
    st.title("📊 My Analytics")

    username = st.session_state.username
    my_reports = api_get("/reports", params={"reported_by": username})

    if not my_reports:
        st.info("You haven't submitted any reports yet.")
        if st.button("➕ Submit Your First Report"):
            st.session_state.page = "➕ Submit Report"
            st.rerun()
        return

    # ── Summary metrics ──
    total = len(my_reports)
    pending = sum(1 for r in my_reports if r["status"] == "pending")
    verified = sum(1 for r in my_reports if r["status"] == "verified")
    rejected = sum(1 for r in my_reports if r["status"] == "rejected")
    total_lost = sum(r.get("amount_lost") or 0 for r in my_reports)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("My Reports", total)
    col2.metric("Pending", pending)
    col3.metric("Verified", verified)
    col4.metric("Rejected", rejected)
    col5.metric("Total Lost (RM)", f"{total_lost:,.2f}")

    # ── Reports by scam type ──
    st.subheader("My Reports by Scam Type")
    scam_counts = {}
    for r in my_reports:
        st_key = r.get("scam_type", "Other")
        scam_counts[st_key] = scam_counts.get(st_key, 0) + 1
    if scam_counts:
        df = pd.DataFrame(list(scam_counts.items()), columns=["Type", "Count"])
        st.bar_chart(df.set_index("Type"))

    # ── Recent reports ──
    st.subheader("My Recent Reports")
    for r in my_reports[:5]:
        status_icon = {"pending": "🟡", "verified": "✅", "rejected": "❌"}.get(r["status"], "⚪")
        st.write(f"{status_icon} **ID {r['id']}** — {r['title']} ({r['scam_type']})")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("➕ Submit New Report", use_container_width=True):
            st.session_state.page = "➕ Submit Report"; st.rerun()
    with col_b:
        if st.button("✏️ Update My Reports", use_container_width=True):
            st.session_state.page = "✏️ Update My Reports"; st.rerun()


def user_update():
    """Update page scoped to the current user's own reports."""
    st.title("✏️ Update My Reports")
    labels, ids = get_report_id_options(only_mine=True)
    if not labels:
        st.info("You have no reports to update.")
        return
    selected_label = st.selectbox("Select Your Report", labels)
    report_id = ids[labels.index(selected_label)]
    r = api_get(f"/reports/{report_id}")
    if r:
        st.markdown("#### Current Evidence")
        render_evidence(report_id)

        # Users cannot change status — only admins can verify/reject
        with st.form("user_update_form"):
            title = st.text_input("Title", value=r["title"])
            description = st.text_area("Description", value=r["description"])
            scammer_contact = st.text_input("Scammer Contact", value=r.get("scammer_contact", "") or "")
            amount_lost = st.number_input("Amount Lost", min_value=0.0, value=float(r.get("amount_lost") or 0))
            st.info(f"**Status:** {r['status']}  *(Only admins can change report status)*")
            status_colors = {
                "pending":  {"bg": "rgba(255,193,7,0.15)",  "border": "#ffc107", "icon": "🟡"},
                "verified": {"bg": "rgba(40,167,69,0.15)",   "border": "#28a745", "icon": "✅"},
                "rejected": {"bg": "rgba(220,53,69,0.15)",   "border": "#dc3545", "icon": "❌"},}
            s = status_colors.get(r["status"], {"bg": "rgba(255,255,255,0.07)", "border": "#aaa", "icon": "⚪"})
            st.markdown(
                f'<div style="background:{s["bg"]};border:1px solid {s["border"]};'
                f'border-radius:10px;padding:12px 16px;margin-bottom:10px;">'
                f'{s["icon"]} <b>Status:</b> {r["status"].upper()} &nbsp;'
                f'<span style="color:#ccc;font-size:0.85rem;"><i>(Only admins can change report status)</i></span>'
                f'</div>', unsafe_allow_html=True)
            
            if st.form_submit_button("Update"):
                payload = {
                "title": title,
                "description": description,
                "scammer_contact": scammer_contact,
                "amount_lost": amount_lost,
                }
                result = api_put(f"/reports/{report_id}", payload)
                if result:
                    st.success("Updated successfully!")
                else:
                    st.error("Failed to update.")
                    st.warning("Could not load report.")


def user_delete():
    """Delete page scoped to the current user's own reports."""
    st.title("🗑️ Delete My Reports")
    labels, ids = get_report_id_options(only_mine=True)
    if not labels:
        st.info("You have no reports to delete.")
        return
    selected_label = st.selectbox("Select Your Report to Delete", labels)
    report_id = ids[labels.index(selected_label)]
    r = api_get(f"/reports/{report_id}")
    if r:
        with st.expander("📄 Preview Report", expanded=True):
            st.write("**Title:**", r["title"])
            st.write("**Type:**", r["scam_type"])
            st.write("**Status:**", r["status"])
            st.write("**Description:**", r["description"])
            st.write("**Amount Lost:**", r.get("amount_lost", 0))
    st.warning(f"⚠️ You are about to delete **ID {report_id}**. This action cannot be undone.")
    if st.button("🗑️ Confirm Delete", type="primary"):
        res = api_delete(f"/reports/{report_id}")
        if res:
            st.success(f"Report ID {report_id} deleted.")
            st.rerun()
        else:
            st.error("Failed to delete.")


# ─────────────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────────────
if not st.session_state.logged_in:
    auth_page()
else:
    render_sidebar()
    page = st.session_state.page
    role = st.session_state.role

    # ── ADMIN routes ──
    if role == "admin":
        if page == "📊 Dashboard":
            dashboard()
        elif page == "📋 All Reports":
            all_reports()
        elif page == "➕ Submit Report":
            submit_report()
        elif page == "🔍 Search":
            admin_search()
        elif page == "✏️ Update":
            admin_update()
        elif page == "👥 Users":
            admin_users()
        elif page == "🗑️ Delete":
            admin_delete()
        else:
            dashboard()

    # ── USER routes ──
    else:
        if page == "📊 My Analytics":
            user_analytics()
        elif page == "➕ Submit Report":
            submit_report()
        elif page == "✏️ Update My Reports":
            user_update()
        elif page == "🗑️ Delete My Reports":
            user_delete()
        else:
            user_analytics()

# ─────────────────────────────────────────────────────
#  Rights Footer
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    font-size: 14px;
    color: gray;
}
</style>

<div class="footer">
    <p>&copy; 2026 🛡️ ScamWatch. All rights reserved</p>
</div>
""", unsafe_allow_html=True)