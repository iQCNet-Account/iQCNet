1. A typing error in Cons.(13e), the channel visiting constraint \
------------------------------------------------------------------------------------------------------------------- \
There is an error in the paper, for the classical request Cons.(13e). The correct (13e) is: \
<img width="367" height="44" alt="wechat_2025-08-22_162457_502" src="https://github.com/user-attachments/assets/821b6a9e-9fda-4b70-8b9a-f14db2b684b2" />

$ \sum\limits_{r} {D_r} {x_{i,j,r}^{k,m,n}} \le D, \quad \sum\limits_{k,m,n} {y_{i,j,\mathfrak{r}}^{k,m,n}} \le 1 $ \
------------------------------------------------------------------------------------------------------------------- \

3. A typing error in Cons.(13g), the fiber capacity visiting constraint \
------------------------------------------------------------------------------------------------------------------------------- \
There is an error in the paper, for the classical request Cons.(13g). The correct (13g) is: \
<img width="358" height="43" alt="wechat_2025-08-22_162510_136" src="https://github.com/user-attachments/assets/fb1922e7-f226-4fb4-ba78-ba02d8fcc00e" />

$ \min (1, \sum\limits_{r,k} {x_{i,j,r}^{k,m,n}})  + \sum\limits_{\mathfrak{r},k} {y_{i,j,\mathfrak{r}}^{k,m,n}}  \leqslant K $ \
------------------------------------------------------------------------------------------------------------------------------- \

5. The integrated formulation is: \
------------------------------------------------------------------------------------------------------------------------------- \
<img width="370" height="606" alt="wechat_2025-08-22_162320_727" src="https://github.com/user-attachments/assets/4f1dcb91-3f33-4d22-89d0-b16a9e08700b" />

\begin{subequations}
	\begin{align} \small
		& obj.: \min \sum\limits{\overline C |{l_{i,j}}|(z_{i,j}-Z_{i,j}^{min})}, \label{pro:obj} \\
		& s.b.: \nonumber \\
		&\left\{
		\begin{aligned}
			& \sum\limits_{j, r,k,m,n} {x_{i,j,r}^{k,m,n}}  = \sum\limits_{j,r,k,m,n} {x_{j,i,r}^{k,m,n}} \\[0.5mm]
			& \sum\limits_{i,k,m,n} {x_{i,d_r,r}^{k,m,n}}  = \sum\limits_{j,k,m,n} {x_{s_r,j,r}^{k,m,n}} = 1 \label{cons: route_connectivity_b} \\[0.5mm]
		\end{aligned}
		\right. \\
        &\left\{
		\begin{aligned}
			& \sum\limits_{j,\mathfrak{r},k,m,n} {y_{i,j,\mathfrak{r}}^{k,m,n}}  = \sum\limits_{j,\mathfrak{r},k,m,n} {y_{j,i,\mathfrak{r}}^{k,m,n}} \\[0.5mm]
			& \sum\limits_{i,k,m,n} {y_{i,d_{\mathfrak{r}},\mathfrak{r}}^{k,m,n}} = \sum\limits_{j,k,m,n} {y_{s_{\mathfrak{r}},j,\mathfrak{r}}^{k,m,n}} = 1 \label{cons: route_connectivity_q} \\[0.5mm]
		\end{aligned}
		\right. \\
		&\left\{
		\begin{aligned}
			& \mathbf{F}_{i,j}^{m,n}(|\mathcal{W}_{i,j}^{m,n}|, |\mathbb{W}_{i,j}^{m,n}|) \to (\mathcal{W}_{i,j}^{m,n}, \mathbb{W}_{i,j}^{m,n}, \sum\limits_{\mathfrak{r},k} \mathbb{D}^{*,k,m,n}_{i,j,\mathfrak{r}}) \\[0.5mm]
			& \sum\limits_{k,m,n} {y_{i,j,\mathfrak{r}}^{k,m,n}} \mathbb{D}^{*,k,m,n}_{i,j,\mathfrak{r}} \ge \mathbb{D}_{\mathfrak{r}} \label{cons: optimal_sum_qubit_transmission_rate} \\
		\end{aligned}
		\right. \\
		& \sum\limits_{r} {D_r} {x_{i,j,r}^{k,m,n}} \le D, \quad \sum\limits_{k,m,n} {y_{i,j,\mathfrak{r}}^{k,m,n}} \le 1 \label{cons: classical_quantum_channel} \\[0.5mm]
        & \sum\limits_{i,j,k,m,n} |{l_{i,j}}| {x_{i,j,r}^{k,m,n}} \le L, \quad \sum\limits_{i,j,k,m,n} |{l_{i,j}}| {y_{i,j,\mathfrak{r}}^{k,m,n}} \le \mathbb{L} \label{cons: classical_quantum_delay} \\[0.5mm]
        & \min (1, \sum\limits_{r,k} {x_{i,j,r}^{k,m,n}})  + \sum\limits_{\mathfrak{r},k} {y_{i,j,\mathfrak{r}}^{k,m,n}}  \leqslant K \label{cons: fiber_capacity} \\[0.5mm]
        & \sum\limits_{m} \left( \min \bigg(1, (\sum\limits_{r,k} {x_{i,j,r}^{k,m,n}} + \sum\limits_{\mathfrak{r},k} {y_{i,j,\mathfrak{r}}^{k,m,n}}) \bigg)\right) \leqslant M \label{cons: cable_capacity} \\[0.5mm]
		& {x_{i,j,r}^{k,m,n}} + {y_{i,j,\mathfrak{r}}^{k,m,n}} \le 1 \label{cons: variable_relationship} \\[0.5mm]
		&\left\{
		\begin{aligned}
			& i,j \in \mathcal{N}, i \ne j, r \in \mathcal{R}, \mathfrak{r} \in \mathbb{R} \\[1mm]
			& 0 < k \le K, 0 < m \le M, 0 < n \le z_{i,j} \\[0.5mm]
                & x,y \in \{0,1\}, z \in \mathbb{Z}^+ \label{cons: variables} \\[0.5mm]
		\end{aligned}
		\right.
	\end{align}
\end{subequations}
