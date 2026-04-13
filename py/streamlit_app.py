import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="MongoDB Database Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
Mongo_API = "http://127.0.0.1:8000"


# ─────────────────────────────────────────────
# API Helper Functions
# ─────────────────────────────────────────────

def check_api_connection():
    try:
        response = requests.get(f"{Mongo_API}/")
        return response.status_code == 200
    except:
        return False


def create_user(name, email, age):
    """Create new user via API"""
    try:
        response = requests.post(
            f"{Mongo_API}/users",
            json={"name": name, "email": email, "age": age}
        )
        return response.json(), response.status_code == 201
    except Exception as e:
        return {"detail": str(e)}, False


def get_all_users():
    """Get all users via API"""
    try:
        response = requests.get(f"{Mongo_API}/users/")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception as e:
        return [], False


def get_user_by_id(user_id):
    """Get user by ID via API"""
    try:
        response = requests.get(f"{Mongo_API}/users/{user_id}")
        if response.status_code == 200:
            return response.json(), True
        return None, False
    except Exception as e:
        return None, False


def get_user_posts(user_id):
    """Get user posts via API"""
    try:
        response = requests.get(f"{Mongo_API}/users/{user_id}/posts")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception as e:
        return [], False


def create_post(user_id, title, content):
    """Create new post via API"""
    try:
        response = requests.post(
            f"{Mongo_API}/posts/",
            json={"user_id": user_id, "title": title, "content": content}
        )
        return response.json(), response.status_code == 201
    except Exception as e:
        return {"detail": str(e)}, False


def get_all_posts():
    """Get all posts via API"""
    try:
        response = requests.get(f"{Mongo_API}/posts/")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception as e:
        return {"error": str(e)}, False


def delete_user(user_id):
    """Delete user by ID via API (with confirm flag)"""
    try:
        response = requests.delete(f"{Mongo_API}/users/{user_id}?confirm=true")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error deleting user: {e}")
        return False


def delete_post(post_id):
    """Delete post by ID via API"""
    try:
        response = requests.delete(f"{Mongo_API}/posts/{post_id}")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error deleting post: {e}")
        return False


def update_user(user_id, name, email, age):
    """Update user by ID via API"""
    try:
        response = requests.put(
            f"{Mongo_API}/users/{user_id}",
            json={"name": name, "email": email, "age": age}
        )
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"detail": str(e)}, False


# ─────────────────────────────────────────────
# Page Functions
# ─────────────────────────────────────────────

def user_page():
    st.header("🐧 User Management")
    tab1, tab2, tab3 = st.tabs(["Create User", "View Users", "Manage User"])

    # ── Tab 1: Create User ──
    with tab1:
        st.subheader("Create New User")
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name", placeholder="Enter user name")
                email = st.text_input("Email", placeholder="Enter email")
            with col2:
                age = st.number_input("Age", min_value=0, max_value=120, value=25)

            submitted = st.form_submit_button("Create User", type="primary")

            if submitted:
                if name and email:
                    result, success = create_user(name, email, age)
                    if success:
                        st.success(f"✅ User '{result['name']}' created successfully with ID: {result['id']}")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('detail', 'Unknown error')} — Failed to create user.")
                else:
                    st.warning("⚠️ Please fill in all required fields (Name and Email).")

    # ── Tab 2: View Users ──
    with tab2:
        st.subheader("View All Users")
        users, success = get_all_users()

        if success and users:
            df = pd.DataFrame(users)
            df["created_at"] = pd.to_datetime(df["created_at"])

            st.dataframe(
                df[["id", "name", "email", "age", "created_at"]].rename(columns={
                    "id": "User ID",
                    "name": "Name",
                    "email": "Email",
                    "age": "Age",
                    "created_at": "Created At"
                }),
                use_container_width=True,
                hide_index=True
            )
            st.info(f"Total Users: {len(users)}")
        else:
            st.info("No users found. Please create some users to see them here.")

    # ── Tab 3: Manage User ──
    with tab3:
        st.subheader("Manage User")
        users, success = get_all_users()

        if success and users:
            user_options = {f"{user['name']} ({user['id']})": user['id'] for user in users}
            selected_user_display = st.selectbox("Select User to Manage", options=list(user_options.keys()))

            if selected_user_display:
                selected_user_id = user_options[selected_user_display]
                selected_user = next((user for user in users if user['id'] == selected_user_id), None)

                if selected_user:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Update User Info**")
                        with st.form("update_user_form"):
                            name = st.text_input("Name", value=selected_user['name'])
                            email = st.text_input("Email", value=selected_user['email'])
                            age = st.number_input("Age", min_value=0, max_value=120, value=selected_user['age'])

                            if st.form_submit_button("Update User", type="primary"):
                                result, success = update_user(selected_user_id, name, email, age)
                                if success:
                                    st.success("✅ User updated successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Error: {result.get('detail', 'Unknown error')} — Failed to update user.")

                    with col2:
                        st.write("**Delete User**")
                        st.warning("⚠️ Deleting a user will also delete all their posts. This action cannot be undone.")
                        if st.button("Delete User", type="secondary"):
                            success = delete_user(selected_user_id)
                            if success:
                                st.success(f"✅ User '{selected_user['name']}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete user. Please try again.")
        else:
            st.info("No users found.")


