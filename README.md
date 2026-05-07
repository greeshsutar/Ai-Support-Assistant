# AI-Support-Assistent- 
A lightweight RAG-based (Retrieval Augmented Generation) Support Assistant built using **Groq LLM + ChromaDB + LangChain + Streamlit**.

The agent answers user queries using your FAQ data, ensuring accurate and context-based responses.

---

## 📌 1. Overview  

This AI Support Assistant helps users get automated answers to common support questions.  
It uses:

- A **vector database (ChromaDB)** to store & retrieve FAQ data  
- **SentenceTransformer embeddings** to match similar questions  
- **Groq LLM (llama-3.3-70b-versatile)** for fast, accurate responses  
- **Streamlit** for the UI  

This makes the tool behave like a mini customer support agent.

---

## 🚀 2. Features  

### ✔ **Context-aware answers**  
Uses RAG to answer strictly from provided FAQ data.

### ✔ **Fast inference with Groq**  
Groq’s hosted LLM provides extremely high speed and low latency.

### ✔ **Expandable FAQ database**  
Simply update the `faqs.txt` file to add new knowledge.

### ✔ **Clean UI using Streamlit**  
Easy for users to interact and test the assistant.

---

## ⚠️ 3. Limitations  

- Cannot answer questions **outside FAQ context**.  
- No authentication (anyone can access if deployed publicly).  
- Basic UI (no chat history).  
- Not suitable for *very large* knowledgebases without optimization.  

---

## 🧠 4. Architecture Diagram  

                     ┌──────────────────────────┐
                     │        User (UI)         │
                     │  Streamlit Frontend      │
                     └─────────────▲────────────┘
                                   │  User Query
                                   │
                     ┌─────────────┴────────────┐
                     │      SupportAgent         │
                     │ (Controls full pipeline)  │
                     └─────────────▲────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                │                  │                  │
                ▼                  │                  ▼
      ┌──────────────────┐         │        ┌──────────────────────┐
      │  ChromaDB Vector  │         │        │ SentenceTransformer │
      │     Database      │◄────────┘        │  Embedding Model     │
      └──────────────────┘   Similarity      └──────────────────────┘
            ▲   │              Search                ▲
            │   │                                    │
            │   └───────────────┬────────────────────┘
            │                   │
            │       Relevant FAQ Snippets
            │                   │
            ▼                   │
       ┌──────────────────────────────────────────────┐
       │       Groq LLM (llama-3.3-70b-versatile)     │
       │  Generates the final answer using context     │
       └──────────────────────────────────────────────┘
                                   │
                                   ▼
                      ┌──────────────────────────┐
                      │     Final Answer         │
                      │  Shown in Streamlit UI   │
                      └──────────────────────────┘

🛠️ 5. Tech Stack & Models Used
🔹 Backend & AI

Groq LLM: llama-3.3-70b-versatile

SentenceTransformer: all-MiniLM-L6-v2 for embeddings

LangChain for text splitting & retrieval pipeline

ChromaDB for vector storage

Python 3.10

🔹 Frontend

Streamlit (interactive user interface)

🔹 Other Tools

dotenv for API key management

pandas for handling text data

GitHub for version control

Streamlit Cloud for deployment

⚙️ 6. Setup & Installation Instructions
# 1. Clone repository
git clone https://github.com/<your-username>/AI-Support-Assiistent-.git
cd AI-Support-Assiistent-

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # on Windows
# OR
source venv/bin/activate  # Mac/Linux

# 3. Install required packages
pip install -r requirements.txt

# 4. Create .env file
touch .env

# Add inside .env:
GROQ_API_KEY=your_api_key_here

# 5. Run the app
streamlit run app.py

7. Project Structure (Required)
AI-Support-Assiistent-/
│
├── app.py                     # Streamlit UI
├── agent.py                   # Main support agent logic
├── retriever.py               # RAG system (Chroma + Embeddings)
├── list_models.py             # Utility to list Groq models
│
├── data/
│   └── faqs.txt               # FAQ knowledge base
│
├── requirements.txt           # Python dependencies
├── .env.example               # Example env file
├── .gitignore
└── README.md

8. Potential Improvements
Future Enhancements

Add chat history for multi-turn conversations

Add authentication for restricted access

Add admin panel to upload FAQs dynamically

Use bigger embedding models for better retrieval

Add feedback system (thumbs up/down)

Improve UI design with animations + branding

Deploy using Docker or HuggingFace Spaces


9. Demo Link
🔗 Live Demo:
https://<your-streamlit-cloud-url>


