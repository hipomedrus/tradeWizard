# TradeWizard: A PnL, risk and funding analysis tool for spot and futures trades.
import streamlit as st

# =======================
# Translation Dictionary: holds UI text in English and Turkish
# =======================
texts = {
    'subtitle':        {'en': 'Quick PnL, risk and funding analysis for spot and futures trading.',
                        'tr': 'Spot ve vadeli işlemler için kâr/zarar, risk ve finansman analizleri.'},
    'market_exp':      {'en': '1) Market Type',         'tr': '1) Piyasa Türü'},
    'select_market':   {'en': 'Select Market:',        'tr': 'Piyasayı Seç:'},
    'spot':            {'en': 'Spot',                  'tr': 'Spot'},
    'futures':         {'en': 'Futures',               'tr': 'Vadeli'},
    'trade_exp':       {'en': '2) Trade Details',       'tr': '2) İşlem Bilgileri'},
    'buy_price':       {'en': 'Buy Price',             'tr': 'Alım Fiyatı'},
    'quantity':        {'en': 'Quantity',              'tr': 'Miktar'},
    'sell_price':      {'en': 'Sell Price',            'tr': 'Satış Fiyatı'},
    'entry_price':     {'en': 'Entry Price',           'tr': 'Giriş Fiyatı'},
    'direction':       {'en': 'Direction',             'tr': 'Pozisyon Yönü'},
    'long':            {'en': 'Long',                  'tr': 'Long'},
    'short':           {'en': 'Short',                 'tr': 'Short'},
    'margin':          {'en': 'Margin',                'tr': 'Teminat'},
    'leverage':        {'en': 'Leverage',              'tr': 'Kaldıraç'},
    'costs_exp':       {'en': '3) Commission & Funding','tr': '3) Komisyon ve ek maliyetler'},
    'buy_comm':        {'en': 'Buy Commission (%)',    'tr': 'Alım Komisyonu (%)'},
    'sell_comm':       {'en': 'Sell Commission (%)',   'tr': 'Satış Komisyonu (%)'},
    'comm':            {'en': 'Commission (%)',        'tr': 'Komisyon (%)'},
    'fund_rate':       {'en': 'Funding Rate (%/h)',    'tr': 'Saatlik Faiz (%)'},
    'duration':        {'en': 'Position Duration (h)', 'tr': 'Pozisyon Süresi (Saat)'},
    'risk_exp':        {'en': '4) Risk Management',    'tr': '4) Risk Yönetimi'},
    'balance':         {'en': 'Account Balance',       'tr': 'Hesap Bakiyesi'},
    'risk_pct':        {'en': 'Risk per Trade (%)',    'tr': 'Risk Oranı (%)'},
    'sl_price':        {'en': 'Stop Loss Price',       'tr': 'Stop Loss Seviyesi'},
    'tp_price':        {'en': 'Take Profit Price',     'tr': 'Take Profit Seviyesi'},
    'btn_calc':        {'en': 'Calculate',             'tr': 'Hesapla'},
    # Spot result keys and helpers
    'res_spot':        {'en': 'Spot Results',          'tr': 'Spot Sonuçları'},
    'res_total_cost':  {'en': 'Total Cost',            'tr': 'Toplam Maliyet'},
    'help_total_cost': {'en': 'Total cost including buy price and commission',
                        'tr': 'Alım fiyatı ve komisyon dahil toplam maliyet'},
    'res_net_sell':    {'en': 'Net Proceeds',          'tr': 'Net Gelir'},
    'help_net_sell':   {'en': 'Proceeds after deducting sell commission',
                        'tr': 'Satış komisyonu düşüldükten sonraki gelir'},
    'res_pnl':         {'en': 'PnL',                   'tr': 'Kâr/Zarar'},
    'help_pnl':        {'en': 'Net profit or loss from the trade',
                        'tr': 'İşlemden elde edilen net kâr veya zarar'},
    'res_percent':     {'en': '% PnL',                'tr': '% Kâr/Zarar'},
    'help_percent':    {'en': 'Profit or loss as percentage of total cost',
                        'tr': 'Toplam maliyete göre yüzde kâr/zarar'},
    'res_break_even':  {'en': 'Break-even Price',      'tr': 'Başabaş Fiyatı'},
    'help_break_even': {'en': 'Price needed per unit to avoid loss',
                        'tr': 'Zarar etmemek için gereken birim fiyat'},
    # Futures result keys and helpers
    'res_fut':         {'en': 'Futures Results',       'tr': 'Vadeli Sonuçları'},
    'res_position':    {'en': 'Position Size',         'tr': 'Pozisyon Büyüklüğü'},
    'help_position':   {'en': 'Total position notional size',
                        'tr': 'Pozisyonun toplam nominal büyüklüğü'},
    'res_liq':         {'en': 'Liquidation Price',     'tr': 'Likidasyon Fiyatı'},
    'help_liq':        {'en': 'Price level at which position is liquidated',
                        'tr': 'Pozisyonunuzun likide edileceği fiyat seviyesi'},
    'res_pnl_sl':      {'en': 'PnL if SL',             'tr': 'SL Senaryosu PnL'},
    'help_pnl_sl':     {'en': 'Profit or loss if stop loss triggers',
                        'tr': 'Stop loss gerçekleştiğinde kâr/zarar'},
    'res_pnl_tp':      {'en': 'PnL if TP',             'tr': 'TP Senaryosu PnL'},
    'help_pnl_tp':     {'en': 'Profit or loss if take profit triggers',
                        'tr': 'Take profit gerçekleştiğinde kâr/zarar'},
    'res_rr':          {'en': 'Risk/Reward Ratio',     'tr': 'Risk/Ödül Oranı'},
    'help_rr':         {'en': 'Ratio of reward amount over risk amount',
                        'tr': 'Ödül miktarının risk miktarına oranı'},
    'res_sugg':        {'en': 'Suggested Position',    'tr': 'Önerilen Pozisyon'},
    'help_sugg':       {'en': 'Recommended position size based on risk settings',
                        'tr': 'Risk ayarlarına göre önerilen pozisyon büyüklüğü'},
    'res_fund':        {'en': 'Funding Cost',          'tr': 'Ek Maliyet'},
    'help_fund':       {'en': 'Total funding cost over position duration',
                        'tr': 'Pozisyon süresi boyunca oluşacak fonlama maliyeti'},
    'res_comm':        {'en': 'Commission',            'tr': 'Komisyon'},
    'help_comm':       {'en': 'Commission cost for opening the position',
                        'tr': 'Pozisyon açma maliyeti olarak komisyon tutarı'},
    'res_roe':         {'en': 'ROE',                   'tr': 'ROE'},
    'help_roe':        {'en': 'Return on equity based on margin',
                        'tr': 'Teminat üzerinden getiri yüzdesi'}
}

