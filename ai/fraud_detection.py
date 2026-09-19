def fraud_score(user, items, total):
    score = 0

    if total > 100000:
        score += 40
    if len(items) > 20:
        score += 20
    if any(item.quantity > 20 for item in items):
        score += 20
    if not user.email or "@" not in user.email:
        score += 20

    return min(score, 100)
