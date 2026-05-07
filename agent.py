# agent.py
import os
from dotenv import load_dotenv
from groq import Groq
from retriever import FAQRetriever

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class SupportAgent:
    def __init__(self):
        self.retriever = FAQRetriever()

    def _is_relevant(self, query: str, snippets: list) -> bool:
        # Check if any snippet has meaningful word overlap with the query
        import re
        q_tokens = set(re.findall(r"\w+", query.lower()))
        for snippet in snippets:
            s_tokens = set(re.findall(r"\w+", snippet.lower()))
            overlap = len(q_tokens & s_tokens)
            if overlap >= 2:
                return True
        return False

    def ask(self, query: str):
        snippets = self.retriever.get_relevant(query)
        context = "\n\n".join(snippets)
        faq_relevant = self._is_relevant(query, snippets)

        if faq_relevant:
            prompt = f"""
You are a support assistant.
Answer using the context below.
If the context does not contain the answer, use your own knowledge to help.

Context:
{context}

Question:
{query}
"""
        else:
            prompt = f"""
You are a helpful general assistant.
Answer the following question using your own knowledge clearly and helpfully.

Question:
{query}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )

        return {
            "answer": response.choices[0].message.content,
            "snippets": snippets if faq_relevant else [],
        }