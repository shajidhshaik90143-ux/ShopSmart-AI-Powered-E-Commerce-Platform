def smart_search(products, query):
    query = query.lower().strip()
    if not query:
        return products

    tokens = set(query.split())
    scored = []
    for product in products:
        text = f"{product.name} {product.category} {product.description}".lower()
        score = sum(2 if token in product.name.lower() else 1 for token in tokens if token in text)
        if score:
            scored.append((score, product))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored]
