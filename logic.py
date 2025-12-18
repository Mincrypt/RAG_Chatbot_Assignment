from collections import Counter

# -------------------------------
# Basic Validators
# -------------------------------
GREETINGS = ["hi", "hello", "hey", "hii"]

PURCHASE_KEYWORDS = [
    "kya kharida",
    "kya kya kharida",
    "kharida",
    "purchases",
    "purchase history",
    "bought"
]

TOTAL_KEYWORDS = ["total", "spending", "kharcha"]
AVERAGE_KEYWORDS = ["average"]
WHO_KEYWORDS = ["kis", "who"]
PRICE_KEYWORDS = ["kitne", "price", "amount"]

# -------------------------------
# Language Detection
# -------------------------------
def detect_language(query: str) -> str:
    """
    Default language: English
    Hindi only if strong Hindi markers are present
    """
    hindi_markers = [
        " kya ", " kharida", " kitne", " kis ",
        " ne ", " hai", " ka ", " ki ", " ke "
    ]

    q = " " + query.lower() + " "

    for marker in hindi_markers:
        if marker in q:
            return "hi"

    return "en"

# -------------------------------
# Greeting Detection
# -------------------------------
def is_greeting(query: str) -> bool:
    return query.lower().strip() in GREETINGS


# -------------------------------
# Main Logic Function
# -------------------------------
def process_query(query, df, retrieve_fn, model, embeddings, texts):
    lang = detect_language(query)
    query_lower = query.lower().strip()

    # -------------------------------
    # Detect customer
    # -------------------------------
    customer = None
    for c in df["customer"].unique():
        if c.lower() in query_lower:
            customer = c
            break

    # -------------------------------
    # Detect product
    # -------------------------------
    product = None
    for p in df["product"].unique():
        if p.lower() in query_lower:
            product = p
            break

    # =====================================================
    # PRODUCT-BASED QUESTIONS
    # =====================================================
    if product:
        pdf = df[df["product"] == product]

        # Who bought the product
        if any(k in query_lower for k in WHO_KEYWORDS):
            buyers = ", ".join(pdf["customer"].unique())
            return f"🛒 **{product} kis kis ne kharida:** {buyers}"

        # Product price details
        if any(k in query_lower for k in PRICE_KEYWORDS):
            response = f"🧾 **{product} purchase details:**\n"
            for _, r in pdf.iterrows():
                response += (
                    f"- {r['customer']} ne ₹{r['amount']} me "
                    f"{r['date'].date()} ko kharida\n"
                )
            return response

    # =====================================================
    # CUSTOMER-BASED QUESTIONS (STRICT, NO RAG)
    # =====================================================
    if customer:
        cdf = df[df["customer"] == customer]

        # Total spending
        if any(k in query_lower for k in TOTAL_KEYWORDS):
            return f"💰 **{customer} ka total spending:** ₹{cdf['amount'].sum()}"

        # Purchase history (IMPORTANT FIX)
        if any(k in query_lower for k in PURCHASE_KEYWORDS):
            if lang == "hi":
                response = f"📜 **{customer} ne yeh cheezein kharidi hain:**\n"
            else:
                response = f"📜 **{customer} made the following purchases:**\n"

            # response = f"📜 **{customer} ne yeh cheezein kharidi hain:**\n"
            for _, r in cdf.iterrows():
                response += (
                    f"- {r['product']} ₹{r['amount']} "
                    f"({r['date'].date()})\n"
                )
            return response

        # Average order value
        if any(k in query_lower for k in AVERAGE_KEYWORDS):
            return f"📊 **{customer} ka average order value:** ₹{cdf['amount'].mean():.2f}"

        # Customer mentioned but intent unclear
        return (
            f"❓ **{customer} ke liye query clear nahi hai.**\n"
            "Try asking: total spending, purchase history, or average order."
        )

    # =====================================================
    # GLOBAL QUESTIONS
    # =====================================================
    if "most" in query_lower:
        product = Counter(df["product"]).most_common(1)[0][0]
        return f"🔥 **Sabse zyada kharida gaya product:** {product}"

    if "average order" in query_lower:
        return f"📊 **Overall average order value:** ₹{df['amount'].mean():.2f}"

    # =====================================================
    # FINAL FALLBACK → RAG (ONLY IF NOTHING MATCHED)
    # =====================================================
    retrieved = retrieve_fn(query, model, embeddings, texts)
    return "📌 **Relevant Information:**\n" + "\n".join(retrieved)
