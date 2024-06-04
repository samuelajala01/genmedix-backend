from langchain_anthropic import ChatAnthropic

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

import streamlit as st
import os
import getpass
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = getpass.getpass()

## Prompt Template
model = ChatAnthropic(model="claude-3-sonnet-20240229")
parser = StrOutputParser()




messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

result = model.invoke(messages)

parser.invoke(result)
## Streamlit framework

# st.title("ChatBot")
# input_text=st.text_input("Search the topic you want")

