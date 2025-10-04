from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
parser = StrOutputParser()
def get_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get all paragraph text
    paragraphs = soup.find_all('p')
    return ' '.join([p.get_text() for p in paragraphs])


def summarize_article(text):
    # Prompt template to summarize in exactly 3 lines
    prompt = PromptTemplate(
        input_variables=["article"],
        template="Summarize the following news article into exactly 3 concise lines:\n\n{article}"
    )
    
    llm = ChatGroq(model ="llama-3.1-8b-instant") 
    chain = prompt | llm | parser
    
    summary = chain.invoke(text)
    return summary



st.title("Article Sumemrizer")
url = st.text_input("Enter URL here :")

if st.button("summerize") :
    article_text = get_article_text(url)
    summary = summarize_article(article_text)
    st.write(summary)