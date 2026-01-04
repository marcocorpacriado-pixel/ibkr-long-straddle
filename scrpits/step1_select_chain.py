from ib_insync import *

# ----------------------------
# Conexión a IBKR
# ----------------------------
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=20)

# ----------------------------
# Definición del subyacente
# ----------------------------
spy = Stock(
    symbol="SPY",
    exchange="SMART",
    currency="USD",
    primaryExchange="ARCA"
)
ib.qualifyContracts(spy)

# ----------------------------
# Solicitud de cadenas de opciones
# ----------------------------
chains = ib.reqSecDefOptParams(
    underlyingSymbol="SPY",
    futFopExchange="",
    underlyingSecType="STK",
    underlyingConId=spy.conId
)

# ----------------------------
# Filtrado de la cadena correcta
#   - Opciones vanilla de SPY
#   - Multiplicador estándar 100
#   - Exchange SMART
# ----------------------------
spy_chains = [
    c for c in chains
    if c.tradingClass == "SPY"
    and c.multiplier == "100"
    and c.exchange == "SMART"
]

if not spy_chains:
    raise RuntimeError("No se encontró una cadena válida de opciones SPY.")

chain = spy_chains[0]

# ----------------------------
# Información básica de la cadena
# ----------------------------
expirations = sorted(chain.expirations)
strikes = sorted(chain.strikes)

print("Cadena seleccionada:")
print("  Exchange     :", chain.exchange)
print("  TradingClass :", chain.tradingClass)
print("  Multiplier   :", chain.multiplier)

print("\nPrimeras expiraciones disponibles:")
print(expirations[:5])

print("\nPrimeros strikes disponibles:")
print(strikes[:10])

ib.disconnect()
