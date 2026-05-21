import streamlit as st
from newsapi import NewsApiClient

# Streamlit secrets se API key uthayega
# Note: Hum secrets baad mein set karenge
api_key = st.secrets["NEWS_API_KEY"]
newsapi = NewsApiClient(api_key=api_key)

st.title("Global Market Intelligence 🌍")

# Yahan user khud company ka naam type karega
company_input = st.text_input("Konsi company track karni hai? (e.g., NVIDIA, Toyota, Reliance):")

if st.button("Fetch News"):
    if company_input:
        st.subheader(f"News for {company_input}")
        
        # API se news fetch karna
        # 'language' English mein rakha hai
        all_articles = newsapi.get_everything(q=company_input, language='en', sort_by='publishedAt', page_size=10)
        
        if all_articles['totalResults'] > 0:
            for article in all_articles['articles']:
                st.write(f"**{article['title']}**")
                st.write(f"{article['description']}")
                st.write(f"[Read More]({article['url']})")
                st.markdown("---")
        else:
            st.write("Is company ki koi nayi khabar nahi mili.")
    else:
        st.write("Please koi company ka naam type karo.")
