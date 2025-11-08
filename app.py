# app.py
from flask import Flask
import requests
import time
import random
from datetime import datetime
from threading import Thread

app = Flask(__name__)

class CloudBot:
    def __init__(self):
        self.BOT_TOKEN = "8224146014:AAGmsLTjTaMkkwZe46VlX2FVCPVBj6BIVh8"
        self.CHAT_ID = "597683397"
        self.signal_count = 0
        
        self.memecoins = [
            {'code': 'XMPIRE', 'price': 0.00085, 'vol': 12},
            {'code': 'PEPE', 'price': 0.0000012, 'vol': 15},
            {'code': 'BONK', 'price': 0.000012, 'vol': 14},
            {'code': 'WIF', 'price': 2.85, 'vol': 10},
            {'code': 'DOGE', 'price': 0.15, 'vol': 8},
        ]
    
    def send_telegram(self, text):
        try:
            url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
            data = {"chat_id": self.CHAT_ID, "text": text, "parse_mode": "HTML"}
            response = requests.post(url, data=data, timeout=10)
            return True
        except:
            return False
    
    def generate_market_data(self):
        data = []
        for coin in self.memecoins:
            change = random.uniform(-5, 20)
            new_price = coin['price'] * (1 + change/100)
            data.append({'code': coin['code'], 'price': new_price, 'change': change})
        return data
    
    def run_bot(self):
        print("🤖 ربات ابری فعال شد")
        self.send_telegram("☁️ <b>ربات ابری فعال شد!</b>")
        
        while True:
            try:
                self.signal_count += 1
                print(f"ارسال سیگنال #{self.signal_count}")
                
                # تولید داده
                market_data = self.generate_market_data()
                market_data.sort(key=lambda x: x['change'], reverse=True)
                
                # ساخت پیام
                message = f"<b>☁️ سیگنال #{self.signal_count}</b>\n"
                message += f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
                message += "─" * 25 + "\n\n"
                
                message += "<b>🚀 برترین‌ها:</b>\n"
                for i, coin in enumerate(market_data[:3], 1):
                    trend = "🟢" if coin['change'] > 0 else "🔴"
                    message += f"{i}. {coin['code']} {trend} {coin['change']:+.1f}%\n"
                
                message += f"\n📊 از طریق سرور ابری"
                
                # ارسال
                if self.send_telegram(message):
                    print("✅ ارسال موفق")
                else:
                    print("❌ ارسال ناموفق")
                
                # انتظار ۵ دقیقه
                time.sleep(300)
                
            except Exception as e:
                print(f"خطا: {e}")
                time.sleep(60)

# ایجاد و اجرای ربات
bot = CloudBot()
bot_thread = Thread(target=bot.run_bot)
bot_thread.daemon = True
bot_thread.start()

@app.route('/')
def home():
    return f"""
    <html>
        <head><title>ربات تلگرام</title><meta charset="utf-8"></head>
        <body style="font-family: Tahoma; text-align: center; padding: 50px;">
            <h1>🤖 ربات تلگرام ابری</h1>
            <p>ربات فعال است و کار می‌کند</p>
            <p>سیگنال‌های ارسالی: {bot.signal_count}</p>
            <p>آخرین بروزرسانی: {datetime.now().strftime('%H:%M:%S')}</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)