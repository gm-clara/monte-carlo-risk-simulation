# monte_carlo.py
import numpy as np
import matplotlib.pyplot as plt

# Function to simulate stock returns
def simulate_stock_returns(mu, sigma, S0, T, dt, simulations):
    """
    mu: Expected return (annualized)
    sigma: Volatility (annualized)
    S0: Initial stock price
    T: Time horizon (in years)
    dt: Time step (in years)
    simulations: Number of simulations
    """
    num_steps = int(T / dt)
    results = np.zeros((simulations, num_steps))
    for i in range(simulations):
        prices = [S0]
        for t in range(1, num_steps):
            # Simulate next price using Geometric Brownian Motion
            price = prices[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal())
            prices.append(price)
        results[i] = prices
    return results

# Function to calculate VaR (Value at Risk)
def calculate_var(simulated_prices, alpha=0.05):
    """
    alpha: Confidence level (e.g., 0.05 for 95% confidence)
    """
    final_prices = simulated_prices[:, -1]
    sorted_prices = np.sort(final_prices)
    var = sorted_prices[int(alpha * len(sorted_prices))]
    return var

# Visualization function
def plot_simulation(results, var_value):
    plt.figure(figsize=(10, 6))
    plt.plot(results.T, color='lightblue', alpha=0.5)  # Plot all simulations
    plt.axhline(y=var_value, color='red', linestyle='--', label=f'VaR at 5%: {var_value:.2f}')
    plt.title('Monte Carlo Simulation: Portfolio Price Simulation')
    plt.xlabel('Time Steps (Years)')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main Simulation Parameters
mu = 0.08  # Expected annual return (8%)
sigma = 0.2  # Volatility (20%)
S0 = 100  # Initial portfolio value ($100)
T = 1  # Time horizon (1 year)
dt = 1/252  # Daily time step (1 trading day)
simulations = 1000  # Number of simulations

# Run Simulation
simulated_results = simulate_stock_returns(mu, sigma, S0, T, dt, simulations)
VaR = calculate_var(simulated_results)

# Plot the results
plot_simulation(simulated_results, VaR)
