import numpy as np
import matplotlib.pyplot as plt

# Parameters
beta = 0.3      # Infection rate
gamma = 0.1     # Recovery rate
population = 1000
I0, R0 = 1, 0   # Initial infected and recovered
S0 = population - I0 - R0

# Time steps
days = 160
S, I, R = [S0], [I0], [R0]

for day in range(1, days):
    new_infections = beta * S[-1] * I[-1] / population
    new_recoveries = gamma * I[-1]
    
    S_next = S[-1] - new_infections
    I_next = I[-1] + new_infections - new_recoveries
    R_next = R[-1] + new_recoveries
    
    S.append(S_next)
    I.append(I_next)
    R.append(R_next)

# Visualization
plt.plot(S, label='Susceptible', color='blue')
plt.plot(I, label='Infected', color='red')
plt.plot(R, label='Recovered', color='green')
plt.xlabel("Days")
plt.ylabel("Number of People")
plt.title("Virus Spread Simulation (SIR Model)")
plt.legend()
plt.grid(True)
plt.show()
