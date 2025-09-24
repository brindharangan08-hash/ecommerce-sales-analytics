async function fetchJSON(url, opts){ 
  const res = await fetch(url, opts);
  return res.json();
}

async function drawRevenue(){
  const data = await fetchJSON('/api/metrics/monthly-revenue');
  const labels = data.map(d=>d.month);
  const values = data.map(d=>d.order_total || d.order_total === 0 ? d.order_total : d[Object.keys(d).find(k=>k!='month')]);
  const ctx = document.getElementById('revenueChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Monthly Revenue',
        data: values,
        fill: false,
        tension: 0.2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true }
      }
    }
  });
}

async function showTopProducts(){
  const data = await fetchJSON('/api/metrics/top-products?n=5');
  const ul = document.getElementById('topProducts');
  ul.innerHTML = '';
  data.forEach(p=>{
    const li = document.createElement('li');
    li.textContent = `${p.product_name} — ₹${(p.order_total||p.order_total===0?Number(p.order_total).toFixed(2):'0.00')}`;
    ul.appendChild(li);
  });
}

async function showRFM(){
  const data = await fetchJSON('/api/customers/rfm');
  const div = document.getElementById('rfmList');
  div.innerHTML = '<small>Top 10 by monetary</small>';
  const table = document.createElement('table');
  table.className = 'table table-sm';
  const thead = document.createElement('thead');
  thead.innerHTML = '<tr><th>Customer</th><th>Recency</th><th>Frequency</th><th>Monetary</th></tr>';
  table.appendChild(thead);
  const tbody = document.createElement('tbody');
  data.slice(0,10).forEach(r=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${r.customer_id}</td><td>${r.recency}</td><td>${r.frequency}</td><td>₹${Number(r.monetary).toFixed(2)}</td>`;
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  div.appendChild(table);
}

// run on load
drawRevenue();
showTopProducts();
showRFM();
