import streamlit as st
import requests

# 🔗 API Endpoints
API_BASE = "https://yl7wyy00bc.execute-api.ap-south-1.amazonaws.com/prod"
UPLOAD_URL = f"{API_BASE}/uploadfilehandler"
LIST_URL = f"{API_BASE}/listfiles"
DOWNLOAD_URL = f"{API_BASE}/downloadfile"
REGISTER_URL = f"{API_BASE}/registeruser"

# 🎨 Page Setup
st.set_page_config(page_title="☁️ File Share Cloud", page_icon="📁")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>☁️ File Sharing System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Secure, Simple & Serverless 💡</p>", unsafe_allow_html=True)

st.divider()

# 🧭 Tabs for flow control
tab1, tab2 = st.tabs(["📧 Register Email", "🔐 Access with User ID"])

# ✉️ Tab 1: Email Registration
with tab1:
    st.subheader("Register with your Email")
    email = st.text_input("📨 Enter your email")

    if st.button("Generate User ID"):
        if email:
            res = requests.post(REGISTER_URL, json={"email": email})
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ {data['message']}")
                st.code(data['user_id'], language="text")
                st.info("💡 Save this User ID to access your files next time.")
            else:
                st.error(f"Error: {res.text}")
        else:
            st.warning("Please enter a valid email.")

# 🔐 Tab 2: File Operations
with tab2:
    st.subheader("Enter Your User ID")
    user_id = st.text_input("🔑 User ID", placeholder="e.g. a1b2c3")

    if user_id:
        st.markdown("---")
        st.subheader("📤 Upload a File")
        uploaded_file = st.file_uploader("Select a file")

        if st.button("Upload File", use_container_width=True) and uploaded_file:
            files = {'file': (uploaded_file.name, uploaded_file.getvalue())}
            headers = {'user_id': user_id}
            res = requests.post(UPLOAD_URL, files=files, headers=headers)

            if res.status_code == 200:
                file_id = res.json().get("file_id", "")
                st.success(f"✅ File uploaded! File ID: `{file_id}`")
            else:
                st.error(f"Upload failed: {res.text}")

        st.markdown("---")
        st.subheader("📂 View & Download Your Files")

        if st.button("Refresh File List 🔄", use_container_width=True):
            res = requests.get(LIST_URL, params={"user_id": user_id})
            if res.status_code == 200:
                files = res.json().get("files", [])
                if not files:
                    st.info("You haven't uploaded any files yet.")
                else:
                    file_map = {f["filename"]: f for f in files}
                    selected = st.selectbox("Choose a file", list(file_map.keys()))
                    file_id = file_map[selected]["file_id"]

                    if st.button("⬇️ Download", use_container_width=True):
                        res = requests.get(DOWNLOAD_URL, params={"file_id": file_id})
                        if res.status_code == 200:
                            download_url = res.json().get("download_url")
                            st.markdown(f"[🔗 Click to Download {selected}]({download_url})", unsafe_allow_html=True)
                        else:
                            st.error("Could not generate download link.")
            else:
                st.error("Failed to fetch file list.")

st.divider()
st.markdown("<p style='text-align: center; font-size: 12px;'>Made with ❤️ by Manas • Powered by AWS Lambda, S3, DynamoDB</p>", unsafe_allow_html=True)
