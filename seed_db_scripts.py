import pandas as pd
import sqlite3, os

src = os.path.join('dataset','processed','orders_cleaned.csv')
if not os.path.exists(src):
    print('Run scripts/etl.py first to create processed data')
    raise SystemExit(1)
df = pd.read_csv(src)
conn = sqlite3.connect('deployment/sample_db.sqlite')
df.to_sql('orders', conn, if_exists='replace', index=False)
print('Seeded deployment/sample_db.sqlite with orders table')
conn.close()