def post_page():
    st.header("📰 Post Management")
    tab1, tab2, tab3 = st.tabs(["Create Post", "View Posts", "Posts by User"])

    # ── Tab 1: Create Post ──
    with tab1:
        st.subheader("Create New Post")
        users, success = get_all_users()

        if success and users:
            with st.form("create_post_form"):
                user_options = {f"{user['name']} ({user['id']})": user['id'] for user in users}
                selected_user_display = st.selectbox("Select User for Post", options=list(user_options.keys()))
                title = st.text_input("Post Title", placeholder="Enter post title")
                content = st.text_area("Post Content", placeholder="Enter post content")

                submitted = st.form_submit_button("Create Post", type="primary")

                if submitted:
                    if selected_user_display and title and content:
                        selected_user_id = user_options[selected_user_display]
                        result, success = create_post(selected_user_id, title, content)
                        if success:
                            st.success(f"✅ Post created successfully with ID: {result.get('id', 'N/A')}")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result.get('detail', 'Unknown error')} — Failed to create post.")
                    else:
                        st.warning("⚠️ Please fill in all required fields (User, Title, and Content).")
        else:
            st.warning("⚠️ No users found. Please create a user before creating posts.")

    # ── Tab 2: View All Posts ──
    with tab2:
        st.subheader("View All Posts")
        posts, success = get_all_posts()

        if success and posts:
            for post in posts:
                with st.expander(f"{post['title']} (by User {post['user_id'][:8]})"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Content:** {post['content']}")
                        st.write(f"**Created At:** {pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")

                    with col2:
                        st.write(f"**User ID:** {post['user_id'][:8]}")
                        if st.button("Delete Post", key=f"delete_{post['id']}", type="secondary"):
                            success = delete_post(post['id'])
                            if success:
                                st.success(f"✅ Post '{post['title']}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete post. Please try again.")
        else:
            st.info("No posts found.")

    # ── Tab 3: Posts by User ──
    with tab3:
        st.subheader("Posts by User")
        users, users_success = get_all_users()

        if users_success and users:
            user_options = {f"{user['name']} ({user['id']})": user['id'] for user in users}
            selected_user_display = st.selectbox("Select User to View Posts", options=list(user_options.keys()))

            if selected_user_display:
                selected_user_id = user_options[selected_user_display]
                user_posts, posts_success = get_user_posts(selected_user_id)

                if posts_success and user_posts:
                    for post in user_posts:
                        with st.expander(f"{post['title']}"):
                            st.write(f"**Content:** {post['content']}")
                            st.write(f"**Created At:** {pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    st.info("No posts found for this user.")
        else:
            st.info("No users found.")


def dashboard_page():
    st.header("📊 Dashboard")

    users, users_success = get_all_users()
    posts, posts_success = get_all_posts()

    if users_success and posts_success:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Users", len(users))
        with col2:
            st.metric("Total Posts", len(posts))
        with col3:
            avg_posts_per_user = len(posts) / len(users) if users else 0
            st.metric("Avg Posts/User", f"{avg_posts_per_user:.1f}")
        with col4:
            st.metric("Posts per User", f"{avg_posts_per_user:.1f}")

        st.markdown("---")

        if users:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("User Age Distribution")
                age_data = pd.DataFrame(users)["age"]
                st.bar_chart(pd.Series(age_data).value_counts().sort_index())

            with col2:
                st.subheader("Recent Activity")
                if posts:
                    posts_df = pd.DataFrame(posts)
                    posts_df['date'] = pd.to_datetime(posts_df['created_at']).dt.date
                    daily_posts = posts_df.groupby('date').size()
                    st.line_chart(daily_posts)

        st.subheader("Recent Posts")
        if posts:
            recent_posts = sorted(posts, key=lambda x: x['created_at'], reverse=True)[:5]
            for post in recent_posts:
                created = pd.to_datetime(post['created_at']).strftime('%Y-%m-%d %H:%M:%S')
                st.write(f"**{post['title']}** by User `{post['user_id'][:8]}` on {created}")
    else:
        st.error("❌ Failed to load Dashboard data.")


# ─────────────────────────────────────────────
# Main App
# ─────────────────────────────────────────────

def main():
    st.title("📚 MongoDB Database Manager")
    st.markdown("Manage your MongoDB database with ease. Create, read, update, and delete users and posts through a friendly interface.")

    if not check_api_connection():
        st.error("❌ Unable to connect to the API. Please ensure the FastAPI backend is running on http://127.0.0.1:8000")
        st.stop()

    st.success("✅ Successfully connected to the API!")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Go to",
        ["🏠 Home", "🐧 Users", "📰 Posts", "🖥 Dashboard"]
    )

    if page == "🏠 Home":
        st.subheader("Welcome to the MongoDB Database Manager!")
        st.markdown("Use the sidebar to navigate between users and posts management.")
    elif page == "🐧 Users":
        user_page()
    elif page == "📰 Posts":                                                
        post_page()
    elif page == "🖥 Dashboard":
        dashboard_page()


if __name__ == "__main__":
    main()


