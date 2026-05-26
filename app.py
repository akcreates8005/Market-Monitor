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
    h2, h3 { color: #00e5ff !important; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #00e5ff !important; }
    div.stMarkdown > div > p { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# 1. Yeh text_input ab "Global Search" ki tarah kaam karega
# Robinhood par jo bhi company hai, bas uska naam type karo, yeh dhund lega
search_query = st.text_input("🔍 Search any company or ticker globally (e.g., IBM, American Express, Ford):", "").strip()

# LOGIC
if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {search_query.upper()}")
    # NewsAPI ka backend engine khud samajh jayega ki tumne kya search kiya hai
    # Ismein humein list ki zaroorat nahi hai
    query_string = f"({search_query}) AND (stock OR market OR earnings)"
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    query_string = "(Nvidia OR Tesla OR Apple OR SpaceX OR Amazon) AND (stock OR market OR earnings)"

# Fetching news
try:
    articles = newsapi.get_everything(
        q=query_string,
        language='en',
        sort_by='relevancy', 
        page_size=30
    )
    
    if articles and articles.get('articles'):
        for article in articles['articles']:
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            with st.expander("Click to view details"):
                st.info(article['description'] or "No summary available.")
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No results found. Try a different company name.")
except Exception as e:
    st.error("Error fetching news. Please check your API key.")
