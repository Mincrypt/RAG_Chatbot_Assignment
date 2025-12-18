import streamlit as st
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

from logic import process_query, is_greeting
from retriever import retrieve_transactions

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="RAG Transaction Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Transaction RAG Chatbot")
st.caption("Professional AI Chatbot for Transactional Data")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    with open("transactions.json") as f:
        return json.load(f)

transactions = load_data()
df = pd.DataFrame(transactions)
df["date"] = pd.to_datetime(df["date"])

texts = [
    f"On {t['date']}, {t['customer']} purchased a {t['product']} for ₹{t['amount']}."
    for t in transactions
]

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()
embeddings = model.encode(texts)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions" not in st.session_state:
    st.session_state.questions = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.subheader("📘 Example Questions")

    examples = [
        "Show me Riya’s purchase history",
        "What is Amit’s total spending?",
        "Who bought the Mobile?",
        "how much laptop price by purchased history?",
        "how much Earbuds price by purchased history?",
        "What is the most purchased product?"
    ]

    for ex in examples:
        if st.button(ex):
            st.session_state.pending_query = ex

    st.divider()

    st.subheader("🧠 Question History")
    for q in st.session_state.questions:
        st.caption(f"- {q}")

    st.divider()

    st.subheader("📂 Open Sections")
    show_analytics = st.checkbox("📊 Analytics")
    show_data = st.checkbox("📄 Raw Data")

# -------------------------------------------------
# Chat Display
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# Input Validation
# -------------------------------------------------
def is_valid_query(query: str) -> bool:
    junk = ["ok", "okay", "hmm", "acha", "fine", "thanks"]
    q = query.lower().strip()
    return q not in junk and len(q.split()) >= 2

# -------------------------------------------------
# Chat Input
# -------------------------------------------------
query = st.chat_input("Ask about purchases, spending, or products...")

if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = ""

if query:
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )
    st.session_state.questions.append(query)

    if is_greeting(query):
        answer = "👋 Hi! Please ask a transaction-related question."
    elif not is_valid_query(query):
        answer = (
            "❗ Please ask a valid transaction question.\n\n"
            "Examples:\n"
            "- What is Amit’s total spending?\n"
            "- Amit ne kya kya kharida?"
        )
    else:
        answer = process_query(
            query, df, retrieve_transactions, model, embeddings, texts
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()

# -------------------------------------------------
# Optional Sections (Hidden by Default)
# -------------------------------------------------
if show_analytics:
    st.subheader("📊 Monthly Spend")
    monthly = df.groupby(
        df["date"].dt.to_period("M")
    )["amount"].sum()
    monthly.index = monthly.index.astype(str)
    st.bar_chart(monthly)

if show_data:
    st.subheader("📄 Transaction Data")
    st.dataframe(df)
