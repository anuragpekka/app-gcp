import os
import configs.config as config
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL, google_api_key=os.environ.get('GOOGLE_API_KEY'))
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=config.INDEX_NAME,
        embedding=embeddings
    )
    return vectorstore.as_retriever(search_type=config.VECTOR_STORE_SEARCH_TYPE, search_kwargs={"k": config.NUM_DOCS})
