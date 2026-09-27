const trendCanvas = document.getElementById('trend-canvas');
const trendCtx = trendCanvas.getContext('2d');

function drawTrendChart(prices) {
  if (!prices || prices.length === 0) return;

  const width = trendCanvas.width;
  const height = trendCanvas.height;
  const padding = 30;
  const max = Math.max(...prices);
  const min = Math.min(...prices);
  const range = Math.max(1, max - min);

  trendCtx.clearRect(0, 0, width, height);
  trendCtx.fillStyle = '#091420';
  trendCtx.fillRect(0, 0, width, height);

  trendCtx.strokeStyle = 'rgba(255,255,255,0.2)';
  trendCtx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = padding + (i / 4) * (height - padding * 2);
    trendCtx.beginPath();
    trendCtx.moveTo(padding, y);
    trendCtx.lineTo(width - padding, y);
    trendCtx.stroke();
  }

  trendCtx.beginPath();
  prices.forEach((price, index) => {
    const x = padding + (index / (prices.length - 1)) * (width - padding * 2);
    const y = height - padding - ((price - min) / range) * (height - padding * 2);
    if (index === 0) {
      trendCtx.moveTo(x, y);
    } else {
      trendCtx.lineTo(x, y);
    }
  });

  trendCtx.strokeStyle = '#66d9ef';
  trendCtx.lineWidth = 3;
  trendCtx.stroke();

  trendCtx.fillStyle = '#ffffff';
  trendCtx.font = '12px Arial';
  trendCtx.fillText('Price', 20, 20);
}

async function updateMetrics(data) {
  document.getElementById('final-signal').textContent = data.final_signal;
  document.getElementById('confidence').textContent = data.confidence;
  document.getElementById('current-price').textContent = data.current_price;
  document.getElementById('change-percent').textContent = `${data.change_percent}%`;
  document.getElementById('tjr-signal').textContent = data.tjr_signal;
  document.getElementById('simpson-signal').textContent = data.simpson_signal;
  document.getElementById('trend-strength').textContent = data.trend_strength;
  document.getElementById('risk-level').textContent = data.risk_level;
  document.getElementById('stop-loss').textContent = data.stop_loss;
  document.getElementById('take-profit').textContent = data.take_profit;
  document.getElementById('simpson-area').textContent = data.simpson_area;
  document.getElementById('processed-points').textContent = data.processed_points;
  drawTrendChart(data.prices);
}

document.getElementById('upload-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const fileInput = document.getElementById('csv-file');
  const file = fileInput.files[0];

  if (!file) {
    const response = await fetch('/api/default');
    const data = await response.json();
    updateMetrics(data);
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/predict', {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();
  if (data.error) {
    alert(data.error);
    return;
  }

  updateMetrics(data);
});
