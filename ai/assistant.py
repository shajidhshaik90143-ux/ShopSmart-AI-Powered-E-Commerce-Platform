def assistant_response(message, products=None):
    text = message.lower().strip()
    products = products or []

    if any(x in text for x in ["hello", "hi", "hey"]):
        return "Hello! I can help you search products, understand orders, or find shopping suggestions."

    if "order" in text:
        return "You can view your order history from the Orders page after logging in."

    if "return" in text:
        return "For this demo, return requests should be handled through the store support process."

    if "cheap" in text or "budget" in text:
        cheap = sorted(products, key=lambda p: p.price)[:3]
        if cheap:
            return "Budget suggestions: " + ", ".join(f"{p.name} (₹{p.price:.0f})" for p in cheap)

    if "laptop" in text or "computer" in text:
        matches = [p for p in products if p.category.lower() in {"computers", "electronics"}][:4]
        if matches:
            return "Computer-related products: " + ", ".join(p.name for p in matches)

    return "Try asking me about products, budget items, orders, returns, laptops, or recommendations."
