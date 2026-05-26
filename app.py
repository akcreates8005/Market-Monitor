import streamlit as st
import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Styling: Aqua Neon & White
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    h2, h3 { color: #00e5ff !important; }
    
    /* Search Bar Input Color */
    .stSelectbox > div > div { color: #ffffff !important; background-color: #111111 !important; border: 1px solid #00e5ff !important; }
    
    /* Headlines - Cyan/Aqua Neon */
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #00e5ff !important; }
    
    /* Body text - Bright White */
    div.stMarkdown > div > p { color: #ffffff !important; }
    
    /* Labels */
    label, p { color: #ffffff !important; }
    
    /* Expander */
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# DYNAMIC TICKER LIST: Yeh link market ki latest companies fetch karegi
@st.cache_data
def get_market_tickers():
    url = "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nasdaq/nasdaq_full.csv"
    try:
        df = pd.read_csv(url)
        # Ticker aur Name ko combine karke list banayein
        return (df['Symbol'] + " - " + df['Name']).tolist()
    except:
        # Agar net issue ho toh fallback
        return ["AAPL - Apple", "TSLA - Tesla", "NVDA - Nvidia", "MSFT - Microsoft", "AMZN - Amazon"]

all_stocks = get_market_tickers()

# SEARCH BAR
selected = st.selectbox(
    "🎯 Search or Select any company (Type to search thousands):", 
    options=[""] + all_stocks,
    index=0
)

# LOGIC
search_query = selected.split(" - ")[-1] if selected else ""

if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {search_query.upper()}")
    query_string = f"({search_query}) AND (stock OR market OR earnings)"
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    query_string = "(Nvidia OR Tesla OR Apple OR SpaceX OR Amazon) AND (stock OR market OR earnings)"

# NEWS FETCHING
try:
    articles = newsapi.get_everything(
        q=query_string,
        language='en',
        sort_by='relevancy', 
        page_size=45
    )

    if articles and articles.get('articles'):
        for article in articles['articles']:
            analysis = TextBlob(article['title'] + " " + (article['description'] or ""))
            sentiment = "🟢 Positive" if analysis.sentiment.polarity > 0.1 else "🔴 Negative" if analysis.sentiment.polarity < -0.1 else "⚪ Neutral"
            
            st.markdown(f'<p class="headline">{article["title"]}</p>', unsafe_allow_html=True)
            st.write(f"**Sentiment:** {sentiment}")
            
            with st.expander("Click to view details"):
                st.info(article['description'] if article['description'] else "No summary available.")                
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"[Read Full Report]({article['url']})")
    else:
        st.write("No major market signals detected.")
except Exception as e:
    st.error("Error fetching news. Please check your API configuration.")
