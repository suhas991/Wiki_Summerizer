import streamlit as st
import os
from langchain.agents import create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain import hub
from langchain_community.chat_models import ChatOllama
# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Wikipedia API Wrapper
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# Tools list
tools = [wiki]

# Initialize LLM model
# llm = ChatGroq(
#     api_key=groq_api_key,
#     model_name="llama-3.1-8b-instant",
#     temperature=0.7,
# )
llm=ChatOllama(model="llama2")

# Initialize prompt
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Page configuration
st.set_page_config(page_title="Wikipedia Summarizer Chatbot", page_icon="🌐", layout="wide")

# App header
st.title("🌐 Wikipedia Summarizer Chatbot")
st.markdown("""
This chatbot leverages the power of LLM to provide concise summaries of Wikipedia articles. 
Simply enter a question, and it will fetch relevant information for you!
""")

# Input section
col1, col2 = st.columns([4, 1])  # Adjust the column width ratio as needed
with col1:
    user_input = st.text_input("Enter your query here:", placeholder="What do you want to know about?")
with col2:
    submit_button = st.button("Submit")

# Display output
if submit_button:
    if not user_input.strip():
        st.error("Please enter a valid query before submitting.")
    else:
        with st.spinner("Fetching your answer..."):
            try:
                answer = agent_executor.invoke({"input": user_input})
                st.success("Here's the summary:")
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; background-color:rgb(255, 255, 255); color:black;">
                    {answer['output']}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("<center>👩‍💻 Developed by Suhas N H | Powered by LangChain</center>", unsafe_allow_html=True)
