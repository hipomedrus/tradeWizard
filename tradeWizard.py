import streamlit as st

# =======================
# Calculation Functions
# =======================

def calculate_spot(buy_price: float, quantity: float,
                   buy_fee_rate: float, sell_price: float,
                   sell_fee_rate: float) -> dict:
    buy_total = buy_price * quantity
    buy_fee = buy_total * buy_fee_rate
    total_cost = buy_total + buy_fee

    sell_total = sell_price * quantity
    sell_fee = sell_total * sell_fee_rate
    net_sell = sell_total - sell_fee

    pnl = net_sell - total_cost
    percent_pnl = (pnl / total_cost) * 100 if total_cost != 0 else 0
    break_even = total_cost / quantity if quantity != 0 else 0

    return {
        'total_cost': total_cost,
        'net_sell': net_sell,
        'pnl': pnl,
        'percent_pnl': percent_pnl,
        'break_even': break_even
    }


def calculate_futures(entry_price: float, position_type: str,
                      margin: float, leverage: int,
                      funding_rate: float, funding_hours: int,
                      fee_rate: float, account_balance: float,
                      risk_percent: float, sl_price: float,
                      tp_price: float) -> dict:
    position_size = margin * leverage

    # PnL calculations
    if position_type.lower() == 'long':
        pnl_sl = (sl_price - entry_price) * position_size / entry_price
        pnl_tp = (tp_price - entry_price) * position_size / entry_price
        liquidation_price = entry_price * (1 - 1 / leverage) if leverage != 0 else 0
    else:
        pnl_sl = (entry_price - sl_price) * position_size / entry_price
        pnl_tp = (entry_price - tp_price) * position_size / entry_price
        liquidation_price = entry_price * (1 + 1 / leverage) if leverage != 0 else 0

    # Risk/Reward
    risk_amount = abs(pnl_sl)
    reward_amount = abs(pnl_tp)
    risk_reward_ratio = (reward_amount / risk_amount) if risk_amount != 0 else 0

    # Suggested position size
    max_risk = account_balance * risk_percent
    suggested_size = (max_risk / abs((sl_price - entry_price) / entry_price)) if sl_price != entry_price else 0

    # Costs
    funding_cost = position_size * funding_rate * funding_hours
    commission_cost = position_size * fee_rate * 2

    # Scenario PnL
    total_pnl_sl = pnl_sl - commission_cost - funding_cost
    total_pnl_tp = pnl_tp - commission_cost - funding_cost

    # Return on Equity
    roe = (pnl_tp / margin) * 100 if margin != 0 else 0

    return {
        'position_size': position_size,
        'liquidation_price': liquidation_price,
        'risk_amount': risk_amount,
        'reward_amount': reward_amount,
        'risk_reward_ratio': risk_reward_ratio,
        'suggested_size': suggested_size,
        'funding_cost': funding_cost,
        'commission_cost': commission_cost,
        'total_pnl_sl': total_pnl_sl,
        'total_pnl_tp': total_pnl_tp,
        'roe': roe
    }


# =======================
# Streamlit App
# =======================

