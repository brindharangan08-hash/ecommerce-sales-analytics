import argparse
import pandas as pd
import os

def run_etl(input_path, output_path):
    df = pd.read_csv(input_path)
    # basic cleaning
    df = df.drop_duplicates(subset=['order_id'])
    # parse date
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    df['order_total'] = df['price'] * df['quantity'] * (1 - df['discount'])
    # simple feature engineering
    df['order_month'] = df['order_date'].dt.to_period('M').astype(str)
    df.to_csv(output_path, index=False)
    print(f"Wrote cleaned data to {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='dataset/raw/orders_raw_sample.csv')
    parser.add_argument('--output', default='dataset/processed/orders_cleaned.csv')
    args = parser.parse_args()
    run_etl(args.input, args.output)
