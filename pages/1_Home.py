import streamlit as st

st.set_page_config(
    page_title="Saudi Culinary Chatbot",
    page_icon="🇸🇦",
    layout="centered"
)

st.title("🇸🇦 Welcome to Saudi Culinary Journey!")

st.markdown("""
### Meet Norah, Your Saudi Food Guide

Norah is here to help foreigners discover the rich flavors of authentic Saudi cuisine. 
Whether you're curious about Kabsa, Mandi, or traditional desserts, she'll guide you step by step!

---

### 💬 What You Can Do

**Chat naturally** - Ask Norah anything about Saudi food  
**Get authentic recipes** - Complete ingredients and cooking steps  
**Learn cultural context** - Understand the story behind each dish

---
""")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.page_link("pages/2_Chat.py", label="💬 Start Chatting with Norah", use_container_width=True)

st.markdown("---")
st.caption("🌟 Bringing Saudi culinary heritage to the world")