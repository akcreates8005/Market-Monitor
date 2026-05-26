import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob

# Page Config
st.set_page_config(page_title="Market Evolution Hub", layout="wide")

# Styling: Aqua Neon Headlines & Bright White Text
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    h1 { color: #00ffcc !important; text-align: center; }
    h2, h3 { color: #00e5ff !important; }
    
    /* Headlines - Cyan/Aqua Neon */
    .headline { font-size: 1.3rem !important; font-weight: 800 !important; color: #00e5ff !important; }
    
    /* Body text - Bright White */
    div.stMarkdown > div > p { color: #ffffff !important; }
    
    /* Labels (Sentiment etc.) */
    label, p { color: #ffffff !important; }
    
    /* Expander */
    .streamlit-expanderHeader { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("🚀 MARKET EVOLUTION HUB")

# Global Search
search_query = st.text_input("🔍 Search specific ticker or company:", "").strip()

# LOGIC:
if search_query:
    st.subheader(f"🌐 SEARCH RESULTS: {search_query.upper()}")
    query_string = f"({search_query}) AND (stock OR market OR earnings)"
else:
    st.subheader("🔥 MARKET PULSE: Top 20 Hyper-News")
    # Robinhood-favorite stocks list
    query_string = "(Nvidia OR Tesla OR Apple OR SpaceX OR Amazon OR Microsoft OR Google OR Meta OR AMD OR Palantir OR Netflix) AND (stock OR market OR earnings)"

# Display 45 articles (as per your request)
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
