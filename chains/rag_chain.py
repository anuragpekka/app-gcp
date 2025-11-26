
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from prompts.prompts import get_prompt
from utils.pinecone_utils import get_retriever
import os
import configs.config as config

def build_chain(memory=None):
    llm = ChatGoogleGenerativeAI(
        model=config.MODEL,
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=config.LLM_TEMPERATURE
    )

    if memory is None:
        print(">>> Creating new memory for chain.")
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=get_retriever(),
        memory=memory,
        return_source_documents=False,
        combine_docs_chain_kwargs={"prompt": get_prompt()},
        chain_type="stuff",
        get_chat_history=lambda h: h
    )
