# app.py
import streamlit as st
from agent import SupportAgent

st.title("AI Support Assistant 🤖")
st.write("Ask any question and I will do my best to help.")

agent = SupportAgent()

query = st.text_input("Your question:")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Thinking..."):
            result = agent.ask(query)

        st.subheader("Answer")
        st.write(result["answer"])

        if result["snippets"]:
            st.subheader("Relevant FAQ Snippets")
            for snip in result["snippets"]:
                with st.expander("Snippet"):
                    st.write(snip)
    else:
        st.warning("Please enter a question.")