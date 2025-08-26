#!/usr/bin/env python3

"""
Stock Portfolio Risk & Return Analysis

1. Pull 5-year daily data for 4-5 stocks + an ETF.
2. Compute monthly log returns.
3. Monte-Carlo simulation of random portfolios (50000 draws).
4. Optimise:
   a) Minimum variance portfolio for a target return.
   b) Maximum Sharpe ratio portfolio.
5. Plot the efficient frontier and highlight optimal points.

Author: <your name>
Date: 2025-08-26
"""

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# ------------------------------------------------------------------
# 1️⃣ Parameters & Data Pull
# ------------------------------------------------------------------
TICKERS = [ <LIST OF TICKERS> ]  # change if desired
PERIOD = '5y'  # last 5 years
TARGET_RET_MONTHLY = 0.01  # ≈ 12% annualised (more realistic)

print("Downloading stock data...")
# Pull adjusted close prices with better error handling
try:
    data = yf.download(TICKERS, period=PERIOD, progress=False)
    print(f"Downloaded data shape: {data.shape}")
    print(f"Data columns: {data.columns.tolist()}")

    # Handle different data structures from yfinance
    if len(TICKERS) == 1:
        # Single ticker case - data might be a simple DataFrame
        if 'Adj Close' in data.columns:
            prices = pd.DataFrame(data['Adj Close'])
            prices.columns = TICKERS
        else:
            # If no 'Adj Close' column, use the entire DataFrame (it might be just adj close)
            prices = data.copy()
            if len(prices.columns) == 1:
                prices.columns = TICKERS
    else:
        # Multiple tickers case
        if isinstance(data.columns, pd.MultiIndex):
            # Multi-level columns: ('Adj Close', 'AAPL'), ('Adj Close', 'MSFT'), etc.
            if 'Adj Close' in data.columns.get_level_values(0):
                prices = data['Adj Close']
            else:
                # Sometimes yfinance returns data with different structure
                print("Warning: 'Adj Close' not found in expected location.")
                print("Available top-level columns:", data.columns.get_level_values(0).unique().tolist())
                # Try to find close price data
                close_cols = [col for col in data.columns.get_level_values(0).unique()
                              if 'close' in col.lower() or 'adj' in col.lower()]
                if close_cols:
                    print(f"Using column: {close_cols[0]}")
                    prices = data[close_cols[0]]
                else:
                    raise KeyError("Could not find adjusted close price data")
        else:
            # Simple columns case - might happen with single ticker
            prices = data

    print(f"Processed prices shape: {prices.shape}")
    print(f"Price columns: {prices.columns.tolist()}")

except Exception as e:
    print(f"Error downloading data: {e}")
    print("Trying alternative approach...")

    # Alternative approach - download each ticker individually
    prices_list = []
    for ticker in TICKERS:
        try:
            ticker_data = yf.download(ticker, period=PERIOD, progress=False)
            if 'Adj Close' in ticker_data.columns:
                ticker_prices = ticker_data['Adj Close']
            else:
                # Use Close if Adj Close not available
                ticker_prices = ticker_data['Close'] if 'Close' in ticker_data.columns else ticker_data.iloc[:, 0]
            ticker_prices.name = ticker
            prices_list.append(ticker_prices)
            print(f"Successfully downloaded {ticker}")
        except Exception as ticker_error:
            print(f"Failed to download {ticker}: {ticker_error}")

    if prices_list:
        prices = pd.concat(prices_list, axis=1)
        print(f"Alternative download successful. Shape: {prices.shape}")
    else:
        raise Exception("Failed to download any stock data")

# Check for any missing data
if prices.isnull().any().any():
    print("Warning: Missing data detected. Forward filling...")
    prices = prices.fillna(method='pad').dropna()  # 'pad' is equivalent to 'ffill'

print(f"Data shape: {prices.shape}")
print(f"Date range: {prices.index[0].date()} to {prices.index[-1].date()}")

# ------------------------------------------------------------------
# 2️⃣ Monthly log returns
# ------------------------------------------------------------------
# Use 'ME' instead of deprecated 'M' for month-end frequency
try:
    monthly_prices = prices.resample('ME').last()
