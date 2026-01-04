from ib_insync import *
from datetime import datetime, date
import calendar

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

    # fallback
    return expirations[0]

def pick_strike_placeholder(strikes):
    strikes = sorted(strikes)
    return strikes[len(strikes)//2]  # strike "central"

# ----------------------------
# Conexión
# ----------------------------
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=23)

# ----------------------------
# Subyacente y chain correcto
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

# ----------------------------
# Selección expiry (mensual)
# ----------------------------
expiry = pick_expiry_monthly(expirations)

# ----------------------------
# Selección strike (placeholder)
# ----------------------------
atm_strike = pick_strike_placeholder(strikes)

print("Expiry (mensual):", expiry)
print("Strike (placeholder):", atm_strike)

# ----------------------------
# Construcción del straddle (Call + Put)
# ----------------------------
call = Option("SPY", expiry, atm_strike, "C", "SMART", tradingClass="SPY")
put  = Option("SPY", expiry, atm_strike, "P", "SMART", tradingClass="SPY")

ib.qualifyContracts(call, put)

print("\nCALL contract:")
print(" ", call)

print("\nPUT contract:")
print(" ", put)

ib.disconnect()
