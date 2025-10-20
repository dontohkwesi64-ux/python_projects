import simpy
import random
import statistics

# --- Simulation Parameters ---
RANDOM_SEED = 42
NUM_TELLERS = 2          # Number of bank tellers
SIM_TIME = 60            # Simulation time (in minutes)
ARRIVAL_INTERVAL = 5     # Time between customer arrivals (avg)
SERVICE_TIME = 8         # Avg service time per customer

wait_times = []          # To record how long each customer waits


def customer(env, name, bank):
    """Each customer arrives, waits, and is served."""
    arrival_time = env.now
    print(f"{name} arrives at the bank at {arrival_time:.2f} minutes.")

    with bank.request() as request:
        yield request  # Wait for an available teller
        wait = env.now - arrival_time
        wait_times.append(wait)

        print(f"{name} starts being served at {env.now:.2f} (waited {wait:.2f} mins).")
        yield env.timeout(random.expovariate(1.0 / SERVICE_TIME))
        print(f"{name} leaves the bank at {env.now:.2f}.")


def setup(env, num_tellers, arrival_interval):
    """Create a bank, some tellers, and keep generating customers."""
    bank = simpy.Resource(env, num_tellers)

    # Create customers as long as simulation runs
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        i += 1
        env.process(customer(env, f"Customer {i}", bank))


# --- Run Simulation ---
print("🏦 Bank Queue Simulation — Event-Driven Model")
random.seed(RANDOM_SEED)
env = simpy.Environment()
env.process(setup(env, NUM_TELLERS, ARRIVAL_INTERVAL))
env.run(until=SIM_TIME)

# --- Results ---
average_wait = statistics.mean(wait_times)
print(f"\nAverage wait time: {average_wait:.2f} minutes")
print(f"Total customers served: {len(wait_times)}")
