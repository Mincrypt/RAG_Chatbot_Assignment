from sklearn.metrics.pairwise import cosine_similarity

def retrieve_transactions(query, model, embeddings, texts, top_k=3):
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [texts[i] for i in top_indices]
