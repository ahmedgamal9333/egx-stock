import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="منصة تحليل البورصة المصرية", layout="wide", initial_sidebar_state="expanded")

st.title("🇪🇬 منصة تحليل أسهم البورصة المصرية (EGX)")
st.markdown("---")

st.sidebar.header("لوحة التحكم")
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

selected_stock_name = st.sidebar.selectbox("اختر السهم للتحليل:", list(stocks_dict.keys()))
tv_symbol = stocks_dict[selected_stock_name]
ticker_code = tv_symbol.split(":")[1] + ".CA"

st.subheader(f"📈 الرسم البياني والتحليل الفني اللحظي: {selected_stock_name}")

tradingview_html = f"""
<div class="tradingview-widget-container" style="height:600px;width:100%;">
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

components.html(tradingview_html, height=620)
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 البيانات الماليّة الأساسية")
    try:
        stock = yf.Ticker(ticker_code)
        info = stock.info
        st.metric("أعلى سعر 52 أسبوع", f"{info.get('fiftyTwoWeekHigh', 'N/A')} ج.م")
        st.metric("أدنى سعر 52 أسبوع", f"{info.get('fiftyTwoWeekLow', 'N/A')} ج.م")
        st.metric("مضاعف الربحية (P/E)", f"{info.get('trailingPE', 'N/A')}")
        st.metric("القيمة الدفترية", f"{info.get('bookValue', 'N/A')} ج.م")
    except:
        st.info("جاري تحديث البيانات المالية...")

with col2:
    st.subheader("📰 أحدث الأخبار المتعلقة بالسهم")
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
        
