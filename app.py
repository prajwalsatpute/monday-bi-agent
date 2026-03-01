import streamlit as st
from agent import run_query

st.set_page_config(page_title="Monday BI Agent")

st.title("📊 Monday Business Intelligence Agent")

question = st.text_input("Ask a business question")

if question:
    answer, trace = run_query(question)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Agent Trace")
    for t in trace:
        st.write("•", t)