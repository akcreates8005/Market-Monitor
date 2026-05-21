import streamlit as st
from newsapi import NewsApiClient

# Layout setup
st.set_page_config(page_title="Market Intelligence", layout="wide")

# Futuristic Styling (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #00ffcc;
    }
    .stApp {
        background: linear-gradient(to right, #000000, #1a1a2e);
    }
    h1 {
        color: #00ffcc;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 Market Evolution Hub")
st.markdown("### *The future of finance is changing. Stay ahead of the curve.*")

# Default companies
default_companies = ["NVIDIA", "Tesla", "Apple"]

for company in default_companies:
    st.markdown("---")
    st.subheader(f"🌐 Real-time Insight: {company}")
    
    articles = newsapi.get_everything(q=company, language='en', sort_by='publishedAt', page_size=3)
    
    if articles['articles']:
        cols = st.columns(3)
        for i, article in enumerate(articles['articles']):
            with cols[i]:
                st.write(f"**{article['title']}**")
                st.write(f"[Read Analysis]({article['url']})")
    else:
        st.write("No new signals detected.")
