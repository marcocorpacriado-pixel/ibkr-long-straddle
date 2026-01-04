from ib_insync import *

# ----------------------------
# Supuestos de la estrategia
# ----------------------------
N_STRADDLES = 1      # número de straddles
MULTIPLIER = 100     # multiplicador estándar de SPY options

# Placeholder de deltas (ATM teórico)
delta_call = 0.50
delta_put  = -0.50

# Delta total del straddle
delta_straddle = delta_call + delta_put

print("Delta call:", delta_call)
print("Delta put :", delta_put)
print("Delta total straddle:", delta_straddle)

# ----------------------------
# Hedge con el subyacente
# ----------------------------
# Posición necesaria en SPY para neutralizar delta
shares_spy = - delta_straddle * MULTIPLIER * N_STRADDLES

print("\nPosición en SPY para delta-neutral:")
print("Shares SPY:", shares_spy)
