📊 E-commerce Sales Analytics Web Application

An end-to-end full stack + data analytics project that demonstrates skills in data engineering, analytics, machine learning, and full stack web development.

🚀 Project Overview

This project simulates a real-world e-commerce analytics platform:

ETL pipeline cleans and transforms raw order data.

Data analysis & ML models generate KPIs, customer segments (RFM), and revenue forecasts.

REST APIs (Flask) serve metrics and predictions.

Interactive dashboard (HTML, CSS, JS, Chart.js) visualizes insights for business users.

Deployment ready with Docker, GitHub Actions CI, and Heroku.

🛠️ Tech Stack

Frontend: HTML5, CSS3, Bootstrap, JavaScript, Chart.js

Backend: Python, Flask, REST APIs, SQLAlchemy

Data: Pandas, NumPy, scikit-learn, PostgreSQL/MySQL (demo uses CSV)

Visualization: Chart.js, Plotly (optional Power BI/Tableau export)

DevOps: Docker, GitHub Actions CI, Heroku deployment

📂 Repository Structure
ecommerce-sales-analytics/
│── backend/        # Flask app, API routes
│── frontend/       # Dashboard (HTML, CSS, JS)
│── dataset/        # Sample raw + processed data
│── scripts/        # ETL + DB seed scripts
│── notebooks/      # Data analysis & modeling
│── deployment/     # Docker & Heroku configs
│── tests/          # API tests
│── docs/           # Screenshots & documentation
│── README.md

📸 Screenshots

### Dashboard – Monthly Revenue Trend  
![Revenue](docs/screenshots/dashboard_revenue.png)  

### Dashboard – Top Products by Sales  
![Top Products](docs/screenshots/dashboard_top_products.png)  

### Dashboard – Customer Segmentation (RFM)  
![Segments](docs/screenshots/dashboard_segments.png)  


⚙️ How to Run Locally
1. Clone the repo
git clone https://github.com/brindharangan08-hash/ecommerce-sales-analytics.git
cd ecommerce-sales-analytics

2. Run ETL (prepare cleaned dataset)
python scripts/etl.py --input dataset/raw/orders_raw_sample.csv --output dataset/processed/orders_cleaned.csv

3. Start Flask backend
cd backend
pip install -r requirements.txt
flask --app app.py run


API runs at → http://localhost:5000

4. Open frontend dashboard

Open frontend/index.html in your browser → dashboard fetches data from Flask APIs.

🔑 Example API Endpoints

GET /api/health → API health check

GET /api/metrics/monthly-revenue → monthly revenue trend

GET /api/metrics/top-products?n=5 → top products

GET /api/customers/rfm → customer segmentation (RFM)

POST /api/predict/forecast → revenue forecast

📊 Data Pipeline & Modeling

ETL: Clean raw orders dataset (remove duplicates, fix dates, calculate totals).

Feature Engineering: Create features (order totals, monthly aggregates, RFM).

Segmentation: Quantile-based RFM scoring → high, medium, low value customers.

Forecasting: Linear regression on monthly sales → predicts revenue for upcoming months.

Serving: Models persisted with joblib and loaded into Flask endpoints.

🧪 Testing & CI/CD

Unit tests for API endpoints (tests/).

GitHub Actions workflow runs tests automatically on push.

Dockerfile + Heroku Procfile included for deployment.


📄 License

MIT License © Brindha P
