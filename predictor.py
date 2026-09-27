import csv
import math
from typing import List, Dict, Any


def simpson_rule(values: List[float]) -> float:
    """
    Numerical integration of a price trend curve using Simpson's rule.
    This estimates the overall area under the signal curve to measure trend strength.
    """
    if len(values) < 3:
        return 0.0

    series = [float(v) for v in values]
    if len(series) % 2 == 0:
        series = series[:-1]

    width = 1.0
    n = len(series) - 1
    if n <= 0:
        return 0.0

    total = series[0] + series[-1]
    for i in range(1, n):
        total += (4 if i % 2 == 1 else 2) * series[i]
    return (width / 3.0) * total


def moving_average(values: List[float], window: int) -> List[float]:
    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        segment = values[start:i + 1]
        result.append(sum(segment) / len(segment))
    return result


def compute_tjr_signal(prices: List[float]) -> Dict[str, Any]:
    """
    TJR-style logic:
    - Trend: directional bias using short and long moving averages
    - Momentum: recent acceleration
    - Risk: volatility adjustment
    """
    if len(prices) < 5:
        return {
            'signal': 'HOLD',
            'confidence': 0.0,
            'trend_strength': 0.0,
            'risk_level': 'LOW'
        }

    recent = prices[-5:]
    short_ma = sum(recent[-3:]) / 3
    long_ma = sum(recent) / len(recent)
    momentum = prices[-1] - prices[-3]
    volatility = max(0.01, (max(recent) - min(recent)))

    trend_component = (short_ma - long_ma) / max(volatility, 0.001)
    momentum_component = momentum / max(volatility, 0.001)
    score = (trend_component + momentum_component) / 2.0

    if score > 0.4:
        signal = 'BUY'
    elif score < -0.4:
        signal = 'SELL'
    else:
        signal = 'HOLD'

    confidence = min(0.99, max(0.0, abs(score) / 3.0))
    risk_level = 'HIGH' if volatility > 10 else 'MEDIUM' if volatility > 5 else 'LOW'

    return {
        'signal': signal,
        'confidence': round(confidence, 3),
        'trend_strength': round(score, 3),
        'risk_level': risk_level
    }


def analyze_prices(prices: List[float]) -> Dict[str, Any]:
    if not prices:
        raise ValueError('Prices list is empty.')

    clean_prices = [float(p) for p in prices]

    # Normalize the curve to highlight trend shape
    baseline = clean_prices[0]
    curve = [p - baseline for p in clean_prices]

    # Simpson's rule gives area under the trend curve to estimate cumulative strength
    area = simpson_rule(curve)

    # TJR trade signal using trend and momentum logic
    tjr = compute_tjr_signal(clean_prices)

    # Blend the two methods for final decision
    area_signal = 'BUY' if area > 0 else 'SELL' if area < 0 else 'HOLD'
    blended_score = (tjr['trend_strength'] * 0.7) + ((area / max(abs(max(clean_prices)), 1.0)) * 10.0 * 0.3)

    if blended_score > 0.35:
        final_signal = 'BUY'
    elif blended_score < -0.35:
        final_signal = 'SELL'
    else:
        final_signal = 'HOLD'

    # Additional summary values
    current_price = clean_prices[-1]
    change_pct = ((current_price - clean_prices[0]) / clean_prices[0]) * 100 if clean_prices[0] else 0.0
    stop_loss = current_price * 0.97
    take_profit = current_price * 1.03

    return {
        'final_signal': final_signal,
        'tjr_signal': tjr['signal'],
        'simpson_signal': area_signal,
        'confidence': round(min(0.99, max(0.0, abs(blended_score) / 2.0 + tjr['confidence'] * 0.5)), 3),
        'trend_strength': round(blended_score, 3),
        'simpson_area': round(area, 3),
        'current_price': round(current_price, 3),
        'change_percent': round(change_pct, 3),
        'stop_loss': round(stop_loss, 3),
        'take_profit': round(take_profit, 3),
        'risk_level': tjr['risk_level'],
        'processed_points': len(clean_prices),
        'prices': clean_prices,
        'market_summary': {
            'trend': 'Bullish' if final_signal == 'BUY' else 'Bearish' if final_signal == 'SELL' else 'Neutral',
            'strategy': 'TJR + Simpson Hybrid Predictor',
            'note': 'Uses trend confirmation and numerical integration to estimate directional bias.'
        }
    }


def load_prices_from_csv(file_path: str) -> List[float]:
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if not reader.fieldnames:
            raise ValueError('CSV file is empty or missing headers.')

        preferred = None
        for candidate in ['Close', 'close', 'price', 'Price', 'adj close', 'Adj Close']:
            if candidate in reader.fieldnames:
                preferred = candidate
                break

        if preferred is None:
            raise ValueError('CSV must contain a Close or price column.')

        prices = []
        for row in reader:
            value = row.get(preferred)
            if value is not None and value != '':
                prices.append(float(value))

    if not prices:
        raise ValueError('No valid price values were found in the CSV file.')

    return prices


if __name__ == '__main__':
    sample_prices = [100, 102, 101, 105, 107, 110, 109, 112, 115, 117, 116, 120, 122]
    print(analyze_prices(sample_prices))
