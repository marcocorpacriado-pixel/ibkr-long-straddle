import numpy as np
import pandas as pd

# ----------------------------
# Parámetros de simulación
# ----------------------------
S0 = 626.0        # spot inicial (placeholder coherente con el strike)
K = 626.0         # strike ATM
T = 30/252        # 30 días a vencimiento
r = 0.0
sigma = 0.20      # volatilidad anual
N_PATHS = 10000

# ----------------------------
# Simulación del subyacente
# ----------------------------
np.random.seed(42)
Z = np.random.randn(N_PATHS)
ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

# ----------------------------
# Payoff del straddle
# ----------------------------
call_payoff = np.maximum(ST - K, 0)
put_payoff  = np.maximum(K - ST, 0)
straddle_payoff = call_payoff + put_payoff

# ----------------------------
# Resultados
# ----------------------------
results = pd.DataFrame({
    "ST": ST,
    "Call": call_payoff,
    "Put": put_payoff,
    "Straddle": straddle_payoff
})

print(results.describe())
