import random
import matplotlib.pyplot as plt

# Number of random points
num_points = 10000
inside_circle = 0

x_inside, y_inside = [], []
x_outside, y_outside = [], []

for _ in range(num_points):
    x, y = random.random(), random.random()
    distance = x**2 + y**2
    if distance <= 1:
        inside_circle += 1
        x_inside.append(x)
        y_inside.append(y)
    else:
        x_outside.append(x)
        y_outside.append(y)

# Estimate of Pi
pi_estimate = 4 * inside_circle / num_points
print(f"Estimated π ≈ {pi_estimate}")

# Visualization
plt.figure(figsize=(6, 6))
plt.scatter(x_inside, y_inside, color="blue", s=2, label="Inside Circle")
plt.scatter(x_outside, y_outside, color="red", s=2, label="Outside Circle")
plt.title(f"Monte Carlo Estimation of π ≈ {pi_estimate}")
plt.legend()
plt.show()