except ValueError:
    # Fallback to 'M' if 'ME' is not supported in older pandas versions
    monthly_prices = prices.resample('M').last()

log_returns = np.log(monthly_prices / monthly_prices.shift(1)).dropna()

# Ensure we have enough data
if len(log_returns) < 12:
    print(f"Warning: Only {len(log_returns)} months of data available. Results may be unreliable.")
if log_returns.empty:
    raise ValueError("No return data available after processing")

mean_ret = log_returns.mean()  # expected monthly return per stock
cov_matrix = log_returns.cov()  # covariance matrix (monthly)

print(f"\nMonthly log returns shape: {log_returns.shape}")
print(f"Average monthly returns:\n{mean_ret}")

# ------------------------------------------------------------------
# 3️⃣ Monte-Carlo simulation
# ------------------------------------------------------------------
N_SIMULATIONS = 50000
print(f"\nRunning Monte Carlo simulation with {N_SIMULATIONS} portfolios...")

# Get the actual number of assets from our data
n_assets = len(mean_ret)
print(f"Number of assets for portfolio optimization: {n_assets}")

np.random.seed(42)
# Generate random weights that sum to 1 using Dirichlet distribution
weights_mc = np.random.dirichlet(np.ones(n_assets), size=N_SIMULATIONS)

print(f"Generated weights shape: {weights_mc.shape}")
print(f"Mean returns shape: {mean_ret.shape}")
print(f"Sample weight vector sum: {weights_mc[0].sum():.6f}")  # Should be 1.0

# Ensure we have the right number of assets
n_assets = len(mean_ret)
print(f"Number of assets: {n_assets}")
print(f"Mean returns shape: {mean_ret.shape}")
print(f"Covariance matrix shape: {cov_matrix.shape}")
print(f"Weights matrix shape: {weights_mc.shape}")

# Make sure we have the right number of assets for the weights
if weights_mc.shape[1] != n_assets:
    print(f"Regenerating weights matrix to match {n_assets} assets...")
    weights_mc = np.random.dirichlet(np.ones(n_assets), size=N_SIMULATIONS)
    print(f"New weights matrix shape: {weights_mc.shape}")

# Calculate portfolio returns and volatilities
port_ret_mc = np.dot(weights_mc, mean_ret.values)
port_vol_mc = np.sqrt(np.sum((weights_mc @ cov_matrix.values) * weights_mc, axis=1))


# ------------------------------------------------------------------
# 4️⃣ Helper: portfolio statistics
# ------------------------------------------------------------------
def port_stats(w, mean_ret_vec=mean_ret.values, cov_mat=cov_matrix.values):
    """Return (expected return, volatility) for weight vector w."""
    ret = np.dot(w, mean_ret_vec)
    vol = np.sqrt(np.dot(w, np.dot(cov_mat, w)))
    return ret, vol


# ------------------------------------------------------------------
# 5️⃣ Optimisation: Minimum-Variance for a target return
# ------------------------------------------------------------------
def min_variance_obj(w):
    """Objective function - variance (σ²)."""
    return port_stats(w)[1] ** 2


constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # weights sum to 1
    {'type': 'eq', 'fun': lambda w: port_stats(w)[0] - TARGET_RET_MONTHLY}  # target return
]
bounds = [(0, 1) for _ in range(n_assets)]

print(f"\nOptimizing minimum variance portfolio for target return: {TARGET_RET_MONTHLY:.4f}")

result_min_var = minimize(
    min_variance_obj,
    np.ones(n_assets) / n_assets,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints,
    options={'disp': False}
)

if not result_min_var.success:
    print("Warning: Minimum variance optimization may not have converged properly")
    print(f"Optimization message: {result_min_var.message}")

w_min_var = result_min_var.x


# ------------------------------------------------------------------
# 6️⃣ Optimisation: Maximum Sharpe Ratio (risk-free rate ≈ 0)
# ------------------------------------------------------------------
def neg_sharpe_obj(w):
    ret, vol = port_stats(w)
    if vol == 0:
        return -np.inf
    return -ret / vol  # negative because we minimize


print("Optimizing maximum Sharpe ratio portfolio...")

result_max_sharpe = minimize(
    neg_sharpe_obj,
    np.ones(len(TICKERS)) / len(TICKERS),
    method='SLSQP',
    bounds=bounds,
    constraints=[{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}],
    options={'disp': False}
)

