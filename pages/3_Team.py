import streamlit as st

st.set_page_config(
    page_title="Our Team",
    page_icon="👥",
    layout="centered"
)

st.title("👥 Team #1")
st.subheader("Meet the developers behind Saudi Culinary Chatbot")

st.markdown("---")


col1, col2 = st.columns([1, 3])
with col1:
    st.image("images/team-member-placeholder.jpg", width=150)
with col2:
    st.subheader("Rahaf Alshahrani")
    st.write("**Role:** UI/UX Developer , Integration Lead")
    st.write("**Responsibility:** Designed all user interfaces and Connected all components")

st.markdown("---")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("images/team-member-placeholder.jpg", width=150)
with col2:
    st.subheader("Lama Alsubaie")
    st.write("**Role:** Recipe Database Specialist")
    st.write("**Responsibility:** Collected Saudi recipes")

st.markdown("---")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("images/team-member-placeholder.jpg", width=150)
with col2:
    st.subheader("Fawziah Alselwly")
    st.write("**Role:** Intent Classification Specialist")
    st.write("**Responsibility:** Built conversation understanding")

st.markdown("---")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("images/team-member-placeholder.jpg", width=150)
with col2:
    st.subheader("Shamah Alshahrani")
    st.write("**Role:** Response Generation Specialist")
    st.write("**Responsibility:** Created natural responses")

st.markdown("---")

st.header("📊 Project Information")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Recipes", "15+")
    st.metric("Lines of Code", "1000+")
with col2:
    st.metric("Development Time", "2 Days")
    st.metric("Team Size", "4")