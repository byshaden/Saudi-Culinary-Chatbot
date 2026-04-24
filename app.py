import streamlit as st

st.set_page_config(
    page_title="Saudi Culinary Chatbot",
    page_icon="🇸🇦",
    layout="wide"
)

# Main page
st.title("🇸🇦 Saudi Culinary Chatbot")
st.write("Use the sidebar to navigate between pages!")

st.page_link("pages/1_Home.py", label="🏠 Home", icon="🏠")
st.page_link("pages/2_Chat.py", label="💬 Chat", icon="💬")
st.page_link("pages/3_Team.py", label="👥 Team", icon="👥")