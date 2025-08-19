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

CHANNEL_NUM = 87
K = CHANNEL_NUM
FIBER_NUM = 10
M = FIBER_NUM

# # 符号率 Baud Rate
# R_s = 32 # GBaud, 32G符号/秒
# # 调制阶数 QAM
# M = 64 # 16bits/符号
# eta = 2  # 双偏振
# R_b = R_s * 4 * eta
# print(R_b)
R_b = 256 # Gbps

LAMBDA_MID = 1550 # nm
# delta_LAMBDA = (1565-1530)/(CHANNEL_NUM-1)
# print(delta_LAMBDA) # 0.4069767441860465
# TOTAL_LAMBDA = []
# for i in range(CHANNEL_NUM):
#     TOTAL_LAMBDA.append(1530+i*delta_LAMBDA)
# print(TOTAL_LAMBDA)
TOTAL_LAMBDA = [1530.0, 1530.406976744186, 1530.8139534883721, 1531.2209302325582, 1531.6279069767443, 1532.0348837209303, 1532.4418604651162, 1532.8488372093022, 1533.2558139534883, 1533.6627906976744, 1534.0697674418604, 1534.4767441860465, 1534.8837209302326, 1535.2906976744187, 1535.6976744186047, 1536.1046511627908, 1536.5116279069769, 1536.9186046511627, 1537.3255813953488, 1537.7325581395348, 1538.139534883721, 1538.546511627907, 1538.953488372093, 1539.360465116279, 1539.7674418604652, 1540.1744186046512, 1540.5813953488373, 1540.9883720930231, 1541.3953488372092, 1541.8023255813953, 1542.2093023255813, 1542.6162790697674, 1543.0232558139535, 1543.4302325581396, 1543.8372093023256, 1544.2441860465117, 1544.6511627906978, 1545.0581395348838, 1545.4651162790697, 1545.8720930232557, 1546.2790697674418, 1546.6860465116279, 1547.093023255814, 1547.5, 1547.906976744186, 1548.3139534883721, 1548.7209302325582, 1549.1279069767443, 1549.5348837209303, 1549.9418604651162, 1550.3488372093022, 1550.7558139534883, 1551.1627906976744, 1551.5697674418604, 1551.9767441860465, 1552.3837209302326, 1552.7906976744187, 1553.1976744186047, 1553.6046511627908, 1554.0116279069769, 1554.4186046511627, 1554.8255813953488, 1555.2325581395348, 1555.639534883721, 1556.046511627907, 1556.453488372093, 1556.860465116279, 1557.2674418604652, 1557.6744186046512, 1558.0813953488373, 1558.4883720930231, 1558.8953488372092, 1559.3023255813953, 1559.7093023255813, 1560.1162790697674, 1560.5232558139535, 1560.9302325581396, 1561.3372093023256, 1561.7441860465117, 1562.1511627906978, 1562.5581395348838, 1562.9651162790697, 1563.3720930232557, 1563.7790697674418, 1564.1860465116279, 1564.593023255814, 1565.0]

# 读标准测量曲线表
# import pandas as pd
# RHO_FIG = pd.read_csv("./data/wavelength.csv", header=None, names=['wavelength', 'rho'])
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
# pd.DataFrame(RHO_TABLE).to_csv('./data/rho.csv', index=False)
RHO = pd.read_csv("./data/rho.csv", skiprows=0).values

# 雷达脉动时间间隔
Ts = 250 * math.pow(10, -12)# ps-->
# 发射器得光子暗计数率
gamma_dc = math.pow(10,-7) * math.pow(10,9) # /ns-->s
# 时间网关间隔，窗口时间间隔
T_d = 100 * math.pow(10, -12) # /ps-->s
p_dc = gamma_dc * T_d


# Plank's constant, J.S, 描述能量与频率之间得关系
h = 6.62607015 * math.pow(10, -34)
# quantum efficiency
eta_d = 0.3
# the energy bandwidth of the quantum receiver
delta_lambda = 3.1 # eV, 对应T_d
# the fiber attenuation coefficient
alpha = 0.2 # dB/km

# The classical transmission data volume limitation of a channel
D = 100
# The delay constraint of the classical request transmission
L = 0.005
# The delay constraint of the quantum request transmission
L_mathbb = 0.000001

