import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Define the LLM and Prompt
llm = Ollama(model="llama2")
embeddings = OllamaEmbeddings(model="llama2")
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer.  
<context>
{context}
</context>
Question: Summarize the website.
""")
document_chain = create_stuff_documents_chain(llm,prompt)

# Input section
website = st.text_input("Enter the website you want to summarize", placeholder="Enter the website URL here")
submit_button = st.button("Analyse")

if submit_button:
    if not website.strip():
        st.error("Please enter a valid website before submitting.")
    else:
        with st.spinner("Fetching your answer..."):
            try:
                # Load documents from the website
                loader = WebBaseLoader(website)
                docs = loader.load()
                
                # Split documents into chunks
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                documents = splitter.split_documents(docs)
                
                # Create vector database with Ollama embeddings
                vectordb = FAISS.from_documents(documents,embeddings)
                retriever = vectordb.as_retriever()
                
                # Create retrieval chain
                
                retrieval_chain = create_retrieval_chain(retriever,document_chain)
                # Query and get the response
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
response=retrieval_chain.invoke({"input":"Summerize the website"})
st.write(response['answer'])  # Adjust according to the response structure                
