import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="منصة التحليل الذكي للبورصة المصرية", layout="wide", initial_sidebar_state="expanded")

st.title("🚀 المنصة الذكية المتقدمة لتحليل أسهم البورصة المصرية (EGX + AI Insights)")
st.markdown("---")

st.sidebar.header("لوحة التحكم والتحليل")
stocks_dict = {
    "أموك (AMOC)": "EGX:AMOC",
    "التجاري الدولي (COMI)": "EGX:COMI",
    "سيدي كرير (SKPC)": "EGX:SKPC",
    "أبو قير للأسمدة (ABUK)": "EGX:ABUK",
    "طلعت مصطفى (TMGH)": "EGX:TMGH",
    "السويدي إلكتريك (SWDY)": "EGX:SWDY",
    "فوري (FWRY)": "EGX:FWRY",
    "مصر للألومنيوم (EGAL)": "EGX:EGAL"
}

selected_stock_name = st.sidebar.selectbox("اختر السهم للتحليل المتقدم:", list(stocks_dict.keys()))
tv_symbol = stocks_dict[selected_stock_name]
ticker_code = tv_symbol.split(":")[1] + ".CA"

# جلب البيانات التاريخية لحساب المؤشرات الذكية
stock = yf.Ticker(ticker_code)
df = stock.history(period="6mo")

if not df.empty:
    current_price = df['Close'].iloc[-1]
    
    # حساب مؤشر القوة النسبية (RSI)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    current_rsi = df['RSI'].iloc[-1]
    
    # تحديد مناطق الدعم والمقاومة المقترحة بناءً على آخر 3 महीने
    recent_low = df['Low'].tail(30).min()
    recent_high = df['High'].tail(30).max()
    suggested_buy = recent_low * 1.01  # قرب منطقة الدعم
    suggested_sell = recent_high * 0.99 # قرب منطقة المقاومة
else:
    current_price = 0
    current_rsi = 50
    recent_low = 0
    recent_high = 0
    suggested_buy = 0
    suggested_sell = 0

st.subheader(f"📊 مؤشرات التحليل الذكي ومناطق التداول: {selected_stock_name}")

# عرض مؤشرات الأسعار والصفقات المقترحة
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("السعر اللحظي الحالي", f"{current_price:.2f} ج.م")
with col_m2:
    st.metric("مؤشر التشبع (RSI 14)", f"{current_rsi:.1f}")
with col_m3:
    st.metric("🟢 سعر الدعم / الشراء المقترح", f"{suggested_buy:.2f} ج.م")
with col_m4:
    st.metric("🔴 سعر المقاومة / البيع المقترح", f"{suggested_sell:.2f} ج.م")

# صندوق تحليل الذكاء الاصطناعي والتوقع الفني
st.markdown("### 🤖 تقرير تحليل الذكاء الاصطناعي وحركة السهم (AI Verdict)")
if current_rsi < 35:
    st.success("🟢 **حالة السهم: فرصة تجميع / تشبع بيعي:** السهم يقترب من مستويات دعم قوية ومؤشر RSI يعكس فرصة دخول تدريجي جيدة مع وضع وقف خسارة أسفل سعر الدعم مباشرة.")
elif current_rsi > 65:
    st.warning("🔴 **حالة السهم: منطقة حذر / تشبع شرائي:** السهم قرب مستويات مقاومة هامة ومؤشر RSI مرتفع، يُنصح بجني الأرباح الجزئي وعدم مطاردة السعر في القمم.")
else:
    st.info("🟡 **حالة السهم: حركة عرضية مستقرة:** السهم يتحرك في نطاق آمن بين الدعم والمقاومة، يُفضل مراقبة الفوليوم والانتظار لاختراق إحدى القنوات.")

# البيانات المالية الأساسية
try:
    info = stock.info
    st.markdown("### 📈 الأساسيات المالية والتقييم العادل")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        st.metric("مضاعف الربحية (P/E)", f"{info.get('trailingPE', 'N/A')}")
    with f_col2:
        st.metric("القيمة الدفترية", f"{info.get('bookValue', 'N/A')} ج.م")
    with f_col3:
        st.metric("أعلى سعر 52 أسبوع", f"{info.get('fiftyTwoWeekHigh', 'N/A')} ج.م")
    with f_col4:
        st.metric("أدنى سعر 52 أسبوع", f"{info.get('fiftyTwoWeekLow', 'N/A')} ج.م")
except:
    pass

st.markdown("---")

# الرسم البياني المتقدم من TradingView
st.subheader(f"📈 الرسم البياني التفاعلي الشامل")
tradingview_html = f"""
<div class="tradingview-widget-container" style="height:580px;width:100%;">
  <div id="tradingview_widget" style="height:calc(100% - 32px);width:100%;"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "autosize": true,
    "symbol": "{tv_symbol}",
    "interval": "D",
    "timezone": "Africa/Cairo",
    "theme": "dark",
    "style": "1",
    "locale": "ar",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_widget"
  }});
  </script>
</div>
"""
components.html(tradingview_html, height=600)
st.markdown("---")

# الأخبار اللحظية وتأثيرها
st.subheader("📰 أحدث الأخبار وتأثيرها المحتمل على السهم")
try:
    news_url = f"https://news.google.com/rss/search?q={selected_stock_name.split()[0]}+البورصة+المصرية&hl=ar&gl=EG&ceid=EG:ar"
    response = requests.get(news_url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')[:5]
    for item in items:
        st.markdown(f"🔹 **[{item.title.text}]({item.link.text})**")
        st.caption(f"التاريخ: {item.pubDate.text[:16]}")
except:
    st.write("تعذر جلب الأخبار حالياً.")
    
