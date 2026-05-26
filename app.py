import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Styling: Fixed Visibility
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    h2, h3 { color: #00e5ff !important; }
    
    /* Search Bar Input: White Background, Black Text */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #00e5ff !important;
    }
    
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #00e5ff !important; }
    div.stMarkdown > div > p { color: #ffffff !important; }
    label, p { color: #ffffff !important; }
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# SEARCH ENGINE: Dropdown ki jagah text_input (Yahi best hai)
search_query = st.text_input("🎯 Enter Company Name or Ticker (e.g., GLD, Nvidia, Apple):", "").strip()

# LOGIC
if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {search_query.upper()}")
    # NewsAPI ka engine khud search karega, list ki limit khatam
    query_string = f"{search_query} stock market"
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    query_string = "(Nvidia OR Tesla OR Apple OR SpaceX OR Amazon) AND (stock OR market)"

# NEWS FETCHING
try:
    articles = newsapi.get_everything(q=query_string, language='en', sort_by='relevancy', page_size=30)
    
    if articles and articles.get('articles'):
        for article in articles['articles']:
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            with st.expander("Click to view details"):
                st.info(article['description'] or "No summary available.")
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("Searching... try a valid company name.")
except Exception as e:
    st.error("Check your API key.")
