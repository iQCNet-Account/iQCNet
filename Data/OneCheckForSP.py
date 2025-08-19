import gurobipy as gp
from gurobipy import GRB
from tools import *
from topologyAndRequest import *

N_NUM = 5
CR_NUM = len(cr)
QR_NUM = len(qr)

# define the optimization model
model = gp.Model("Complex_MINLP")
# define the six-dimensional variable
# visit the variable by using x[0,0,0,0,0,0], x[0,0,1,0,0,0], ..., x[1,2,3,0,0,0],...
x = model.addVars(NODE_NUM, NODE_NUM, CR_NUM, CHANNEL_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="x")
y = model.addVars(NODE_NUM, NODE_NUM, QR_NUM, CHANNEL_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="y")
# define the objective
model.setObjective(0, gp.GRB.MINIMIZE)

# define the flow reservation constraint for the classical request
# Constraint (13b)
model.addConstrs(
    gp.quicksum(
            x[i,j,r,k,m,n]
            for j in range(NODE_NUM)
            for r in range(CR_NUM)
            for k in range(CHANNEL_NUM)
            for m in range(FIBER_NUM)
            for n in range(N_NUM)
        ) == gp.quicksum(
            x[j,i,r,k,m,n]
            for j in range(NODE_NUM)
            for r in range(CR_NUM)
            for k in range(CHANNEL_NUM)
            for m in range(FIBER_NUM)
            for n in range(N_NUM)
    )
    for i in range(NODE_NUM)
)
model.addConstrs(
    gp.quicksum(
        x[i,cr[r][1],r,k,m,n]
        for i in range(NODE_NUM)
        for k in range(CHANNEL_NUM)
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) == 1
    for r in range(CR_NUM)
)
model.addConstrs(
    gp.quicksum(
        x[cr[r][1],j,r,k,m,n]
        for j in range(NODE_NUM)
        for k in range(CHANNEL_NUM)
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) == 1
    for r in range(CR_NUM)
)

# define the flow reservation constraint for the quantum request
# Constraint (13c)
model.addConstrs(
    gp.quicksum(
            y[i,j,r,k,m,n]
            for j in range(NODE_NUM)
            for r in range(QR_NUM)
            for k in range(CHANNEL_NUM)
            for m in range(FIBER_NUM)
            for n in range(N_NUM)
        ) == gp.quicksum(
            x[j,i,r,k,m,n]
            for j in range(NODE_NUM)
            for r in range(QR_NUM)
            for k in range(CHANNEL_NUM)
            for m in range(FIBER_NUM)
            for n in range(N_NUM)
    )
    for i in range(NODE_NUM)
)
model.addConstrs(
    gp.quicksum(
        x[i,cr[r][1],r,k,m,n]
        for i in range(NODE_NUM)
        for k in range(CHANNEL_NUM)
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) == 1
    for r in range(QR_NUM)
)
model.addConstrs(
    gp.quicksum(
        x[cr[r][1],j,r,k,m,n]
        for j in range(NODE_NUM)
        for k in range(CHANNEL_NUM)
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) == 1
    for r in range(QR_NUM)
)

# define the transmission requirement of the quantum request
# Constraint (13d)
model.addConstrs(
    gp.quicksum(
        y[i,j,r,k,m,n] * (
            math.pow((
                (
                    gp.quicksum(
                        ((math.pow(10, -3.5 + (alpha * edge[i][j])/10)) * math.exp(-alpha * edge[i][j]) * edge[i][j] * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)) *
                        x[i,j,r,kk,m,n] * TOTAL_LAMBDA[k] * RHO[kk][k]
                        +
                        ((math.pow(10, -3.5 + (alpha * edge[i][j])/10)) * ((1-math.exp(-2*alpha*edge[i][j]))/(2*alpha)) * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)) *
                        x[j,i,r,kk,m,n] * TOTAL_LAMBDA[k] * RHO[kk][k]
                    )
                    for kk in range(CHANNEL_NUM)
                )
            ),2) - 2*(1-p_dc)*(
                (
                    gp.quicksum(
                        ((math.pow(10, -3.5 + (alpha * edge[i][j])/10)) * math.exp(-alpha * edge[i][j]) * edge[i][j] * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)) *
                        x[i,j,r,kk,m,n] * TOTAL_LAMBDA[k] * RHO[kk][k]
                        +
                        ((math.pow(10, -3.5 + (alpha * edge[i][j])/10)) * ((1-math.exp(-2*alpha*edge[i][j]))/(2*alpha)) * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)) *
                        x[j,i,r,kk,m,n] * TOTAL_LAMBDA[k] * RHO[kk][k]
                    )
                    for kk in range(CHANNEL_NUM)
                )
        ) - (2*p_dc-math.pow(p_dc,2))
        )
        for k in range(CHANNEL_NUM)
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) <= qr[r][2] * Ts
    for r in range(QR_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
)