# Initialize session state for language persistence
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

# =======================
# Calculation Functions
# =======================
def calculate_spot(buy_price: float, quantity: float,
                   buy_fee_rate: float, sell_price: float,
                   sell_fee_rate: float) -> dict:
    total_cost = buy_price * quantity * (1 + buy_fee_rate)
    net_sell = sell_price * quantity * (1 - sell_fee_rate)
    pnl = net_sell - total_cost
    percent_pnl = (pnl / total_cost) * 100 if total_cost else 0
    break_even = total_cost / quantity if quantity else 0
    return {'total_cost': total_cost,
            'net_sell': net_sell,
            'pnl': pnl,
            'percent_pnl': percent_pnl,
            'break_even': break_even}


def calculate_futures(entry_price: float, direction: str,
                      margin: float, leverage: int,
                      funding_rate: float, duration_hours: int,
                      fee_rate: float, balance: float,
                      risk_fraction: float,
                      sl_price: float, tp_price: float) -> dict:
    position_size = margin * leverage
    if direction.lower() == 'long':
        pnl_sl = (sl_price - entry_price) * position_size / entry_price
        pnl_tp = (tp_price - entry_price) * position_size / entry_price
        liquidation_price = entry_price * (1 - 1 / leverage)
    else:
        pnl_sl = (entry_price - sl_price) * position_size / entry_price
        pnl_tp = (entry_price - tp_price) * position_size / entry_price
        liquidation_price = entry_price * (1 + 1 / leverage)
    risk_amount = abs(pnl_sl)
    reward_amount = abs(pnl_tp)
    risk_reward_ratio = (reward_amount / risk_amount) if risk_amount else 0
    max_risk_amount = balance * risk_fraction
    suggested_position = (max_risk_amount * entry_price / abs(sl_price - entry_price)) if sl_price != entry_price else 0
    funding_cost = position_size * funding_rate * duration_hours
    commission = position_size * fee_rate
    net_pnl_sl = pnl_sl - commission - funding_cost
    net_pnl_tp = pnl_tp - commission - funding_cost
    roe = (pnl_tp / margin) * 100 if margin else 0
    return {'position_size': position_size,
            'liquidation_price': liquidation_price,
            'net_pnl_sl': net_pnl_sl,
            'net_pnl_tp': net_pnl_tp,
            'risk_reward_ratio': risk_reward_ratio,
            'suggested_position': suggested_position,
            'funding_cost': funding_cost,
            'commission': commission,
            'roe': roe}

