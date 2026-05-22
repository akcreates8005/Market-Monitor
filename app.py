import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Futuristic Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; text-transform: uppercase; }
    h3 { color: #00ffcc !important; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #ffffff !important; }
    .sentiment { font-weight: bold; color: #aaaaaa; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")
st.markdown("### *High-precision financial intelligence tracking.*")

# Search/Filter Bar
search_query = st.text_input("🔍 Search company/sector:", "")
target_list = [search_query] if search_query else ["NVIDIA", "Tesla", "Apple"]

for company in target_list:
    st.markdown("---")
    st.subheader(f"🌐 MARKET SIGNALS: {company}")
    
    # Gold Standard Filter: Financial sources + Market keywords
    articles = newsapi.get_everything(
        q=f"{company} AND (merger OR partnership OR acquisition OR stock OR revenue OR earnings OR dividend)",
        domains='bloomberg.com,reuters.com,cnbc.com,wsj.com,ft.com',
        language='en',
        sort_by='publishedAt',
        page_size=3
    )
    
    if articles['articles']:
        for article in articles['articles']:
            # Sentiment based on Title + Description
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            # Format date
            pub_date = article['publishedAt'][:10] 
            
            # Display Article
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Date:** {pub_date} | **Sentiment:** {sentiment}")
            if article['description']:
                st.write(f"*{article['description']}*")
            st.write(f"[Read Full Report]({article['url']})")
            st.markdown("---")
    else:
        st.write("No major market signals detected.")
