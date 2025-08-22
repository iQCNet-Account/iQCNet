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

# Define the flow reservation constraint for the classical request
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

# Define the flow reservation constraint for the quantum request
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


# Define the transmission requirement of the quantum request
# Constraint (13d) --> Constraint (18,19)
# -------------------------------------------------------------------------------------------------------------------------------
# 1. Add the auxiliary variable w_{i,j,r,r'}^{k,kk,m,n}, v_{i,j,r,r'}^{k,kk,ll,m,n}
w = model.addVars(NODE_NUM, NODE_NUM, CR_NUM, QR_NUM, CHANNEL_NUM, CHANNEL_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="w")
v = model.addVars(NODE_NUM, NODE_NUM, CR_NUM, QR_NUM, CHANNEL_NUM, CHANNEL_NUM, CHANNEL_NUM, FIBER_NUM, N_NUM, vtype=gp.GRB.BINARY, name="v")
model.addConstrs(
    w[i,j,r,rr,k,kk,m,n] <= y[i,j,rr,k,m,n]
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for rr in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for kk in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    w[i,j,r,rr,k,kk,m,n] <= x[i,j,r,kk,m,n]
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for rr in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for kk in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    w[i,j,r,rr,k,kk,m,n] >= y[i,j,rr,k,m,n] + x[i,j,r,k,m,n] - 1
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for rr in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for kk in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
)
model.addConstrs(
    v[i,j,r,rr,k,kk,ll,m,n] >= w[i,j,r,rr,k,kk,m,n]
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for rr in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for kk in range(CHANNEL_NUM)
    for ll in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    if kk <= ll
)
model.addConstrs(
    v[i,j,r,rr,k,kk,ll,m,n] >= w[i,j,r,rr,k,ll,m,n]
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for rr in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for kk in range(CHANNEL_NUM)
    for ll in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    if kk <= ll
)
model.addConstrs(
    v[i,j,r,rr,k,kk,ll,m,n] >= w[i,j,r,rr,k,kk,m,n] + w[i,j,r,rr,k,ll,m,n] - 1
    for i in range(NODE_NUM)
    for j in range(NODE_NUM)
    for r in range(CR_NUM)
    for rr in range(QR_NUM)
    for k in range(CHANNEL_NUM)
    for kk in range(CHANNEL_NUM)
    for ll in range(CHANNEL_NUM)
    for m in range(FIBER_NUM)
    for n in range(N_NUM)
    if kk <= ll
)


# D_ijr_kmn = P(p_ij_kmn)/Ts = (1-math.pow((1-(p_dc + p_ij_kmn)), 2))/Ts
#
# # 激光器的发射功率
# I = math.pow(10, -3.5 + (alpha * edge[i][j])/10) # mW
#
# gamma_ij_wmn = I * math.exp(-alpha * edge[i][j]) * edge[i][j] * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)
# gamma_ji_wmn = I * ((1-math.exp(-2*alpha*edge[i][j]))/(2*alpha)) * delta_lambda * T_d * eta_d / (2 * h * LIGHT_SPEED)
# p_ij_kmn = gamma_ij_wmn * ()
# -------------------------------------------------------------------------------------------------------------------

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

# The fiber capacity constraint
# Constraint (13g) --> Constraint (20)
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

# The cable capacity constraint
# Constraint (13h) --> Constraint (21)
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

# The visiting conflict on a channel
# Constraint (13d) --> Constraint (18,19)
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
