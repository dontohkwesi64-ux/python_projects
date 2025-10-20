# monte_carlo_retirement.py
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# User parameters (change)
# -------------------------
np.random.seed(42)

# Economic assumptions (annual, in decimals)
mu = 0.06            # expected nominal return (6%)
sigma = 0.12         # annual volatility (12%)
inflation = 0.02     # annual inflation (2%)

# Timing
years_to_retirement = 20
retirement_years = 30
years_total = years_to_retirement + retirement_years

# Cash flow
initial_portfolio = 200000.0    # starting savings (₵ or $)
annual_contribution = 10000.0   # contribution each year pre-retirement (nominal)
withdrawal_real = 40000.0       # desired real withdrawal per year in retirement (today's purchasing power)

# Simulation control
num_simulations = 5000
plot_sample_paths = 50

# -------------------------
# Helper: single simulation
# -------------------------
def run_single_simulation():
    """
    Returns:
      balances: array of portfolio values for each year (length years_total+1)
      ruined: boolean whether portfolio ran out (balance < 0) during retirement
      ruin_year: year of ruin (None if never)
    """
    balances = np.zeros(years_total + 1)
    balances[0] = initial_portfolio

    # We'll convert target withdrawal to nominal each retirement year using inflation
    # withdrawal in nominal in year t (t counted from 0 at start)
    ruined = False
    ruin_year = None

    for year in range(1, years_total + 1):
        # Pre-retirement: years 1..years_to_retirement
        if year <= years_to_retirement:
            # end-of-year contribution model:
            # 1) apply returns to current balance for the year
            r = np.random.normal(mu, sigma)
            balances[year] = balances[year-1] * (1 + r)
            # 2) add contribution at end of year
            balances[year] += annual_contribution
        else:
            # Retirement years: withdrawals then returns (conservative)
            # compute nominal withdrawal this year (inflate the real withdrawal)
            yrs_into_ret = year - years_to_retirement - 1  # 0-based within retirement
            nominal_withdrawal = withdrawal_real * ((1 + inflation) ** yrs_into_ret)
            # withdraw at start of year
            balance_after_withdraw = balances[year-1] - nominal_withdrawal
            if balance_after_withdraw <= 0:
                # ruin immediately
                balances[year] = balance_after_withdraw
                ruined = True
                ruin_year = year
                # we still keep simulating negative balances to record severity, or break early
                # break
                # For tracking we stop at ruin and fill remainder with negative marks
                for rem in range(year+1, years_total+1):
                    balances[rem] = balances[year]  # stays negative
                return balances, ruined, ruin_year
            # apply returns for the year
            r = np.random.normal(mu, sigma)
            balances[year] = balance_after_withdraw * (1 + r)

    return balances, ruined, ruin_year

# -------------------------
# Run Monte Carlo
# -------------------------
all_final_balances = np.zeros(num_simulations)
ruin_flags = np.zeros(num_simulations, dtype=bool)
ruin_years = []

# For plotting a selection of paths
sample_paths = []

for i in range(num_simulations):
    balances, ruined, ruin_year = run_single_simulation()
    all_final_balances[i] = balances[-1]
    ruin_flags[i] = ruined
    ruin_years.append(ruin_year if ruin_year is not None else np.nan)
    if i < plot_sample_paths:
        sample_paths.append(balances)

# -------------------------
# Results & metrics
# -------------------------
success_rate = 1.0 - ruin_flags.mean()
median_final = np.median(all_final_balances)
mean_final = all_final_balances.mean()
p5 = np.percentile(all_final_balances, 5)
p1 = np.percentile(all_final_balances, 1)
p95 = np.percentile(all_final_balances, 95)

print("Monte Carlo Retirement Simulation")
print(f"Simulations: {num_simulations}")
print(f"Initial portfolio: {initial_portfolio:,.2f}")
print(f"Annual contribution (pre-ret): {annual_contribution:,.2f}")
print(f"Desired real withdrawal (retirement start): {withdrawal_real:,.2f} per year")
print(f"Years to retirement: {years_to_retirement}, retirement years: {retirement_years}")
print(f"Assumed mu={mu:.2%}, sigma={sigma:.2%}, inflation={inflation:.2%}")
print()
print(f"Probability of success (not ruined during retirement): {success_rate:.2%}")
print(f"Mean final balance after {years_total} years: {mean_final:,.2f}")
print(f"Median final balance: {median_final:,.2f}")
print(f"5th percentile: {p5:,.2f}")
print(f"1st percentile: {p1:,.2f}")
print(f"95th percentile: {p95:,.2f}")
print(f"Number of ruined sims: {ruin_flags.sum()}")

# Basic ruin-year distribution (for those that ruined)
ruin_years_arr = np.array([y for y in ruin_years if not np.isnan(y)])
if ruin_years_arr.size > 0:
    print(f"Earliest ruin year: {int(np.nanmin(ruin_years_arr))}")
    print(f"Median ruin year: {int(np.nanmedian(ruin_years_arr))}")

# -------------------------
# Plots
# -------------------------
plt.figure(figsize=(10,6))
for path in sample_paths:
    plt.plot(path, alpha=0.6)
plt.title("Sample portfolio trajectories (first {} sims)".format(plot_sample_paths))
plt.xlabel("Year")
plt.ylabel("Nominal portfolio value")
plt.grid(True)
plt.axvline(years_to_retirement, color='k', linestyle='--', label='Retirement start')
plt.legend([f"Sample path (n={len(sample_paths)})", "Retirement start"], loc='upper left')
plt.show()

plt.figure(figsize=(8,5))
plt.hist(all_final_balances, bins=60, edgecolor='k')
plt.title("Histogram of final portfolio balances")
plt.xlabel("Final portfolio value (nominal)")
plt.ylabel("Frequency")
plt.axvline(p5, color='red', linestyle='--', label=f'5th pct: {p5:.0f}')
plt.axvline(median_final, color='black', linestyle='-', label=f'median: {median_final:.0f}')
plt.legend()
plt.grid(True)
plt.show()

# Ruin year histogram
if ruin_years_arr.size > 0:
    plt.figure(figsize=(8,4))
    plt.hist(ruin_years_arr - years_to_retirement, bins=range(0, retirement_years+2), edgecolor='k')
    plt.title("Ruin occurrences by retirement-year (years since retirement start)")
    plt.xlabel("Years since retirement start")
    plt.ylabel("Number of simulations that ruined in that year")
    plt.grid(True)
    plt.show()
