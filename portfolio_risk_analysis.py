import numpy as np
import matplotlib.pyplot as plt

# --- Portfolio parameters ---
np.random.seed(42)
num_assets = 3
num_simulations = 500
num_steps = 252  # trading days
T = 1.0

# Annualized expected returns & volatilities for each asset
mu = np.array([0.10, 0.07, 0.12])  # expected returns
sigma = np.array([0.18, 0.10, 0.22])  # volatilities
weights = np.array([0.4, 0.3, 0.3])  # portfolio weights

# Correlation matrix
corr_matrix = np.array([
    [1.0, 0.2, 0.1],
    [0.2, 1.0, 0.25],
    [0.1, 0.25, 1.0]
])

# Covariance matrix
cov_matrix = np.outer(sigma, sigma) * corr_matrix

dt = T / num_steps

# --- Monte Carlo Simulation ---
portfolio_end_values = []
for _ in range(num_simulations):
    portfolio_value = 100  # initial
    prices = np.ones(num_assets) * portfolio_value / num_assets
    for _ in range(num_steps):
        Z = np.random.multivariate_normal(np.zeros(num_assets), cov_matrix)
        returns = mu * dt + Z * np.sqrt(dt)
        prices *= np.exp(returns)
    portfolio_value = np.dot(weights, prices)
    portfolio_end_values.append(portfolio_value)

# --- Analysis ---
portfolio_end_values = np.array(portfolio_end_values)
mean_final = np.mean(portfolio_end_values)
median_final = np.median(portfolio_end_values)
std_final = np.std(portfolio_end_values)
p5 = np.percentile(portfolio_end_values, 5)
p1 = np.percentile(portfolio_end_values, 1)
p95 = np.percentile(portfolio_end_values, 95)

# Value at Risk (VaR) and Conditional VaR (CVaR)
VaR_95 = mean_final - p5
CVaR_95 = mean_final - np.mean(portfolio_end_values[portfolio_end_values <= p5])

# Risk-adjusted return (Sharpe ratio)
risk_free_rate = 0.04
expected_return = (mean_final - 100) / 100
annual_volatility = std_final / 100
sharpe_ratio = (expected_return - risk_free_rate) / annual_volatility

# Maximum Drawdown estimation (simplified)
drawdowns = 1 - portfolio_end_values / np.maximum.accumulate(portfolio_end_values)
max_drawdown = np.max(drawdowns)

# --- Display Results ---
print("📊 Monte Carlo Portfolio Risk Analysis")
print(f"Expected final value: {mean_final:.2f}")
print(f"Std deviation (Volatility): {std_final:.2f}")
print(f"5th percentile: {p5:.2f}")
print(f"1st percentile: {p1:.2f}")
print(f"VaR (95% conf): {VaR_95:.2f}")
print(f"CVaR (95% conf): {CVaR_95:.2f}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Max Drawdown: {max_drawdown:.2%}")

# --- Plot ---
plt.figure(figsize=(10, 6))
plt.hist(portfolio_end_values, bins=50, color='lightblue', edgecolor='black')
plt.axvline(p5, color='r', linestyle='--', label=f'5% percentile (₵{p5:.2f})')
plt.axvline(mean_final, color='k', linestyle='-', label=f'Mean (₵{mean_final:.2f})')
plt.title("Monte Carlo Portfolio End-Value Distribution")
plt.xlabel("Final Portfolio Value")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
plt.show()