if not result_max_sharpe.success:
    print("Warning: Maximum Sharpe optimization may not have converged properly")
    print(f"Optimization message: {result_max_sharpe.message}")

w_max_sharpe = result_max_sharpe.x


# ------------------------------------------------------------------
# 7️⃣ Results & Plot
# ------------------------------------------------------------------
def plot_frontier():
    plt.figure(figsize=(12, 8))

    # Random portfolios
    scatter = plt.scatter(port_vol_mc, port_ret_mc, c=port_ret_mc / port_vol_mc,
                          cmap='viridis', alpha=0.5, s=1, label='Random Portfolios')
    plt.colorbar(scatter, label='Sharpe Ratio')

    # Minimum-variance point
    ret_min, vol_min = port_stats(w_min_var)
    plt.scatter(vol_min, ret_min, marker='*', s=500, color='red',
                edgecolors='black', linewidth=2, label=f'Min-Var (Target: {TARGET_RET_MONTHLY:.3f})')

    # Max Sharpe point
    ret_max, vol_max = port_stats(w_max_sharpe)
    sharpe_max = ret_max / vol_max
    plt.scatter(vol_max, ret_max, marker='*', s=500, color='gold',
                edgecolors='black', linewidth=2, label=f'Max Sharpe ({sharpe_max:.2f})')

    plt.xlabel('Monthly Volatility (Standard Deviation)', fontsize=12)
    plt.ylabel('Monthly Expected Return', fontsize=12)
    plt.title('Efficient Frontier with Optimized Portfolios', fontsize=14, fontweight='bold')
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Add some statistics to the plot
    plt.figtext(0.02, 0.02, f'Simulation: {N_SIMULATIONS:,} random portfolios\n'
                            f'Data period: {prices.index[0].date()} to {prices.index[-1].date()}',
                fontsize=9, ha='left')

    plt.show()


def print_weights(name, w):
    print(f"\n{name} Weights:")
    print("-" * 40)
    total_weight = 0

    # Get the actual ticker names from the data
    actual_tickers = mean_ret.index.tolist()

    for i, (ticker, weight) in enumerate(zip(actual_tickers, w)):
        print(f"  {ticker:5s}: {weight:7.4f} ({weight * 100:6.2f}%)")
        total_weight += weight
    print(f"  Total: {total_weight:7.4f} ({total_weight * 100:6.2f}%)")

    ret, vol = port_stats(w)
    sharpe = ret / vol if vol > 0 else 0
    print(f"Expected Return: {ret:8.6f} ({ret * 12:6.2f}% annualized)")
    print(f"Volatility    : {vol:8.6f} ({vol * np.sqrt(12):6.2f}% annualized)")
    print(f"Sharpe Ratio  : {sharpe:8.4f}")


def print_summary_stats():
    print("\n" + "=" * 60)
    print("PORTFOLIO ANALYSIS SUMMARY")
    print("=" * 60)

    # Data summary
    actual_tickers = mean_ret.index.tolist()
    print(f"Tickers analyzed: {', '.join(actual_tickers)}")
    print(f"Analysis period: {prices.index[0].date()} to {prices.index[-1].date()}")
    print(f"Monthly observations: {len(log_returns)}")

    # Monte Carlo summary
    mc_sharpe = port_ret_mc / port_vol_mc
    print(f"\nMonte Carlo Simulation ({N_SIMULATIONS:,} portfolios):")
    print(f"Return range: {port_ret_mc.min():.4f} to {port_ret_mc.max():.4f}")
    print(f"Volatility range: {port_vol_mc.min():.4f} to {port_vol_mc.max():.4f}")
    print(f"Sharpe ratio range: {mc_sharpe.min():.4f} to {mc_sharpe.max():.4f}")


if __name__ == "__main__":
    # Print summary statistics
    print_summary_stats()

    # Display optimized portfolio weights
    print_weights("Minimum-Variance Portfolio (Target Return)", w_min_var)
    print_weights("Maximum Sharpe Ratio Portfolio", w_max_sharpe)

    # Plot frontier
    print("\nGenerating efficient frontier plot...")
    plot_frontier()