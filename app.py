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
    h2, h3 { color: #00ffcc !important; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #ffffff !important; }
    div.stMarkdown > div > p { color: #e0e0e0 !important; }
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# Badi Company List
options = ["", "Technology", "Finance", "Healthcare", "NVIDIA", "Tesla", "Apple", "Netflix", "Microsoft", "Amazon", "Google", "Meta", "AMD", "Intel", "JP Morgan", "Goldman Sachs"]
selected_item = st.selectbox("🎯 Select a Sector or Company to track:", options)

# Logic: Selection hote hi news load hogi
target_list = [selected_item] if selected_item else ["Technology", "Finance", "Healthcare"]

for item in target_list:
    st.markdown("---")
    st.subheader(f"🌐 MARKET SIGNALS: {item if item else 'Overview'}")
    
    # NewsAPI Call
    articles = newsapi.get_everything(
        q=f"{item} AND (stock OR merger OR earnings)",
        domains='bloomberg.com,reuters.com,cnbc.com,wsj.com',
        language='en',
        sort_by='publishedAt',
        page_size=10
    )
    
    if articles['articles']:
        for article in articles['articles']:
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            with st.expander("Click to view available details"):
                st.markdown("### Summary")
                st.info(article['description'] if article['description'] else "No detailed summary available.")                
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No active signals found.")
