# monte_carlo_portfolio.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# User parameters (changeable)
# ---------------------------
np.random.seed(42)

# Assets: example 3 assets (you can change to N assets)
asset_names = ["Asset_A", "Asset_B", "Asset_C"]

# Initial prices for each asset
S0 = np.array([100.0, 50.0, 20.0])

# Annual expected returns (mu) per asset (as decimals, e.g., 0.08 = 8%)
mu = np.array([0.08, 0.06, 0.12])

# Annual covariance matrix between asset returns (var and cov)
# THIS MUST BE positive-definite. Example cov matrix:
cov = np.array([
    [0.04, 0.006, 0.01],   # var(A)=0.04 => sigma_A=20%
    [0.006, 0.0225, 0.008],# var(B)=0.0225 => sigma_B=15%
    [0.01, 0.008, 0.09]    # var(C)=0.09 => sigma_C=30%
])

# Portfolio weights (must sum to 1)
weights = np.array([0.5, 0.3, 0.2])

# Simulation control
T = 1.0                  # time horizon in years
steps_per_year = 252     # trading days approximation
num_steps = int(T * steps_per_year)
dt = T / num_steps

num_simulations = 2000   # number of Monte Carlo paths

# ---------------------------
# Helper: simulate correlated GBM
# ---------------------------
def simulate_correlated_gbm(S0, mu, cov, T, num_steps, num_simulations):
    """
    Returns simulated price paths of shape (num_simulations, num_steps+1, n_assets)
    """
    n_assets = len(S0)
    dt = T / num_steps

    # Cholesky factorization of covariance matrix (annual)
    L = np.linalg.cholesky(cov)

    # Pre-allocate array
    paths = np.zeros((num_simulations, num_steps + 1, n_assets), dtype=float)
    paths[:, 0, :] = S0

    # Precompute drift term: (mu - 0.5 * var) * dt, where var = diag(cov)
    var = np.diag(cov)
    drift = (mu - 0.5 * var) * dt

    for sim in range(num_simulations):
        S_t = S0.copy()
        for step in range(1, num_steps + 1):
            # independent standard normals
            z = np.random.normal(size=n_assets)
            # correlated normal increment
            correlated = L @ z  # shape (n_assets,)
            shock = correlated * np.sqrt(dt)       # sigma * sqrt(dt) * Z where cov provides sigma^2 & cov
            # geometric Brownian motion update (element-wise)
            S_t = S_t * np.exp(drift + shock)
            paths[sim, step, :] = S_t

    return paths

# Run simulation
paths = simulate_correlated_gbm(S0, mu, cov, T, num_steps, num_simulations)

# Compute portfolio value at each time for each simulation
# portfolio_value = sum(weights * asset_prices)
portfolio_paths = np.einsum('s t a, a -> s t', paths, weights)  # shape (num_simulations, num_steps+1)

# Extract final portfolio values at T
final_values = portfolio_paths[:, -1]

# ---------------------------
# Results summary
# ---------------------------
initial_portfolio_value = np.dot(weights, S0)
mean_final = final_values.mean()
median_final = np.median(final_values)
std_final = final_values.std(ddof=0)

p5 = np.percentile(final_values, 5)
p1 = np.percentile(final_values, 1)
p95 = np.percentile(final_values, 95)

print("Monte Carlo Portfolio Simulation (GBM, correlated assets)")
print(f"Initial portfolio value: {initial_portfolio_value:,.2f}")
print(f"Mean final value (T={T}yr): {mean_final:,.2f}")
print(f"Median final value: {median_final:,.2f}")
print(f"Std of final values: {std_final:,.2f}")
print(f"5th percentile (P5): {p5:,.2f}")
print(f"1st percentile (P1): {p1:,.2f}")
print(f"95th percentile (P95): {p95:,.2f}")

# Value at Risk (VaR) at 95% confidence ~ loss from initial value to 5th percentile
VaR_95 = max(0.0, initial_portfolio_value - p5)
print(f"Estimated VaR (95% conf) over {T} year: {VaR_95:,.2f}")

# ---------------------------
# Plot a sample of simulated portfolio paths
# ---------------------------
plt.figure(figsize=(10,6))
# Plot some sample paths (not all, to avoid clutter)
sample_count = 50
for i in range(sample_count):
    plt.plot(portfolio_paths[i], linewidth=0.8, alpha=0.7)
plt.plot(np.mean(portfolio_paths, axis=0), color='black', linewidth=2.0, label='Mean path')
plt.title("Monte Carlo Simulated Portfolio Paths (sample)")
plt.xlabel("Step (days)")
plt.ylabel("Portfolio Value")
plt.grid(True)
plt.legend()
plt.show()

# Plot histogram of final portfolio values
plt.figure(figsize=(8,5))
plt.hist(final_values, bins=60)
plt.axvline(p5, color='red', linestyle='--', label=f'5th pct: {p5:.2f}')
plt.axvline(mean_final, color='black', linestyle='-', label=f'mean: {mean_final:.2f}')
plt.title("Distribution of Final Portfolio Values")
plt.xlabel("Portfolio Value at T")
plt.ylabel("Frequency")
plt.legend()
plt.show()
