import csv
import json
import os
from datetime import datetime

import numpy as np
from flask import Flask, jsonify, render_template, request

from predictor import analyze_prices, load_prices_from_csv

app = Flask(__name__)


@app.route('/')
def index():
    default_prices = load_prices_from_csv('data/sample_prices.csv')
    analysis = analyze_prices(default_prices)
    return render_template('index.html', analysis=analysis, title='TJR Simpson Trade Predictor')


@app.route('/api/default')
def default_api():
    prices = load_prices_from_csv('data/sample_prices.csv')
    return jsonify(analyze_prices(prices))


@app.route('/api/predict', methods=['POST'])
def predict_api():
    payload = request.get_json(silent=True) or {}
    prices = payload.get('prices')

    if isinstance(prices, list) and prices:
        clean_prices = [float(p) for p in prices]
        return jsonify(analyze_prices(clean_prices))

    uploaded_file = request.files.get('file')
    if uploaded_file and uploaded_file.filename:
        file_path = os.path.join('/tmp', uploaded_file.filename)
        uploaded_file.save(file_path)
        clean_prices = load_prices_from_csv(file_path)
        return jsonify(analyze_prices(clean_prices))

    return jsonify({"error": "No price data provided. Send JSON or upload a CSV file."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
