# Solidly LP Simulator

This repository contains a simple Python script that simulates providing liquidity to a
Solidly-style constant product AMM. It estimates impermanent loss and trading fees
based on user-supplied parameters.

## Usage

Run the simulator with Python 3:

```bash
python lp_simulator.py --token0 <amount_token0> --token1 <amount_token1> \
    --final_price <token1_per_token0> [--volume <swap_volume>] [--fee_rate <fee_rate>]
```

Arguments:
- `--token0` – Amount of token0 deposited.
- `--token1` – Amount of token1 deposited.
- `--final_price` – Final price of token1 per token0 after the simulated period.
- `--volume` – (Optional) Total swap volume in the pool during the period.
- `--fee_rate` – (Optional) Fee rate applied to each swap. Defaults to 0.0005 (0.05%).

The script prints the final token balances, value of the LP position, impermanent
loss, and fees earned.
