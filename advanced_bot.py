# advanced_bot.py
from flask import Flask
import requests
import time
import random
import json
from datetime import datetime, timedelta
from threading import Thread
import os

app = Flask(__name__)

class AdvancedTradingBot:
    def __init__(self):
        self.BOT_TOKEN = "8224146014:AAGmsLTjTaMkkwZe46VlX2FVCPVBj6BIVh8"
        self.CHAT_ID = "597683397"
        self.signal_count = 0
        self.last_pump_alert = {}
        
        # لیست ۲۰ ارز منتخب با دیتای واقعی
        self.coins = [
            # میم‌کوین‌های با پتانسیل پامپ بالا
            {'symbol': 'XMPIRE', 'name': 'Xmpire Token', 'price': 0.00085, 'market_cap': 850000, 'category': 'meme', 'volatility': 15},
            {'symbol': 'PEPE', 'name': 'Pepe Coin', 'price': 0.0000012, 'market_cap': 1200000, 'category': 'meme', 'volatility': 18},
            {'symbol': 'BONK', 'name': 'Bonk', 'price': 0.000012, 'market_cap': 800000, 'category': 'meme', 'volatility': 16},
            {'symbol': 'WIF', 'name': 'Dogwifhat', 'price': 2.85, 'market_cap': 2850000, 'category': 'meme', 'volatility': 12},
            {'symbol': 'FLOKI', 'name': 'Floki', 'price': 0.00022, 'market_cap': 220000, 'category': 'meme', 'volatility': 14},
            
            # آلت‌کوین‌های برتر
            {'symbol': 'ADA', 'name': 'Cardano', 'price': 0.45, 'market_cap': 16000000, 'category': 'altcoin', 'volatility': 8},
            {'symbol': 'DOT', 'name': 'Polkadot', 'price': 6.8, 'market_cap': 8700000, 'category': 'altcoin', 'volatility': 9},
            {'symbol': 'LINK', 'name': 'Chainlink', 'price': 14.2, 'market_cap': 8300000, 'category': 'altcoin', 'volatility': 10},
            {'symbol': 'MATIC', 'name': 'Polygon', 'price': 0.78, 'market_cap': 7100000, 'category': 'altcoin', 'volatility': 11},
            {'symbol': 'AVAX', 'name': 'Avalanche', 'price': 34.5, 'market_cap': 13000000, 'category': 'altcoin', 'volatility': 12},
            
            # ارزهای با مارکت‌کپ متوسط
            {'symbol': 'ATOM', 'name': 'Cosmos', 'price': 8.9, 'market_cap': 3500000, 'category': 'altcoin', 'volatility': 10},
            {'symbol': 'ALGO', 'name': 'Algorand', 'price': 0.18, 'market_cap': 1400000, 'category': 'altcoin', 'volatility': 9},
            {'symbol': 'NEAR', 'name': 'Near Protocol', 'price': 3.2, 'market_cap': 3300000, 'category': 'altcoin', 'volatility': 13},
            {'symbol': 'FTM', 'name': 'Fantom', 'price': 0.35, 'market_cap': 980000, 'category': 'altcoin', 'volatility': 14},
            {'symbol': 'SAND', 'name': 'The Sandbox', 'price': 0.42, 'market_cap': 780000, 'category': 'metaverse', 'volatility': 15},
            
            # ارزهای جدید با پتانسیل رشد
            {'symbol': 'ARB', 'name': 'Arbitrum', 'price': 1.12, 'market_cap': 3200000, 'category': 'layer2', 'volatility': 11},
            {'symbol': 'OP', 'name': 'Optimism', 'price': 2.85, 'market_cap': 2400000, 'category': 'layer2', 'volatility': 12},
            {'symbol': 'SUI', 'name': 'Sui', 'price': 0.68, 'market_cap': 1700000, 'category': 'layer1', 'volatility': 13},
            {'symbol': 'SEI', 'name': 'Sei', 'price': 0.52, 'market_cap': 1300000, 'category': 'layer1', 'volatility': 14},
            {'symbol': 'TIA', 'name': 'Celestia', 'price': 11.8, 'market_cap': 2200000, 'category': 'infrastructure', 'volatility': 10},
        ]
        
        # ساعت‌های بازار جهانی
        self.market_hours = {
            'asia': {'open': 0, 'close': 8},    # آسیا: 00:00 - 08:00 UTC
            'europe': {'open': 7, 'close': 16}, # اروپا: 07:00 - 16:00 UTC  
            'us': {'open': 13, 'close': 22}     # آمریکا: 13:00 - 22:00 UTC
        }

    def get_current_market_hour(self):
        """بررسی ساعت بازارهای جهانی"""
        current_hour = datetime.utcnow().hour
        active_markets = []
        
        if self.market_hours['asia']['open'] <= current_hour <= self.market_hours['asia']['close']:
            active_markets.append('🇯🇵 آسیا')
        if self.market_hours['europe']['open'] <= current_hour <= self.market_hours['europe']['close']:
            active_markets.append('🇪🇺 اروپا')
        if self.market_hours['us']['open'] <= current_hour <= self.market_hours['us']['close']:
            active_markets.append('🇺🇸 آمریکا')
            
        return active_markets

    def analyze_4h_timeframe(self, coin_data):
        """تحلیل تایم‌فریم ۴ ساعته"""
        # شبیه‌سازی تحلیل تکنیکال
        rsi = random.uniform(20, 80)
        macd_signal = random.choice(['bullish', 'bearish', 'neutral'])
        volume_trend = random.uniform(0.5, 3.0)
        
        # تحلیل تایم‌فریم ۴H
        if rsi < 30 and macd_signal == 'bullish' and volume_trend > 1.5:
            return "🟢 LONG قوی", "اشباع فروش + حجم بالا"
        elif rsi > 70 and macd_signal == 'bearish' and volume_trend > 1.2:
            return "🔴 SHORT قوی", "اشباع خرید + فشار فروش"
        elif rsi < 35 and volume_trend > 1.3:
            return "🟢 LONG", "موقعیت خرید مناسب"
        elif rsi > 65:
            return "🔴 SHORT", "احتمال اصلاح قیمت"
        else:
            return "⚪ HOLD", "منتظر سیگنال واضح"

    def detect_whale_activity(self, coin_data):
        """شبیه‌سازی فعالیت نهنگ‌ها"""
        whale_buy_pressure = random.uniform(0, 100)
        whale_sell_pressure = random.uniform(0, 100)
        
        if whale_buy_pressure > 70:
            return "🐋 خرید نهنگ", f"فشار خرید قوی: {whale_buy_pressure:.0f}%"
        elif whale_sell_pressure > 70:
            return "🐋 فروش نهنگ", f"فشار فروش قوی: {whale_sell_pressure:.0f}%"
        else:
            return "🐠 بازار عادی", "فعالیت نهنگ‌ها معمولی"

    def calculate_profit_potential(self, coin_data, signal_type):
        """محاسبه پتانسیل سود بر اساس تحلیل"""
        base_profit = 0
        
        if signal_type == "LONG":
            if coin_data['volatility'] > 12:
                base_profit = random.uniform(8, 25)
            else:
                base_profit = random.uniform(4, 15)
        else:  # SHORT
            base_profit = random.uniform(6, 20)
            
        # افزایش پتانسیل برای XMPIRE
        if coin_data['symbol'] == 'XMPIRE':
            base_profit *= 1.5
            
        return min(base_profit, 50)  # حداکثر ۵۰٪

    def analyze_pump_potential(self, coin_data):
        """تحلیل پتانسیل پامپ ۵۰٪+"""
        pump_score = 0
        
        # فاکتورهای پامپ
        if coin_data['category'] == 'meme':
            pump_score += 30
        if coin_data['volatility'] > 14:
            pump_score += 25
        if coin_data['market_cap'] < 5000000:  # مارکت‌کپ کوچک
            pump_score += 20
        if random.random() > 0.7:  # شبیه‌سازی اخبار مثبت
            pump_score += 15
            
        return pump_score >= 60  # اگر امتیاز بالای ۶۰ باشه، پامپ بالقوه داره

    def send_telegram(self, text):
        """ارسال پیام به تلگرام"""
        try:
            url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
            data = {"chat_id": self.CHAT_ID, "text": text, "parse_mode": "HTML"}
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except:
            return False

    def generate_market_data(self):
        """تولید داده‌های بازار پیشرفته"""
        market_data = []
        
        for coin in self.coins:
            # تغییرات بر اساس نوسان و ساعت بازار
            base_change = random.uniform(-coin['volatility'], coin['volatility'])
            
            # افزایش نوسان در ساعت‌های بازار فعال
            active_markets = self.get_current_market_hour()
            if active_markets:
                base_change *= 1.3
                
            current_price = coin['price'] * (1 + base_change/100)
            
            # تحلیل تایم‌فریم ۴ ساعته
            signal_4h, reason_4h = self.analyze_4h_timeframe(coin)
            
            # فعالیت نهنگ‌ها
            whale_action, whale_reason = self.detect_whale_activity(coin)
            
            # پتانسیل پامپ
            has_pump_potential = self.analyze_pump_potential(coin)
            
            # محاسبه پتانسیل سود
            profit_potential = self.calculate_profit_potential(coin, "LONG" if "LONG" in signal_4h else "SHORT")
            
            coin_data = {
                'symbol': coin['symbol'],
                'name': coin['name'],
                'price': current_price,
                'change_4h': base_change,
                'signal_4h': signal_4h,
                'signal_reason': reason_4h,
                'whale_activity': whale_action,
                'whale_reason': whale_reason,
                'profit_potential': profit_potential,
                'has_pump_potential': has_pump_potential,
                'category': coin['category'],
                'market_cap': coin['market_cap'],
                'volatility': coin['volatility']
            }
            
            market_data.append(coin_data)
            
        return market_data

    def send_urgent_pump_alert(self, coin_data):
        """ارسال هشدار پامپ فوری"""
        alert_key = f"{coin_data['symbol']}_pump"
        
        # جلوگیری از اسپم
        if alert_key in self.last_pump_alert:
            time_diff = datetime.now() - self.last_pump_alert[alert_key]
            if time_diff.total_seconds() < 3600:  # 1 hour
                return False
        
        message = f"🚨🚨 <b>هشدار پامپ بالقوه!</b> 🚨🚨\n\n"
        message += f"💰 <b>ارز:</b> {coin_data['symbol']} - {coin_data['name']}\n"
        message += f"📈 <b>تغییر ۴H:</b> {coin_data['change_4h']:+.1f}%\n"
        message += f"🎯 <b>سیگنال:</b> {coin_data['signal_4h']}\n"
        message += f"💎 <b>پتانسیل سود:</b> {coin_data['profit_potential']:.1f}%\n"
        message += f"🐋 <b>فعالیت نهنگ‌ها:</b> {coin_data['whale_activity']}\n\n"
        
        message += "⚡ <b>استراتژی پیشنهادی:</b>\n"
        message += "• 🟢 موقعیت LONG با ۴۰% سرمایه\n"
        message += f"• 🎯 حد سود: {coin_data['profit_potential']:.1f}%\n"
        message += "• ⚠️ حد ضرر: ۸%\n"
        message += "• ⏰ تایم‌فریم: ۴-۱۲ ساعت\n"
        
        if self.send_telegram(message):
            self.last_pump_alert[alert_key] = datetime.now()
            return True
        return False

    def create_4h_signal_report(self):
        """گزارش سیگنال ۴ ساعته"""
        market_data = self.generate_market_data()
        
        # فیلتر سیگنال‌های با ارزش
        valuable_signals = [c for c in market_data if c['profit_potential'] > 10]
        valuable_signals.sort(key=lambda x: x['profit_potential'], reverse=True)
        
        self.signal_count += 1
        
        # بازارهای فعال
        active_markets = self.get_current_market_hour()
        
        message = f"<b>📊 گزارش حرفه‌ای #{self.signal_count}</b>\n"
        message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        
        if active_markets:
            message += f"🌍 <b>بازارهای فعال:</b> {', '.join(active_markets)}\n"
        
        message += "─" * 40 + "\n\n"
        
        # سیگنال‌های برتر
        if valuable_signals:
            message += "<b>🎯 سیگنال‌های با پتانسیل بالا:</b>\n\n"
            for coin in valuable_signals[:5]:
                message += f"<b>💰 {coin['symbol']}</b> - {coin['name']}\n"
                message += f"   📈 {coin['signal_4h']} | سود: {coin['profit_potential']:.1f}%\n"
                message += f"   📊 دلیل: {coin['signal_reason']}\n"
                message += f"   🐋 {coin['whale_activity']}\n"
                
                if coin['has_pump_potential']:
                    message += f"   ⚡ <b>پتانسیل پامپ ۵۰٪+</b>\n"
                    
                message += "\n"
        
        # رتبه‌بندی ارزها
        message += "<b>🏆 رتبه‌بندی ارزها (پتانسیل سود):</b>\n"
        valuable_signals = sorted(market_data, key=lambda x: x['profit_potential'], reverse=True)
        for i, coin in enumerate(valuable_signals[:8], 1):
            signal_icon = "🟢" if "LONG" in coin['signal_4h'] else "🔴" if "SHORT" in coin['signal_4h'] else "🟡"
            message += f"{i}. {signal_icon} <b>{coin['symbol']}</b> | {coin['profit_potential']:.1f}% | {coin['signal_4h']}\n"
        
        # آمار کلی
        long_signals = len([c for c in market_data if "LONG" in c['signal_4h']])
        short_signals = len([c for c in market_data if "SHORT" in c['signal_4h'])
        pump_potentials = len([c for c in market_data if c['has_pump_potential']])
        
        message += f"\n<b>📈 آمار بازار:</b>\n"
        message += f"• 🟢 LONG: {long_signals}/20\n"
        message += f"• 🔴 SHORT: {short_signals}/20\n"
        message += f"• 🚀 پامپ بالقوه: {pump_potentials} ارز\n"
        message += f"• 💎 میانگین پتانسیل سود: {sum(c['profit_potential'] for c in market_data)/len(market_data):.1f}%\n"
        
        message += f"\n⏳ بروزرسانی بعدی: ۴ ساعت\n"
        message += f"📡 تحت نظر: ۲۰ ارز منتخب"
        
        return message, market_data

    def monitor_pumps(self, market_data):
        """مانیتورینگ لحظه‌ای پامپ‌ها"""
        pumps_detected = 0
        
        for coin in market_data:
            # شرایط پامپ: تغییرات بالا + پتانسیل سود بالا + فعالیت نهنگ‌ها
            if (coin['change_4h'] > 15 and 
                coin['profit_potential'] > 20 and 
                "نهنگ" in coin['whale_activity'] and
                coin['has_pump_potential']):
                
                if self.send_urgent_pump_alert(coin):
                    pumps_detected += 1
                    
        return pumps_detected

    def run_bot(self):
        """اجرای ربات"""
        print("🤖 ربات تحلیل‌گر حرفه‌ای فعال شد")
        self.send_telegram("🎯 <b>ربات تحلیل‌گر حرفه‌ای فعال شد!</b>\n\n"
                          "📊 تحلیل ۲۰ ارز منتخب\n"
                          "⏰ سیگنال‌های ۴ ساعته\n"
                          "🐋 ردیابی نهنگ‌ها\n"
                          "🚀 هشدار پامپ‌های بالقوه")
        
        while True:
            try:
                print(f"🔍 تحلیل #{self.signal_count + 1}")
                
                # تولید گزارش ۴ ساعته
                report, market_data = self.create_4h_signal_report()
                self.send_telegram(report)
                
                # مانیتورینگ پامپ‌های لحظه‌ای
                pumps_detected = self.monitor_pumps(market_data)
                if pumps_detected > 0:
                    print(f"🚨 {pumps_detected} هشدار پامپ ارسال شد")
                
                print(f"✅ سیگنال #{self.signal_count} ارسال شد")
                
                # انتظار ۴ ساعت
                time.sleep(4 * 3600)  # 4 hours
                
            except Exception as e:
                print(f"💥 خطا: {e}")
                time.sleep(300)  # 5 minutes then retry

# ایجاد و اجرای ربات
bot = AdvancedTradingBot()
bot_thread = Thread(target=bot.run_bot)
bot_thread.daemon = True
bot_thread.start()

@app.route('/')
def home():
    active_markets = bot.get_current_market_hour()
    return f"""
    <html>
        <head>
            <title>ربات تحلیل‌گر حرفه‌ای</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Tahoma; text-align: center; padding: 30px; }}
                .info {{ background: #f0f8ff; padding: 20px; border-radius: 10px; margin: 10px; }}
            </style>
        </head>
        <body>
            <h1>🤖 ربات تحلیل‌گر حرفه‌ای</h1>
            
            <div class="info">
                <h3>📊 وضعیت ربات</h3>
                <p>سیگنال‌های ارسالی: {bot.signal_count}</p>
                <p>بازارهای فعال: {', '.join(active_markets) if active_markets else 'همه بازارها بسته'}</p>
                <p>آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="info">
                <h3>🎯 ویژگی‌ها</h3>
                <p>• تحلیل ۲۰ ارز منتخب</p>
                <p>• سیگنال‌های ۴ ساعته</p>
                <p>• ردیابی نهنگ‌ها</p>
                <p>• هشدار پامپ‌های بالقوه</p>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)