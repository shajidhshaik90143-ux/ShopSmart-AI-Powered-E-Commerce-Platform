from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_products(product, products, limit=4):
    candidates = [p for p in products if p.id != product.id and p.is_active]
    if not candidates:
        return []

    docs = [
        f"{product.name} {product.category} {product.description}"
    ] + [
        f"{p.name} {p.category} {p.description}" for p in candidates
    ]
    matrix = TfidfVectorizer(stop_words="english").fit_transform(docs)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [p for p, _ in ranked[:limit]]
