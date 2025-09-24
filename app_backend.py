from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# data file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROC_PATH = os.path.join(BASE_DIR, '..', 'dataset', 'processed', 'orders_cleaned.csv')
SAMPLE_PATH = os.path.join(BASE_DIR, '..', 'dataset', 'raw', 'orders_raw_sample.csv')

def load_data():
    path = PROC_PATH if os.path.exists(PROC_PATH) else SAMPLE_PATH
    df = pd.read_csv(path, parse_dates=['order_date'] if 'order_date' in pd.read_csv(path, nrows=0).columns else None)
    return df

@app.route('/api/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/api/metrics/monthly-revenue')
def monthly_revenue():
    df = load_data()
    if 'order_total' not in df.columns:
        df['order_total'] = df['price'] * df['quantity'] * (1 - df.get('discount',0))
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
    agg = df.groupby('month')['order_total'].sum().reset_index()
    agg['month'] = agg['month'].dt.strftime('%Y-%m')
    return jsonify(agg.to_dict(orient='records'))

@app.route('/api/metrics/top-products')
def top_products():
    df = load_data()
    df['order_total'] = df['price'] * df['quantity'] * (1 - df.get('discount',0))
    topn = int(request.args.get('n', 5))
    agg = df.groupby(['product_id','product_name'])['order_total'].sum().reset_index().sort_values('order_total', ascending=False).head(topn)
    return jsonify(agg.to_dict(orient='records'))

@app.route('/api/customers/rfm')
def rfm():
    df = load_data()
    df['order_date'] = pd.to_datetime(df['order_date'])
    snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('customer_id').agg({'order_date': lambda x: (snapshot_date - x.max()).days,
                                         'order_id': 'nunique',
                                         'order_total': lambda x: x.sum() if 'order_total' in df.columns else (df.loc[x.index,'price']*df.loc[x.index,'quantity']).sum()})
    rfm.columns = ['recency','frequency','monetary']
    # simple quantile-based segments
    rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1]).astype(int)
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4]).astype(int)
    rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4]).astype(int)
    rfm['rfm_segment'] = rfm['r_score'].map(str) + rfm['f_score'].map(str) + rfm['m_score'].map(str)
    rfm = rfm.reset_index().sort_values(['monetary'], ascending=False).head(20)
    return jsonify(rfm[['customer_id','recency','frequency','monetary','rfm_segment']].to_dict(orient='records'))

@app.route('/api/predict/forecast', methods=['POST'])
def forecast():
    # Accepts {"months": 3} and returns monthly revenue predictions for next `months`
    data = request.get_json() or {}
    months = int(data.get('months', 3))
    df = load_data()
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_total'] = df.get('order_total', df['price'] * df['quantity'] * (1 - df.get('discount',0)))
    monthly = df.set_index('order_date').resample('M')['order_total'].sum().reset_index()
    monthly['t'] = np.arange(len(monthly))
    X = monthly[['t']].values
    y = monthly['order_total'].values
    if len(X) < 3:
        # not enough data, repeat last value
        last = float(y[-1]) if len(y)>0 else 0.0
        preds = [last for _ in range(months)]
    else:
        model = LinearRegression().fit(X, y)
        t_future = np.arange(len(monthly), len(monthly)+months).reshape(-1,1)
        preds = model.predict(t_future).tolist()
    # format months
    last_month = monthly['order_date'].max()
    out = []
    for i, p in enumerate(preds):
        month = (last_month + pd.DateOffset(months=i+1)).strftime('%Y-%m')
        out.append({'month': month, 'prediction': float(round(p,2))})
    return jsonify(out)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
