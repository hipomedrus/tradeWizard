import streamlit as st

st.set_page_config(page_title="Trade Wizard", page_icon="💹")

st.title("💹 Piyasa İşlem Hesaplayıcı (Market Trade Calculator)")

st.markdown("""
*Bu uygulama, spot ve vadeli (futures) piyasalarda pozisyonunu, kâr/zararını ve riskini hesaplamanıza yardımcı olur.*
""")

market_type = st.radio(
    "İşlem türünü seçiniz (Select market type):",
    ("Spot", "Vadeli/Futures"),
    index=0
)

if market_type == "Spot":
    st.subheader("Spot İşlem (Spot Trade)")
    with st.form("spot_form"):
        buy_price = st.number_input("Alım fiyatı (Buy Price):", min_value=0.0, format="%.8f")
        quantity = st.number_input("Alınan miktar (Quantity):", min_value=0.0, format="%.8f")
        buy_fee_rate = st.number_input("Alım komisyon oranı (ör: %0.1 için 0.001 girin) (Buy Fee Rate):", min_value=0.0, format="%.6f")
        sell_price = st.number_input("Satış fiyatı (Sell Price):", min_value=0.0, format="%.8f")
        sell_fee_rate = st.number_input("Satış komisyon oranı (ör: %0.1 için 0.001 girin) (Sell Fee Rate):", min_value=0.0, format="%.6f")
        submitted = st.form_submit_button("Hesapla")
    
    if submitted:
        buy_total = buy_price * quantity
        buy_fee = buy_total * buy_fee_rate
        total_cost = buy_total + buy_fee

        sell_total = sell_price * quantity
        sell_fee = sell_total * sell_fee_rate
        net_sell = sell_total - sell_fee

        pnl = net_sell - total_cost
        percent_pnl = (pnl / total_cost) * 100 if total_cost != 0 else 0
        break_even = total_cost / quantity if quantity != 0 else 0

        st.success("💹 **Sonuçlar:**")
        st.write(f"Toplam Alım Maliyeti (Total Cost): `{total_cost:.4f}`")
        st.write(f"Net Satış Geliri (Net Proceeds): `{net_sell:.4f}`")
        st.write(f"Kâr/Zarar (Profit/Loss): `{pnl:.4f}`")
        st.write(f"Yüzde Kâr/Zarar (Percent PnL): `{percent_pnl:.2f}%`")
        st.write(f"Başabaş Fiyatı (Break-even Price): `{break_even:.4f}`")

elif market_type == "Vadeli/Futures":
    st.subheader("Vadeli İşlem (Futures Trade)")
    with st.form("futures_form"):
        entry_price = st.number_input("Pozisyona giriş fiyatı (Entry Price):", min_value=0.0, format="%.8f")
        position_type = st.selectbox("İşlem yönü (Position Type):", ("long", "short"))
        margin = st.number_input("Kullanılan teminat (Margin/Collateral):", min_value=0.0, format="%.4f")
        leverage = st.number_input("Kaldıraç oranı (Leverage Ratio):", min_value=1.0, format="%.2f", value=1.0)
        funding_rate = st.number_input("Saatlik ek maliyet oranı (ör: %0.005 için 0.00005 girin) (Funding/Swap Rate):", min_value=0.0, format="%.8f")
        funding_hours = st.number_input("Pozisyon süresi (saat) (Position duration in hours):", min_value=0.0, format="%.2f", value=24.0)
        fee_rate = st.number_input("İşlem komisyon oranı (ör: %0.02 için 0.0002 girin) (Trading Fee Rate):", min_value=0.0, format="%.6f")
        account_balance = st.number_input("Portföy büyüklüğü (Account Balance):", min_value=0.0, format="%.2f")
        risk_percent = st.number_input("İşlem başına risk oranı (ör: %2 için 0.02 girin) (Risk per Trade):", min_value=0.0, max_value=1.0, format="%.4f")
        sl_price = st.number_input("Stop Loss seviyesi (Stop Loss Price):", min_value=0.0, format="%.8f")
        tp_price = st.number_input("Take Profit seviyesi (Take Profit Price):", min_value=0.0, format="%.8f")
        submitted = st.form_submit_button("Hesapla")
    
    if submitted:
        position_size = margin * leverage
        st.write(f"Pozisyon Büyüklüğü (Position Size): `{position_size:.4f}`")

        # PnL hesaplama
        if position_type == "long":
            pnl_sl = (sl_price - entry_price) * position_size / entry_price
            pnl_tp = (tp_price - entry_price) * position_size / entry_price
        else:
            pnl_sl = (entry_price - sl_price) * position_size / entry_price
            pnl_tp = (entry_price - tp_price) * position_size / entry_price

        risk_amount = abs(pnl_sl)
        reward_amount = abs(pnl_tp)
        risk_reward_ratio = reward_amount / risk_amount if risk_amount != 0 else 0

        max_risk = account_balance * risk_percent
        suggested_position_size = max_risk / abs((sl_price - entry_price) / entry_price) if sl_price != entry_price else 0

        funding_cost = position_size * funding_rate * funding_hours
        commission = position_size * fee_rate * 2

        st.success("💹 **Sonuçlar:**")
        st.write(f"Stop Loss'ta kayıp (Risk Amount): `{risk_amount:.4f}`")
        st.write(f"Take Profit'te kazanç (Reward Amount): `{reward_amount:.4f}`")
        st.write(f"Risk/Ödül Oranı (Risk/Reward Ratio): `{risk_reward_ratio:.2f}`")
        st.write(f"Risk yönetimine göre önerilen pozisyon büyüklüğü (Suggested Position Size): `{suggested_position_size:.4f}`")
        st.write(f"{funding_hours:.2f} saatlik ek maliyet (Funding/Swap): `{funding_cost:.4f}`")
        st.write(f"İşlem komisyonu (Transaction Fees, round-trip): `{commission:.4f}`")

        # Senaryolar
        st.markdown("**Olası Senaryolar (Possible Scenarios):**")
        total_pnl_sl = pnl_sl - commission - funding_cost
        total_pnl_tp = pnl_tp - commission - funding_cost
        st.write(f"Stop Loss'a ulaşılırsa: Fiyat `{sl_price}`, Net Sonuç: `{total_pnl_sl:.4f}` (Kâr/Zarar - komisyon - ek maliyet)")
        st.write(f"Take Profit'e ulaşılırsa: Fiyat `{tp_price}`, Net Sonuç: `{total_pnl_tp:.4f}` (Kâr/Zarar - komisyon - ek maliyet)")

        roe = (pnl_tp / margin) * 100 if margin != 0 else 0
        st.write(f"Kârlı senaryoda özsermaye getirisi (ROE): `%{roe:.2f}`")

st.info("Herhangi bir sonucu başka bir hesaplama yapmak için kutuları değiştirebilir, yeni değerler girerek tekrar hesaplayabilirsiniz.")