# D_ijr_kmn = P(p_ij_kmn)/Ts = (1-math.pow((1-(p_dc + p_ij_kmn)), 2))/Ts
#
# # 激光器的发射功率
# I = math.pow(10, -3.5 + (alpha * edge[i][j])/10) # mW
#
# gamma_ij_wmn = I * math.exp(-alpha * edge[i][j]) * edge[i][j] * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)
# gamma_ji_wmn = I * ((1-math.exp(-2*alpha*edge[i][j]))/(2*alpha)) * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)
# p_ij_kmn = gamma_ij_wmn * ()

# channel visiting constraint
# Constraint (13e)
# -------------------------------------------------------------------------------------------------------------------
# there is an error in the paper, for the classical request Cons.(13e). The correct (13e) is:
# $ \sum\limits_{r} {D_r} {x_{i,j,r}^{k,m,n}} \le D, \quad \sum\limits_{k,m,n} {y_{i,j,\mathfrak{r}}^{k,m,n}} \le 1 $
# -------------------------------------------------------------------------------------------------------------------
model.addConstrs(
    gp.quicksum(
        cr[r][2] * x[i,j,r,k,m,n]
        for r in range(CR_NUM)
        ) <= D
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
)
model.addConstrs(
    gp.quicksum(
        y[i,j,r,k,m,n]
        for k in range(CHANNEL_NUM)
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
        ) <= 1
    for r in range(QR_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
)

# The delay constraints of the quantum and classical constraint
# Constraint (13f)
model.addConstrs(
    gp.quicksum(
    edge[i][j] * x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    ) <= L
    for r in range(CR_NUM)
)
model.addConstrs(
    gp.quicksum(
    edge[i][j] * x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    ) <= L_mathbb
    for r in range(CR_NUM)
)

# the fiber capacity constraint
#  Constraint (13g) --> Constraint (20)
# -------------------------------------------------------------------------------------------------------------------------------
# there is an error in the paper, for the classical request Cons.(13g). The correct (13g) is:
# $ \min (1, \sum\limits_{r,k} {x_{i,j,r}^{k,m,n}})  + \sum\limits_{\mathfrak{r},k} {y_{i,j,\mathfrak{r}}^{k,m,n}}  \leqslant K $
# -------------------------------------------------------------------------------------------------------------------------------
# 1. Add the auxiliary variable
s = model.addVars(NODE_NUM, NODE_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="s")
# 2. Transform the constraint
model.addConstrs(
    s[i,j,m,n] <=
    gp.quicksum(
    x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for r in range(CR_NUM)
    )
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    gp.quicksum(
    x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for r in range(CR_NUM)
    ) <= CR_NUM * K * s[i,j,m,n]
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    s[i,j,m,n] +
    gp.quicksum(
    x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for r in range(CR_NUM)
    ) <= K
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)

# the cable capacity constraint
#  Constraint (13h) --> Constraint (21)
# -------------------------------------------------------------------------------------------------------------------------------
# 1. Add the auxiliary variable
o = model.addVars(NODE_NUM, NODE_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="o")
# 2. Transform the constraint
model.addConstrs(
    o[i,j,m,n] >= x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
)
model.addConstrs(
    o[i,j,m,n] >= y[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(QR_NUM)
)
model.addConstrs(
    gp.quicksum(
    x[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for r in range(CR_NUM)
    ) + gp.quicksum(
    y[i,j,r,k,m,n]
    for k in range(CHANNEL_NUM)
    for r in range(QR_NUM)
    ) >= o[i,j,m,n]
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    gp.quicksum(
    o[i,j,m,n]
    for m in range(FIBER_NUM)
    ) <= M
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for n in range(N_NUM)
)


# 定义一个请求（传统+量子）默认不能跨光纤响应，只能在一个光纤里被满足
o = model.addVars(CR_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="o")
model.addConstrs(
    gp.quicksum(
        o[r,m,n]
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) == 1
    for r in range(CR_NUM)
)
model.addConstrs(
    x[i,j,r,k,m,n] - o[r,m,n] <= 0
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
_o = model.addVars(QR_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="_o")
model.addConstrs(
    gp.quicksum(
        _o[r,m,n]
        for m in range(FIBER_NUM)
        for n in range(N_NUM)
    ) == 1
    for r in range(QR_NUM)
)
model.addConstrs(
    y[i,j,r,k,m,n] - _o[r,m,n] <= 0
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)

# 每根光纤里的信道数据量约束
model.addConstrs(
    gp.quicksum(
        x[i,j,r,k,m,n]
        for r in range(CR_NUM)
        for k in range(CHANNEL_NUM)
    ) + gp.quicksum(
        y[i,j,_r,k,m,n]
        for _r in range(QR_NUM)
        for k in range(CHANNEL_NUM)
    ) <= CHANNEL_NUM
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)

# 两个节点之间的一根光纤中的光缆数量约束
model.addConstrs(
    gp.quicksum(
        o[r,m,n]
        for r in range(CR_NUM)
    ) <= FIBER_NUM
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    gp.quicksum(
        _o[r,m,n]
        for r in range(QR_NUM)
    ) <= FIBER_NUM
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)

# 每个信道被访问的冲突约束
model.addConstrs(
    x[i,j,r,k,m,n] + y[i,j,_r,k,m,n] <= 1
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for _r in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)

)

model.optimize()
if model.status == gp.GRB.OPTIMAL:
    print("The feasible solution space exist!")
else:
    print("No feasible solution space!")






# # 转化为有向边（双向）
# directed_edges = []
# for (u, v) in undirected_edges:
#     directed_edges.append((u, v))
#     directed_edges.append((v, u))
#
# # 容量和成本（假设双向对称）
# capacity = {}
# cost = {}
# for (u, v) in directed_edges:
#     capacity[u, v] = 3  # 统一容量
#     cost[u, v] = 2 if u == 0 or v == 0 else 1  # 假设中心节点0成本较高
#
# commodities = [1, 2]
# demand = {1: 2, 2: 1}  # 商品需求
# source = {1: 0, 2: 1}
# sink = {1: 3, 2: 3}
#
# # 创建模型
# model = gp.Model("Undirected_IMCF")
#
# # 变量：商品k在边u->v上的流量（整数）
# flow = {}
# for k in commodities:
#     for (u, v) in directed_edges:
#         flow[k, u, v] = model.addVar(vtype=GRB.INTEGER, name=f"flow_{k}_{u}_{v}")
#
# # 目标：最小化总成本
# model.setObjective(
#     gp.quicksum(cost[u, v] * flow[k, u, v] for k in commodities for (u, v) in directed_edges),
#     GRB.MINIMIZE
# )
#
# # 约束1：边容量（双向边独立计算）
# for (u, v) in directed_edges:
#     model.addConstr(
#         gp.quicksum(flow[k, u, v] for k in commodities) <= capacity[u, v],
#         name=f"cap_{u}_{v}"
#     )
#
# # 约束2：流量守恒
# for k in commodities:
#     for v in nodes:
#         outflow = gp.quicksum(flow[k, v, j] for (i, j) in directed_edges if i == v)
#         inflow = gp.quicksum(flow[k, i, v] for (i, j) in directed_edges if j == v)
#         if v == source[k]:
#             model.addConstr(outflow - inflow == demand[k], name=f"source_{k}_{v}")
#         elif v == sink[k]:
#             model.addConstr(outflow - inflow == -demand[k], name=f"sink_{k}_{v}")
#         else:
#             model.addConstr(outflow - inflow == 0, name=f"transit_{k}_{v}")
#
# # 求解
# model.optimize()
#
# # 输出结果
# if model.status == GRB.OPTIMAL:
#     print("最优解：")
#     for k in commodities:
#         print(f"\n商品 {k}:")
#         for (u, v) in directed_edges:
#             if flow[k, u, v].x > 0:
#                 print(f"  {u}->{v}: {flow[k, u, v].x}")
# else:
#     print("未找到可行解")