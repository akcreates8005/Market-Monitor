import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #ffffff !important; }
    div.stMarkdown > div > p { color: #e0e0e0 !important; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# Global Search
search_query = st.text_input("🔍 Search specific ticker or company:", "").strip()

# LOGIC:
# If user searches, show that news. 
# If empty, show the "Market Pulse" (Top 20 Hyper-News for Robinhood-favorite stocks)
if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {search_query.upper()}")
    query_string = f"({search_query}) AND (stock OR market OR earnings)"
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    # This list covers the stocks most common on Robinhood platforms
    query_string = "(Nvidia OR Tesla OR Apple OR SpaceX OR Amazon OR Microsoft OR Google OR Meta OR AMD OR Palantir OR Netflix) AND (stock OR market OR earnings)"

# Display 20 articles
articles = newsapi.get_everything(
    q=query_string,
    language='en',
    sort_by='relevancy', 
    page_size=45
)

if articles['articles']:
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
    st.write("No major market signals detected right now.")
