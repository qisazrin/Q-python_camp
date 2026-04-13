# Streamlit + CSS markdown

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MongoDB Database Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.nav-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid rgba(99, 179, 237, 0.2);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    margin-bottom: 0.75rem;
}
.nav-card .icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.nav-card .title {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #63b3ed;
    margin-bottom: 0.4rem;
}
.nav-card .desc { font-size: 0.85rem; color: #a0aec0; line-height: 1.5; }

.hero {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    border: 1px solid rgba(99, 179, 237, 0.15);
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    color: #fff;
    margin-bottom: 0.5rem;
}
.hero p { color: #a0aec0; font-size: 1rem; max-width: 520px; margin: 0 auto; }
.hero .badge {
    display: inline-block;
    background: rgba(99, 179, 237, 0.15);
    color: #63b3ed;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    border: 1px solid rgba(99, 179, 237, 0.3);
    margin-bottom: 1rem;
}

.status-ok {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(72, 187, 120, 0.1); color: #48bb78;
    border: 1px solid rgba(72, 187, 120, 0.3);
    border-radius: 20px; padding: 0.3rem 1rem;
    font-size: 0.8rem; font-family: 'Space Mono', monospace; margin-top: 1rem;
}
.status-err {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(245, 101, 101, 0.1); color: #f56565;
    border: 1px solid rgba(245, 101, 101, 0.3);
    border-radius: 20px; padding: 0.3rem 1rem;
    font-size: 0.8rem; font-family: 'Space Mono', monospace; margin-top: 1rem;
}

div.stButton > button {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    border-radius: 10px;
    transition: all 0.2s ease;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3182ce, #63b3ed);
    border: none; color: white;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2b6cb0, #3182ce);
    box-shadow: 0 4px 15px rgba(99, 179, 237, 0.4);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ─────────────────────────────────────────────
# API Config & Helpers
# ─────────────────────────────────────────────
Mongo_API = "http://127.0.0.1:8000"

def check_api_connection():
    try:
        return requests.get(f"{Mongo_API}/", timeout=3).status_code == 200
    except:
        return False

def create_user(name, email, age):
    try:
        r = requests.post(f"{Mongo_API}/users", json={"name": name, "email": email, "age": age})
        return r.json(), r.status_code == 201
    except Exception as e:
        return {"detail": str(e)}, False

def get_all_users():
    try:
        r = requests.get(f"{Mongo_API}/users/")
        return (r.json(), True) if r.status_code == 200 else ([], False)
    except:
        return [], False

def get_user_posts(user_id):
    try:
        r = requests.get(f"{Mongo_API}/users/{user_id}/posts")
        return (r.json(), True) if r.status_code == 200 else ([], False)
    except:
        return [], False

def create_post(user_id, title, content):
    try:
        r = requests.post(f"{Mongo_API}/posts/", json={"user_id": user_id, "title": title, "content": content})
        return r.json(), r.status_code == 201
    except Exception as e:
        return {"detail": str(e)}, False

def get_all_posts():
    try:
        r = requests.get(f"{Mongo_API}/posts/")
        return (r.json(), True) if r.status_code == 200 else ([], False)
    except Exception as e:
        return {"error": str(e)}, False

def delete_user(user_id):
    try:
        return requests.delete(f"{Mongo_API}/users/{user_id}?confirm=true").status_code == 200
    except:
        return False

def delete_post(post_id):
    try:
        return requests.delete(f"{Mongo_API}/posts/{post_id}").status_code == 200
    except:
        return False

def update_user(user_id, name, email, age):
    try:
        r = requests.put(f"{Mongo_API}/users/{user_id}", json={"name": name, "email": email, "age": age})
        return r.json(), r.status_code == 200
    except Exception as e:
        return {"detail": str(e)}, False


# ─────────────────────────────────────────────
# Sidebar Navigation
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 DB Manager")
    st.markdown("---")

    for label in ["🏠 Home", "🐧 Users", "📰 Posts", "🖥 Dashboard"]:
        is_active = st.session_state.page == label
        if st.button(
            f"{'▶  ' if is_active else ''}{label}",
            key=f"sidebar_{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = label
            st.rerun()

    st.markdown("---")
    connected = check_api_connection()
    if connected:
        st.markdown('<div class="status-ok">● API Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-err">● API Offline</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Page: Home
# ─────────────────────────────────────────────
def home_page(connected):
    st.markdown("""
    <div class="hero">
        <div class="badge">MongoDB · FastAPI · Streamlit</div>
        <h1>📚 DB Manager</h1>
        <p>Create, read, update, and delete users and posts through a clean, unified interface.</p>
    </div>
    """, unsafe_allow_html=True)

    if connected:
        st.markdown('<div style="text-align:center"><span class="status-ok">● FastAPI server is online</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center"><span class="status-err">● FastAPI server is offline — start it first</span></div>', unsafe_allow_html=True)
        st.stop()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("#### Quick Navigation")
    st.markdown("Jump to any section using the cards below or the sidebar.")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="icon">🐧</div>
            <div class="title">Users</div>
            <div class="desc">Create, view, update and delete user accounts in your database.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Users →", key="home_users", use_container_width=True, type="primary"):
            st.session_state.page = "🐧 Users"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="icon">📰</div>
            <div class="title">Posts</div>
            <div class="desc">Manage blog posts linked to users. Create, browse and delete content.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Posts →", key="home_posts", use_container_width=True, type="primary"):
            st.session_state.page = "📰 Posts"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="nav-card">
            <div class="icon">🖥</div>
            <div class="title">Dashboard</div>
            <div class="desc">Visual analytics — user stats, post activity and trends at a glance.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Dashboard →", key="home_dash", use_container_width=True, type="primary"):
            st.session_state.page = "🖥 Dashboard"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Live Stats")
    users, u_ok = get_all_users()
    posts, p_ok = get_all_posts()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Users", len(users) if u_ok else "—")
    c2.metric("Total Posts", len(posts) if p_ok else "—")
    avg = round(len(posts) / len(users), 1) if (u_ok and p_ok and users) else "—"
    c3.metric("Avg Posts / User", avg)


# ─────────────────────────────────────────────
# Page: Users
# ─────────────────────────────────────────────
def user_page():
    st.header("🐧 User Management")
    tab1, tab2, tab3 = st.tabs(["Create User", "View Users", "Manage User"])

    with tab1:
        st.subheader("Create New User")
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name", placeholder="Enter user name")
                email = st.text_input("Email", placeholder="Enter email")
            with col2:
                age = st.number_input("Age", min_value=0, max_value=120, value=25)
            if st.form_submit_button("Create User", type="primary"):
                if name and email:
                    result, ok = create_user(name, email, age)
                    if ok:
                        st.success(f"✅ User '{result['name']}' created with ID: {result['id']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('detail', 'Unknown error')}")
                else:
                    st.warning("⚠️ Name and Email are required.")

    with tab2:
        st.subheader("View All Users")
        users, ok = get_all_users()
        if ok and users:
            df = pd.DataFrame(users)
            df["created_at"] = pd.to_datetime(df["created_at"])
            st.dataframe(
                df[["id", "name", "email", "age", "created_at"]].rename(columns={
                    "id": "User ID", "name": "Name", "email": "Email",
                    "age": "Age", "created_at": "Created At"
                }),
                use_container_width=True, hide_index=True
            )
            st.info(f"Total Users: {len(users)}")
        else:
            st.info("No users found.")

    with tab3:
        st.subheader("Manage User")
        users, ok = get_all_users()
        if ok and users:
            user_options = {f"{u['name']} ({u['id']})": u['id'] for u in users}
            selected = st.selectbox("Select User", options=list(user_options.keys()))
            if selected:
                uid = user_options[selected]
                user = next((u for u in users if u['id'] == uid), None)
                if user:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Update User Info**")
                        with st.form("update_user_form"):
                            name = st.text_input("Name", value=user['name'])
                            email = st.text_input("Email", value=user['email'])
                            age = st.number_input("Age", min_value=0, max_value=120, value=user['age'])
                            if st.form_submit_button("Update User", type="primary"):
                                result, ok2 = update_user(uid, name, email, age)
                                if ok2:
                                    st.success("✅ User updated!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {result.get('detail', 'Unknown error')}")
                    with col2:
                        st.write("**Delete User**")
                        st.warning("⚠️ This will also delete all their posts.")
                        if st.button("Delete User", type="secondary"):
                            if delete_user(uid):
                                st.success(f"✅ User '{user['name']}' deleted!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete user.")
        else:
            st.info("No users found.")


# ─────────────────────────────────────────────
# Page: Posts
# ─────────────────────────────────────────────
def post_page():
    st.header("📰 Post Management")
    tab1, tab2, tab3 = st.tabs(["Create Post", "View Posts", "Posts by User"])

    with tab1:
        st.subheader("Create New Post")
        users, ok = get_all_users()
        if ok and users:
            with st.form("create_post_form"):
                user_options = {f"{u['name']} ({u['id']})": u['id'] for u in users}
                selected = st.selectbox("Select User", options=list(user_options.keys()))
                title = st.text_input("Post Title", placeholder="Enter post title")
                content = st.text_area("Post Content", placeholder="Enter post content")
                if st.form_submit_button("Create Post", type="primary"):
                    if selected and title and content:
                        result, ok2 = create_post(user_options[selected], title, content)
                        if ok2:
                            st.success(f"✅ Post created with ID: {result.get('id', 'N/A')}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('detail', 'Unknown error')}")
                    else:
                        st.warning("⚠️ All fields are required.")
        else:
            st.warning("⚠️ No users found. Create a user first.")

    with tab2:
        st.subheader("View All Posts")
        posts, ok = get_all_posts()
        if ok and posts:
            for post in posts:
                with st.expander(f"{post['title']} — User {post['user_id'][:8]}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Content:** {post['content']}")
                        st.write(f"**Created At:** {pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
                    with col2:
                        if st.button("🗑 Delete", key=f"del_{post['id']}", type="secondary"):
                            if delete_post(post['id']):
                                st.success("✅ Deleted!")
                                st.rerun()
                            else:
                                st.error("❌ Failed.")
        else:
            st.info("No posts found.")

    with tab3:
        st.subheader("Posts by User")
        users, ok = get_all_users()
        if ok and users:
            user_options = {f"{u['name']} ({u['id']})": u['id'] for u in users}
            selected = st.selectbox("Select User", options=list(user_options.keys()), key="posts_by_user")
            if selected:
                user_posts, ok2 = get_user_posts(user_options[selected])
                if ok2 and user_posts:
                    for post in user_posts:
                        with st.expander(post['title']):
                            st.write(f"**Content:** {post['content']}")
                            st.write(f"**Created At:** {pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    st.info("No posts for this user.")
        else:
            st.info("No users found.")


# ─────────────────────────────────────────────
# Page: Dashboard
# ─────────────────────────────────────────────
def dashboard_page():
    st.header("🖥 Dashboard")
    users, u_ok = get_all_users()
    posts, p_ok = get_all_posts()

    if u_ok and p_ok:
        avg = len(posts) / len(users) if users else 0
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Users", len(users))
        c2.metric("Total Posts", len(posts))
        c3.metric("Avg Posts/User", f"{avg:.1f}")
        c4.metric("Active Users", len(set(p['user_id'] for p in posts)) if posts else 0)

        st.markdown("---")

        if users:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("User Age Distribution")
                age_data = pd.DataFrame(users)["age"]
                st.bar_chart(pd.Series(age_data).value_counts().sort_index())
            with col2:
                st.subheader("Daily Post Activity")
                if posts:
                    posts_df = pd.DataFrame(posts)
                    posts_df['date'] = pd.to_datetime(posts_df['created_at']).dt.date
                    st.line_chart(posts_df.groupby('date').size())

        st.subheader("Recent Posts")
        if posts:
            for post in sorted(posts, key=lambda x: x['created_at'], reverse=True)[:5]:
                created = pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M')
                st.write(f"**{post['title']}** — User `{post['user_id'][:8]}` · {created}")
    else:
        st.error("❌ Failed to load dashboard data.")


# ─────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────
connected = check_api_connection()
page = st.session_state.page

if page == "🏠 Home":
    home_page(connected)
else:
    if not connected:
        st.error("❌ Unable to connect to the API. Please ensure the FastAPI backend is running on http://127.0.0.1:8000")
        st.stop()
    if page == "🐧 Users":
        user_page()
    elif page == "📰 Posts":
        post_page()
    elif page == "🖥 Dashboard":
        dashboard_page()