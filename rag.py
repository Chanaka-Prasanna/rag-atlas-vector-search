from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import key_param
import streamlit as st

dbName = "book_mongodb_chunks"
collectionName = "chunked_data"
index = "vector_index"

vectorStore = MongoDBAtlasVectorSearch.from_connection_string(
    key_param.MONGODB_URI,
    dbName + "." + collectionName,
    GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=key_param.LLM_API_KEY
    ),
    index_name=index,
)

def query_data(query):
    retriever = vectorStore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3,
            "pre_filter": {"hasCode": {"$eq": False}},
            "score_threshold": 0.01
        },
    )
    template = """
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Do not answer the question if there is no given context.
        Do not answer the question if it is not related to the context.
        Do not give recommendations to anything other than Deep Learning.
        Context:
        {context}
        Question: {question}
        """
    custom_rag_prompt = PromptTemplate.from_template(template)

    retrieve = {
        "context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])),
        "question": RunnablePassthrough()
    }
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-8b",
        google_api_key=key_param.LLM_API_KEY,
        temperature=0
    )
    response_parser = StrOutputParser()
    rag_chain = (
            retrieve
            | custom_rag_prompt
            | llm
            | response_parser
    )
    answer = rag_chain.invoke(query)

    return answer

