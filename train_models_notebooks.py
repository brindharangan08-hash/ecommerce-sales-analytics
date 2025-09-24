import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

proc = os.path.join('dataset','processed','orders_cleaned.csv')
if not os.path.exists(proc):
    print('Processed data not found. Please run scripts/etl.py first.')
    raise SystemExit(1)
df = pd.read_csv(proc, parse_dates=['order_date'])
df['order_total'] = df['order_total']
monthly = df.set_index('order_date').resample('M')['order_total'].sum().reset_index()
monthly['t'] = np.arange(len(monthly))
X = monthly[['t']].values
y = monthly['order_total'].values
if len(X) >= 3:
    model = LinearRegression().fit(X,y)
    os.makedirs('backend/models', exist_ok=True)
    joblib.dump(model, 'backend/models/forecast_model.joblib')
    print('Saved forecast model to backend/models/forecast_model.joblib')
else:
    print('Not enough data to train a model.')
