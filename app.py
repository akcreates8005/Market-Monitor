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

# SEARCH BAR ADDED HERE
search_query = st.text_input("🔍 Search specific company/sector (e.g., Apple, Tesla, Crypto):", "")

# Logic: Search hoga toh sirf wo dikhega, varna default sectors
target_list = [search_query] if search_query else ["Technology", "Finance", "Healthcare"]

for item in target_list:
    st.markdown("---")
    st.subheader(f"🌐 MARKET SIGNALS: {item}")
    
    # Fetch news
    articles = newsapi.get_everything(
        q=f"{item} AND (stock OR merger OR earnings)",
        domains='bloomberg.com,reuters.com,cnbc.com,wsj.com',
        language='en',
        sort_by='publishedAt',
        page_size=10 # Badha kar 10 kar diya hai
    )
    
    if articles['articles']:
        for article in articles['articles']:
            # Sentiment
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            # Display headline
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            # Collapsible Summary Section
            with st.expander("Click to view available details"):
                st.markdown("### Summary")
                st.info(article['description'] if article['description'] else "No detailed summary available from this source.")                
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No active signals found for this search.")
