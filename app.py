import streamlit as st
from rag import query_data

st.set_page_config(page_title='Ask About Deep Learning',layout='centered')

st.title("Learn Deep Learning with AI")

user_query = st.text_area("Enter Your Query")

if st.button("Submit"):
    if user_query.strip() != "":
        with st.spinner("Thinking..."):
            answer = query_data(user_query)
        st.success("Answer: ")
        st.write(answer)
    else:
        st.warning("Please enter a question")