# =======================
# Streamlit App
# =======================
def main():
    st.set_page_config(page_title="TradeWizard", page_icon="💹")
    st.markdown("""
        <style>
        .stButton>button { font-size:0.75rem; padding:0.25rem 0.5rem; }
        </style>
        """, unsafe_allow_html=True)
    cols = st.columns([15, 1, 1])
    with cols[1]:
        if st.button('EN', key='lang_en'):
            st.session_state.lang = 'en'
    with cols[2]:
        if st.button('TR', key='lang_tr'):
            st.session_state.lang = 'tr'
    tr = (st.session_state.lang == 'tr')
    _ = lambda k: texts[k]['tr'] if tr else texts[k]['en']

    st.title("TradeWizard")
    st.write(_('subtitle'))

    # 1) Market selection
    with st.expander(_('market_exp'), expanded=True):
        market = st.radio(_('select_market'), [_('spot'), _('futures')], key='market')

    # 2) Trade detail inputs
    with st.expander(_('trade_exp'), expanded=True):
        if market == _('spot'):
            buy_price = st.number_input(_('buy_price'), min_value=0.0, step=0.10, format="%.8f", key='buy')
            quantity = st.number_input(_('quantity'), min_value=0.0, step=0.10, format="%.8f", key='qty')
            sell_price = st.number_input(_('sell_price'), min_value=0.0, step=0.10, format="%.8f", key='sell')
        else:
            entry_price = st.number_input(_('entry_price'), min_value=0.0, step=0.10, format="%.8f", key='entry')
            direction = st.selectbox(_('direction'), [_('long'), _('short')], key='dir')
            margin = st.number_input(_('margin'), min_value=0.0, step=0.10, format="%.2f", key='mg')
            leverage = st.number_input(_('leverage'), min_value=1, max_value=1000, step=1,
                                      format="%d", value=1, key='lev')

    # 3) Commission and funding inputs
    with st.expander(_('costs_exp'), expanded=False):
        if market == _('spot'):
            buy_fee_pct = st.number_input(_('buy_comm'), min_value=0.0, step=0.0001,
                                          format="%.4f", key='bf')
            sell_fee_pct = st.number_input(_('sell_comm'), min_value=0.0, step=0.0001,
                                           format="%.4f", key='sf')
            buy_fee_rate = buy_fee_pct / 100
            sell_fee_rate = sell_fee_pct / 100
        else:
            fee_pct = st.number_input(_('comm'), min_value=0.0, step=0.0001,
                                      format="%.4f", key='cf')
            fee_rate = fee_pct / 100
            fund_pct = st.number_input(_('fund_rate'), min_value=0.0, step=0.0001,
                                      format="%.4f", key='ff')
            funding_rate = fund_pct / 100
            duration = st.number_input(_('duration'), min_value=0, step=1,
                                       format="%d", value=24, key='dur')

    # 4) Risk management for futures
    if market == _('futures'):
        with st.expander(_('risk_exp'), expanded=False):
            balance = st.number_input(_('balance'), min_value=0.0, step=1.0,
                                      format="%.2f", key='bal')
            risk_pct = st.number_input(_('risk_pct'), min_value=0.0,
                                       max_value=100.0, step=0.50, format="%.2f", key='rp')
            risk_fraction = risk_pct / 100
            sl_price = st.number_input(_('sl_price'), min_value=0.00,
                                       step=0.1000000, format="%.8f", key='sl')
            tp_price = st.number_input(_('tp_price'), min_value=0.00,
                                       step=0.1000000, format="%.8f", key='tp')

    # Calculate and display results
    if st.button(_('btn_calc'), key='calc'):
        if market == _('spot'):
            res = calculate_spot(buy_price, quantity, buy_fee_rate, sell_price, sell_fee_rate)
            with st.expander(_('res_spot'), expanded=True):
                st.metric(label=_('res_total_cost'), value=f"{res['total_cost']:.4f}", help=_('help_total_cost'))
                st.metric(label=_('res_net_sell'),   value=f"{res['net_sell']:.4f}",   help=_('help_net_sell'))
                st.metric(label=_('res_pnl'),        value=f"{res['pnl']:.4f}",        help=_('help_pnl'))
                st.metric(label=_('res_percent'),    value=f"{res['percent_pnl']:.2f}%", help=_('help_percent'))
                st.metric(label=_('res_break_even'), value=f"{res['break_even']:.4f}", help=_('help_break_even'))
        else:
            res = calculate_futures(entry_price, direction, margin, leverage,
                                     funding_rate, duration, fee_rate,
                                     balance, risk_fraction, sl_price, tp_price)
            with st.expander(_('res_fut'), expanded=True):
                # display futures results with hidden helpers via st.metric
                st.metric(label=_('res_position'), value=f"{res['position_size']:.4f}", help=_('help_position'))
                st.metric(label=_('res_liq'),      value=f"{res['liquidation_price']:.8f}", help=_('help_liq'))
                st.metric(label=_('res_pnl_sl'),   value=f"{res['net_pnl_sl']:.4f}", help=_('help_pnl_sl'))
                st.metric(label=_('res_pnl_tp'),   value=f"{res['net_pnl_tp']:.4f}", help=_('help_pnl_tp'))
                st.metric(label=_('res_rr'),       value=f"{res['risk_reward_ratio']:.2f}", help=_('help_rr'))
                st.metric(label=_('res_sugg'),     value=f"{res['suggested_position']:.4f}", help=_('help_sugg'))
                st.metric(label=_('res_fund'),     value=f"{res['funding_cost']:.4f}", help=_('help_fund'))
                st.metric(label=_('res_comm'),     value=f"{res['commission']:.4f}",     help=_('help_comm'))
                st.metric(label=_('res_roe'),      value=f"{res['roe']:.2f}%",       help=_('help_roe'))

if __name__ == '__main__':
    main()
