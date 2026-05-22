import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    .headline { font-size: 1.2rem !important; font-weight: 700 !important; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# 1. Predefined sectors/companies for automatic load
target_sectors = ["Technology", "Finance", "Healthcare"]

for sector in target_sectors:
    st.markdown("---")
    st.subheader(f"🌐 SECTOR TREND: {sector}")
    
    # Fetch news automatically on load
    articles = newsapi.get_everything(
        q=f"{sector} AND (stock OR merger OR earnings)",
        domains='bloomberg.com,reuters.com,cnbc.com,wsj.com',
        language='en',
        sort_by='publishedAt',
        page_size=3
    )
    
    if articles['articles']:
        for article in articles['articles']:
            # Sentiment
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            # Display headline
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            # 2. Collapsible Summary Section
            with st.expander("View 8-10 line summary"):
                summary = article['description'] or "No summary available."
                st.write(summary)
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No active signals.")