def main():
    st.set_page_config(page_title="TradeWizard", page_icon="🧙‍♂️")
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #007bff;
            color: white;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.title("🧙‍♂️ TradeWizard")
    st.write("Kâr/zarar, risk ve finansman analizlerinizi hızlıca yapın. Spot ve vadeli işlemler için ideal araç.")

    # 1) Market Type
    with st.expander("1) Piyasa Türü / Market Type", expanded=True):
        market_type = st.radio(
            "Seçiniz:",
            ["Spot", "Vadeli/Futures"],
            index=0,
            help="Spot: doğrudan alım/satım; Vadeli/Futures: kaldıraçlı pozisyon."
        )

    # 2) İşlem Bilgileri / Trade Details
    with st.expander("2) İşlem Bilgileri / Trade Details", expanded=True):
        if market_type == "Spot":
            buy_price = st.number_input("Alım fiyatı (Buy Price)", min_value=0.0, step=0.10, format="%.8f",
                                       help="Varlığı alacağınız birim fiyat.")
            quantity = st.number_input("Miktar (Quantity)", min_value=0.0, step=0.10, format="%.8f",
                                       help="Alım için gireceğiniz miktar.")
            sell_price = st.number_input("Satış fiyatı (Sell Price)", min_value=0.0, step=0.10, format="%.8f",
                                        help="Varlığı satacağınız birim fiyat.")
        else:
            entry_price = st.number_input("Giriş fiyatı (Entry Price)", min_value=0.0, step=0.10, format="%.8f",
                                        help="Pozisyona giriş yapacağınız fiyat.")
            position_type = st.selectbox("Pozisyon Yönü (Position Type)", ["Long (Buy)", "Short (Sell)"],
                                        help="Long: yükseliş; Short: düşüş yönlü pozisyon.")
            margin = st.number_input("Teminat (Collateral)", min_value=0.0, step=0.10, format="%.2f",
                                     help="Pozisyon açmak için yatırdığınız tutar.")
            leverage = st.number_input("Kaldıraç (Leverage)", min_value=1, max_value=1000, step=1, format="%d", value=1,
                                        help="Pozisyonda kullandığınız kaldıraç çarpanı.")

    # 3) Komisyon ve ek maliyetler / Commission & Additional Costs
    with st.expander("3) Komisyon ve ek maliyetler / Commission & Additional Costs", expanded=False):
        if market_type == "Spot":
            buy_fee_percent = st.number_input("Alım komisyon oranı (%) (Buy Fee %)", min_value=0.0, step=0.0001, format="%.4f",
                                             help="Alım işlemi için alınan komisyon yüzdesi.")
            sell_fee_percent = st.number_input("Satış komisyon oranı (%) (Sell Fee %)", min_value=0.0, step=0.0001, format="%.4f",
                                              help="Satış işlemi için alınan komisyon yüzdesi.")
            buy_fee_rate = buy_fee_percent / 100
            sell_fee_rate = sell_fee_percent / 100
        else:
            fee_percent = st.number_input("Komisyon oranı (%) (Fee %)", min_value=0.0, step=0.0001, format="%.4f",
                                         help="Pozisyon açıp kapatma işlemindeki toplam komisyon yüzdesi.")
            fee_rate = fee_percent / 100
            funding_percent = st.number_input("Saatlik faiz oranı (%) (Funding Rate %)", min_value=0.0, step=0.0001, format="%.4f",
                                             help="Açık pozisyonunuz için uygulanan saatlik fonlama/faiz oranı.")
            funding_rate = funding_percent / 100
            funding_hours = st.number_input("Pozisyon Süresi (Saat)", min_value=0, step=1, format="%d", value=24,
                                           help="Pozisyonun açık kalacağı tahmini süre saat olarak.")

    # 4) Risk Yönetimi / Risk Management (Futures only)
    if market_type == "Vadeli/Futures":
        with st.expander("4) Risk Yönetimi / Risk Management", expanded=False):
            account_balance = st.number_input("Hesap Bakiyesi (Account Balance)", min_value=0.0, step=1.0, format="%.2f",
                                             help="Toplam portföy bakiyesi veya kullanılabilir sermaye.")
            risk_percent_input = st.number_input("Risk oranı (%) (Risk %)", min_value=0.0, max_value=100.0, step=0.50, format="%.2f",
                                                 help="Portföyden işlem başına riske edilecek yüzde.")
            risk_percent = risk_percent_input / 100
            sl_price = st.number_input("Stop Loss Seviyesi (SL Price)", min_value=0.00, step=0.1000000, format="%.8f",
                                       help="Pozisyon zararı sınırlandırmak için belirlenen fiyat seviyesi.")
            tp_price = st.number_input("Take Profit Seviyesi (TP Price)", min_value=0.00, step=0.1000000, format="%.8f",
                                       help="Pozisyon kârı almak için belirlenen fiyat seviyesi.")

    # Calculate Button
    if st.button("Hesapla / Calculate"):
        if market_type == "Spot":
            res = calculate_spot(buy_price, quantity, buy_fee_rate, sell_price, sell_fee_rate)
            with st.expander("Spot Sonuçları", expanded=True):
                st.write(f"Toplam Maliyet: {res['total_cost']:.4f}")
                st.write(f"Net Gelir: {res['net_sell']:.4f}")
                st.write(f"Kâr/Zarar: {res['pnl']:.4f}")
                st.write(f"% Kâr/Zarar: {res['percent_pnl']:.2f}%")
                st.write(f"Başabaş Fiyatı: {res['break_even']:.4f}")
        else:
            res = calculate_futures(entry_price, position_type, margin, leverage,
                                     funding_rate, funding_hours, fee_rate,
                                     account_balance, risk_percent, sl_price, tp_price)
            with st.expander("Vadeli Sonuçları", expanded=True):
                st.write(f"Pozisyon Büyüklüğü: {res['position_size']:.4f}")
                st.write(f"Likidasyon Fiyatı: {res['liquidation_price']:.8f}")
                st.write(f"Risk Miktarı: {res['risk_amount']:.4f}")
                st.write(f"Kazanç: {res['reward_amount']:.4f}")
                st.write(f"Risk/Ödül: {res['risk_reward_ratio']:.2f}")
                st.write(f"Önerilen Pozisyon: {res['suggested_size']:.4f}")
                st.write(f"Ek Maliyet: {res['funding_cost']:.4f}")
                st.write(f"Komisyon: {res['commission_cost']:.4f}")
                st.write(f"SL Senaryosu Net: {res['total_pnl_sl']:.4f}")
                st.write(f"TP Senaryosu Net: {res['total_pnl_tp']:.4f}")
                st.write(f"ROE: {res['roe']:.2f}%")

if __name__ == '__main__':
    main()
