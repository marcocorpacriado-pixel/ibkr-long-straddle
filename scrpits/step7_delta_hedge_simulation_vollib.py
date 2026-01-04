import numpy as np
import pandas as pd
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta as bs_delta

S0 = 626.0
K = 626.0
r = 0.0
sigma = 0.20

T_total = 30 / 252
steps = 30
dt = T_total / steps

n_paths = 2000
np.random.seed(42)

Z = np.random.randn(n_paths, steps)
S = np.zeros((n_paths, steps + 1))
S[:, 0] = S0

for t in range(steps):
    S[:, t+1] = S[:, t] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t])

# Orden correcto: (flag, S, K, t, r, sigma)
call0 = bs('c', S0, K, T_total, r, sigma)
put0  = bs('p', S0, K, T_total, r, sigma)
V0 = call0 + put0

delta0 = bs_delta('c', S0, K, T_total, r, sigma) + bs_delta('p', S0, K, T_total, r, sigma)

shares0 = -delta0
cash0 = -V0 - shares0 * S0

final_values = []

for i in range(n_paths):
    shares = shares0
    cash = cash0

    for t in range(steps):
        St = S[i, t]
        T_remain = max(T_total - t * dt, 1e-8)  # evita t=0 exacto

        delta_t = bs_delta('c', St, K, T_remain, r, sigma) + bs_delta('p', St, K, T_remain, r, sigma)

        target_shares = -delta_t
        d_shares = target_shares - shares
        cash -= d_shares * St
        shares = target_shares

    ST = S[i, -1]
    payoff = max(ST - K, 0) + max(K - ST, 0)
    final_values.append(payoff + shares * ST + cash)

df = pd.DataFrame({"FinalValue_Hedged": final_values})
print(df.describe())
