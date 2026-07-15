import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Kukuha ng Live Prices mula sa mismong OKX API (Libre at Public)
def get_okx_data():
    try:
        # Kumukuha ng market ticker para sa BTC, ETH, at SOL mula sa OKX V5 API
        tickers = ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']
        market_data = {}
        for ticker in tickers:
            url = f"https://www.okx.com/api/v5/market/ticker?instId={ticker}"
            res = requests.get(url).json()
            if res.get('code') == '0' and len(res.get('data', [])) > 0:
                market_data[ticker] = {
                    'price': float(res['data'][0]['last']),
                    'high': float(res['data'][0]['high24h']),
                    'low': float(res['data'][0]['low24h'])
                }
        return market_data
    except Exception as e:
        print("API Error:", e)
        return None

# Simpleng Local AI Analytics Engine (Simulated AI Agent para sa OKX.AI)
def okx_ai_analyze(coin, budget, data):
    if not data or f"{coin}-USDT" not in data:
        return "Paumanhin, hindi ko makuha ang live market feed mula sa OKX sa kasalukuyan."
    
    coin_data = data[f"{coin}-USDT"]
    current_price = coin_data['price']
    high_24h = coin_data['high']
    low_24h = coin_data['low']
    
    # Kalkulahin kung ilang coins ang mabibili ng budget ng user
    amount_to_buy = float(budget) / current_price
    
    # Rule-Based AI Market Insight
    # Titingnan ng AI kung malapit ba ang presyo sa 24h High o 24h Low
    price_range = high_24h - low_24h
    if price_range > 0:
        position_pct = ((current_price - low_24h) / price_range) * 100
    else:
        position_pct = 50

    if position_pct > 80:
        market_sentiment = "🔥 OVERBOUGHT (Masyadong Mataas): Malapit ang presyo sa 24-hour high. Mag-ingat sa pagbili ng marami ngayon, baka magkaroon ng correction."
    elif position_pct < 20:
        market_sentiment = "📉 OVERSOLD (Magandang Oportunidad): Malapit ang presyo sa 24-hour low nito. Magandang simulan ang Dollar-Cost Averaging (DCA)."
    else:
        market_sentiment = "⚖️ NEUTRAL: Matatag ang takbo ng merkado sa kasalukuyan."

    analysis = (
        f"🤖 **OKX.AI GENESIS ANALYTICS REPORT**\n\n"
        f"• **Alokasyon:** Gamit ang iyong ${float(budget):,.2f} USDT, makakabili ka ng humigit-kumulang na **{amount_to_buy:.6f} {coin}**.\n"
        f"• **Kasalukuyang Presyo (OKX):** ${current_price:,.2f} USDT\n"
        f"• **24h Range:** High: ${high_24h:,.2f} | Low: ${low_24h:,.2f}\n\n"
        f"💡 **AI Rekomendasyon:** {market_sentiment}\n"
        f"ℹ️ *Note: Ang pagsusuring ito ay batay sa real-time technical structures ng OKX exchange.*"
    )
    return analysis

@app.route('/', methods=['GET', 'POST'])
def home():
    prices = get_okx_data()
    advice = ""
    
    if request.method == 'POST':
        budget = request.form.get('budget', 0)
        crypto = request.form.get('crypto', 'BTC')
        if budget:
            advice = okx_ai_analyze(crypto, budget, prices)
            
    return render_template('index.html', prices=prices, advice=advice)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

