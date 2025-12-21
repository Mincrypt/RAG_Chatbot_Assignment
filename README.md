# 🤖 RAG-Powered Transaction Chatbot (Streamlit)

A **professional, production-style RAG chatbot** built using **Python + Streamlit** that answers questions from **structured transactional data**.

This project was designed with **senior-level architecture** in mind:

- Deterministic logic for structured data
- RAG used **only as a safe fallback**
- Clean chatbot UI
- Strict input validation
- English & Hindi language support

---

## 🎯 Assignment Objective

Build a **Retrieval-Augmented Generation (RAG) chatbot** that answers questions based on customer transactional data such as:

- Total customer spending
- Purchase history
- Product-wise buyers
- Product prices
- Most purchased product
- Monthly spending analytics

---

## 🧠 Key Design Decisions (Important)

> **Structured data ≠ Pure RAG**

- Customer & product questions are answered using **rule-based deterministic logic** (accurate & safe)
- RAG is used **only when the query is ambiguous**
- Prevents hallucinations and wrong answers

---

## 📁 Project Structure

```
rag_chatbot/
│
├── app.py              # Streamlit UI (Chatbot + Analytics toggle)
├── logic.py            # Core business logic + language detection
├── retriever.py        # Embedding & cosine similarity retriever
├── transactions.json   # Sample transactional dataset
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📊 Dataset (`transactions.json`)

```json
[
  {"id": 1, "customer": "Amit", "product": "Laptop", "amount": 55000, "date": "2024-01-12"},
  {"id": 2, "customer": "Amit", "product": "Mouse", "amount": 700, "date": "2024-02-15"},
  {"id": 3, "customer": "Riya", "product": "Mobile", "amount": 30000, "date": "2024-01-05"},
  {"id": 4, "customer": "Riya", "product": "Earbuds", "amount": 1500, "date": "2024-02-20"},
  {"id": 5, "customer": "Karan", "product": "Keyboard", "amount": 1200, "date": "2024-03-01"}
]
```

---

## 💬 Features

### ✅ Chatbot UI

- ChatGPT-style interface
- Question history stored (questions only)
- Clickable example questions
- Clean sidebar navigation

### ✅ Language Support

- **English question → English answer**
- **Hindi question → Hindi answer**
- No mixed-language responses

### ✅ Input Validation

- Ignores junk inputs (`ok`, `hmm`, `acha`, etc.)
- Friendly guidance for invalid queries

### ✅ Analytics

- Monthly spending bar chart
- Hidden by default (opened via sidebar toggle)

---

## 📘 Expected Example Interactions

### Example 1 (English)

**User:** Show me Riya’s purchase history

**Bot:**

```
Riya made the following purchases:
- Mobile for ₹30000 on 2024-01-05
- Earbuds for ₹1500 on 2024-02-20
```

### Example 2 (English)

**User:** What is Amit’s total spending?

**Bot:**

```
Amit spent a total of ₹55700
```

### Example 3 (Hindi)

**User:** amit ne kya kya kharida

**Bot:**

```
Amit ne yeh cheezein kharidi hain:
- Laptop ₹55000 (2024-01-12)
- Mouse ₹700 (2024-02-15)
```

---

## ▶️ How to Run the Project

### 1️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

The app will open at:

```
http://localhost:8501
```
### Server Streamlit App Link

```bash
https://tratbot.streamlit.app/
```
---

## 🧪 Sample Questions to Test

```
Amit total spending
```
Show me Riya’s purchase history
```
Mobile kis kis ne kharida?
```
Mobile kitne me kharida?
```
What is the most purchased product?
```

---

## 🏆 Why This Project Stands Out

✔ Senior-level architecture ✔ Clean separation of concerns ✔ Safe & explainable logic ✔ No hallucinations ✔ Assignment + interview ready

---

## 🚀 Possible Enhancements

- LLM-based intent classification
- FastAPI backend
- Database-backed chat history
- User authentication
- Multi-language expansion

---

## 👨‍💻 Author

Built as a **Entry-level AI/ML assignment project** using Python & Streamlit.

