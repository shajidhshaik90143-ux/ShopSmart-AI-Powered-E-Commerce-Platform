from datetime import datetime, timedelta
from collections import defaultdict
from database.models import Sale
from database.database import db
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_sales(days=7):
    sales = Sale.query.all()
    if not sales:
        return {"predicted_units": 0, "daily_predictions": []}

    start = min(s.sale_date.date() for s in sales)
    daily = defaultdict(int)
    for sale in sales:
        daily[(sale.sale_date.date() - start).days] += sale.quantity

    x = np.array(sorted(daily.keys()), dtype=float).reshape(-1, 1)
    y = np.array([daily[i] for i in sorted(daily.keys())], dtype=float)

    if len(x) < 2:
        base = int(y.mean())
        return {"predicted_units": base * days, "daily_predictions": [base] * days}

    model = LinearRegression().fit(x, y)
    future_x = np.arange(x.max() + 1, x.max() + days + 1).reshape(-1, 1)
    preds = np.maximum(0, model.predict(future_x)).round().astype(int).tolist()
    return {"predicted_units": int(sum(preds)), "daily_predictions": preds}
