# TJR + Simpson Trade Predictor

A lightweight trading strategy dashboard that combines a TJR-style trend method with Simpson's rule integration for predictive trade signals.

## Features

- Upload CSV files with a `Close` price column
- Analyze trend direction using TJR-style logic
- Estimate cumulative trend strength with Simpson's rule
- Show BUY / SELL / HOLD signals with confidence and risk metrics
- Visualize price trend in a browser dashboard

## Running locally

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open: http://localhost:5000

## Strategy logic

- TJR component: evaluates short-term trend, momentum, and volatility
- Simpson component: integrates the price-change curve to estimate cumulative directional force
- Final signal: blends both signals into a BUY / SELL / HOLD recommendation

## File structure

- `app.py` — Flask application entry point
- `predictor.py` — trading logic and CSV parsing
- `templates/index.html` — dashboard UI
- `static/styles.css` — styling
- `static/app.js` — client-side interactions
- `data/sample_prices.csv` — default sample dataset

## Example forecast output

```
final_signal: BUY
confidence: 0.71
current_price: 118.24
change_percent: 17.42
risk_level: MEDIUM
```
