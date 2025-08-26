import math

import pandas as pd

NODE_NUM = 10

LIGHT_SPEED = 300000000 # m/s
# C-band (1530nm-1565nm) = 1530nm-1565nm
# import math
# DELTA_F = abs(LIGHT_SPEED/1530 - LIGHT_SPEED/1565)
# H =  50 # GHz
# CHANNEL_NUM = math.floor(DELTA_F/H)
# print(DELTA_F)
# print(CHANNEL_NUM)

CHANNEL_NUM = 57
K = CHANNEL_NUM
FIBER_NUM = 10
M = FIBER_NUM

# # Baud Rate
# R_s = 32 # GBaud, 32G Baud/s
# # QAM
# M = 64 # 16 bits/Baud
# eta = 2  # Double polarization
# R_b = R_s * 4 * eta
# print(R_b)
R_b = 256 # Gbps

LAMBDA_MID = 1550 # nm
# delta_LAMBDA = (1565-1530)/(CHANNEL_NUM-1)
# print(delta_LAMBDA) # 0.625
# TOTAL_LAMBDA = []
# for i in range(CHANNEL_NUM):
#     TOTAL_LAMBDA.append(1530+i*delta_LAMBDA)
# print(TOTAL_LAMBDA)
TOTAL_LAMBDA = [1530.0, 1530.625, 1531.25, 1531.875, 1532.5, 1533.125, 1533.75, 1534.375, 1535.0, 1535.625, 1536.25, 1536.875, 1537.5, 1538.125, 1538.75, 1539.375, 1540.0, 1540.625, 1541.25, 1541.875, 1542.5, 1543.125, 1543.75, 1544.375, 1545.0, 1545.625, 1546.25, 1546.875, 1547.5, 1548.125, 1548.75, 1549.375, 1550.0, 1550.625, 1551.25, 1551.875, 1552.5, 1553.125, 1553.75, 1554.375, 1555.0, 1555.625, 1556.25, 1556.875, 1557.5, 1558.125, 1558.75, 1559.375, 1560.0, 1560.625, 1561.25, 1561.875, 1562.5, 1563.125, 1563.75, 1564.375, 1565.0]

# Read the standard measurement curve in Fig.2, and conduct the Rho table
# import pandas as pd
# RHO_FIG = pd.read_csv("./wavelength.csv", header=None, names=['wavelength', 'rho'])
# RHO_TABLE = [[0 for j in range(CHANNEL_NUM)] for i in range(CHANNEL_NUM)]
# for i in range(CHANNEL_NUM):
#     for j in range(i, CHANNEL_NUM):
#         q_lambda = TOTAL_LAMBDA[i]
#         b_lambda = TOTAL_LAMBDA[j]
#         _lambda = 1/(1/q_lambda - 1/b_lambda + 1/LAMBDA_MID)
#         closest_idy = (RHO_FIG['wavelength']-_lambda).abs().idxmin()
#         RHO_TABLE[i][j] = RHO_FIG.loc[closest_idy, 'rho'] * math.pow(10, -9)
# for i in range(CHANNEL_NUM):
#     for j in range(i):
#         RHO_TABLE[i][j] = RHO_TABLE[j][i]
# pd.DataFrame(RHO_TABLE).to_csv('./rho.csv', index=False)
RHO = pd.read_csv("./rho.csv", skiprows=0).values

# Radar pulse interval
Ts = 250 * math.pow(10, -12)# ps-->
# Dark count rate of photons for the emitter
gamma_dc = math.pow(10,-7) * math.pow(10,9) # /ns-->s
# Time gateway interval, window time interval
T_d = 100 * math.pow(10, -12) # /ps-->s
p_dc = gamma_dc * T_d


# Plank's constant, J.S, describe the relationship between energy and frequency
h = 6.62607015 * math.pow(10, -34)
# quantum efficiency
eta_d = 0.3
# the energy bandwidth of the quantum receiver
delta_lambda = 3.1 # eV, responding to T_d
# the fiber attenuation coefficient
alpha = 0.2 # dB/km

# The classical transmission data volume limitation of a channel
D = 100
# The delay constraint of the classical request transmission
L = 0.005
# The delay constraint of the quantum request transmission
L_mathbb = 0.000001

