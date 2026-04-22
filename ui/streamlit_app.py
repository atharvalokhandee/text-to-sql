import sys
import os

# Fix Python path so 'app' module is found from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from app.pipeline import text_to_sql_pipeline

st.set_page_config(page_title="Text-to-SQL", page_icon="🗄️", layout="centered")

st.title("🗄️ Text-to-SQL Engine")
st.caption("Ask questions about your database in plain English — powered by Groq + LLaMA 3.3")

question = st.text_input(
    "Your question",
    placeholder="Who are the top 3 customers by total order value?"
)

if st.button("Run Query", type="primary") and question:
    with st.spinner("Generating SQL with Groq..."):
        output = text_to_sql_pipeline(question, "data/sample.db")

    if output["error"]:
        st.error(output["error"])
    else:
        st.subheader("Generated SQL")
        st.code(output["sql"], language="sql")

        if output["result"] and output["result"]["rows"]:
            st.subheader("Result")
            df = pd.DataFrame(output["result"]["rows"], columns=output["result"]["columns"])
            st.dataframe(df, use_container_width=True)

        if output["explanation"]:
            st.subheader("Answer")
            st.success(output["explanation"])