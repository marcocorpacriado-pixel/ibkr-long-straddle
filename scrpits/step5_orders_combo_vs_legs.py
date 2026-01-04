from ib_insync import *
from datetime import datetime, date
import calendar

# ----------------------------
# Helpers: expiración mensual (tercer viernes)
# ----------------------------
def third_friday(year: int, month: int) -> date:
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    fridays = [d for d in c.itermonthdates(year, month)
               if d.month == month and d.weekday() == calendar.FRIDAY]
    return fridays[2]

def pick_expiry_monthly(expirations):
    expirations = sorted(expirations)
    exp_dates = [datetime.strptime(x, "%Y%m%d").date() for x in expirations]
    start = exp_dates[0]
    year, month = start.year, start.month

    for _ in range(12):
        tf = third_friday(year, month)
        if tf in exp_dates:
            return tf.strftime("%Y%m%d")

        month += 1
        if month == 13:
            month = 1
            year += 1

    return expirations[0]  # fallback

def pick_strike_placeholder(strikes):
    strikes = sorted(strikes)
    return strikes[len(strikes)//2]

# ----------------------------
# Conexión
# ----------------------------
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=40)

# ----------------------------
# 1) Subyacente + option chain correcto (SPY vanilla)
# ----------------------------
spy = Stock("SPY", "SMART", "USD", primaryExchange="ARCA")
ib.qualifyContracts(spy)

chains = ib.reqSecDefOptParams("SPY", "", "STK", spy.conId)
chain = next(
    c for c in chains
    if c.tradingClass == "SPY" and c.multiplier == "100" and c.exchange == "SMART"
)

expirations = sorted(chain.expirations)
strikes = sorted(chain.strikes)

expiry = pick_expiry_monthly(expirations)
strike = pick_strike_placeholder(strikes)

# ----------------------------
# 2) Construir straddle (CALL + PUT) y cualificar
# ----------------------------
call = Option("SPY", expiry, strike, "C", "SMART", tradingClass="SPY")
put  = Option("SPY", expiry, strike, "P", "SMART", tradingClass="SPY")
ib.qualifyContracts(call, put)

print("CALL:", call.localSymbol, "conId:", call.conId)
print("PUT :", put.localSymbol,  "conId:", put.conId)

# ----------------------------
# 3) A) STRADDLE COMO COMBO (BAG)
# ----------------------------
combo = Contract()
combo.symbol = "SPY"
combo.secType = "BAG"
combo.currency = "USD"
combo.exchange = "SMART"

combo.comboLegs = [
    ComboLeg(conId=call.conId, ratio=1, action="BUY", exchange="SMART"),
    ComboLeg(conId=put.conId,  ratio=1, action="BUY", exchange="SMART"),
]

combo_order = MarketOrder("BUY", 1)

print("\n--- COMBO (BAG) ---")
print("Combo legs:", combo.comboLegs)
print("Order:", combo_order)

# ----------------------------
# 4) B) PATAS SUELTAS (órdenes separadas)
# ----------------------------
call_order = MarketOrder("BUY", 1)
put_order  = MarketOrder("BUY", 1)

print("\n--- PATAS SUELTAS ---")
print("Call order:", call_order)
print("Put order :", put_order)

# Nota: NO enviamos órdenes reales (no usamos ib.placeOrder)
ib.disconnect()
