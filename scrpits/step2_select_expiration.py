from ib_insync import *
from datetime import datetime, date
import calendar

def third_friday(year: int, month: int) -> date:
    """
    Devuelve el tercer viernes de un mes concreto.
    """
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    fridays = [d for d in c.itermonthdates(year, month)
               if d.month == month and d.weekday() == calendar.FRIDAY]
    return fridays[2]  # tercer viernes

def pick_expiry(expirations, mode="monthly"):
    """
    mode:
      - 'nearest': devuelve la expiración más cercana (mínima).
      - 'monthly': intenta elegir el tercer viernes más cercano disponible.
                  Si no existe en la lista, hace fallback a 'nearest'.
    """
    expirations = sorted(expirations)
    exp_dates = [datetime.strptime(x, "%Y%m%d").date() for x in expirations]

    if mode == "nearest":
        return expirations[0]

    # mode == "monthly"
    # Buscamos el primer tercer viernes (del mes de la expiración más cercana, o siguientes meses)
    # que esté disponible en exp_dates.
    # Ventana de búsqueda: próximos 12 meses a partir del primer vencimiento disponible.
    start = exp_dates[0]
    year, month = start.year, start.month

    for _ in range(12):
        tf = third_friday(year, month)
        if tf in exp_dates:
            return tf.strftime("%Y%m%d")
        # avanzar un mes
        month += 1
        if month == 13:
            month = 1
            year += 1

    # Fallback
    return expirations[0]

# ----------------------------
# Conexión a IBKR
# ----------------------------
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=22)

spy = Stock("SPY", "SMART", "USD", primaryExchange="ARCA")
ib.qualifyContracts(spy)

chains = ib.reqSecDefOptParams("SPY", "", "STK", spy.conId)

chain = next(
    c for c in chains
    if c.tradingClass == "SPY" and c.multiplier == "100" and c.exchange == "SMART"
)

expirations = sorted(chain.expirations)

selected_monthly = pick_expiry(expirations, mode="monthly")
selected_nearest = pick_expiry(expirations, mode="nearest")

print("Expiración seleccionada (monthly con fallback):", selected_monthly)
print("Expiración más cercana (nearest):", selected_nearest)

ib.disconnect()
