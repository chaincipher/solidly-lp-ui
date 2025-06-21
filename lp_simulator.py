import argparse
import math


def simulate_lp(token0_amount, token1_amount, final_price, volume=0.0, fee_rate=0.0005):
    """Simulate providing liquidity to a constant product pool.

    Args:
        token0_amount (float): Initial amount of token0 deposited.
        token1_amount (float): Initial amount of token1 deposited.
        final_price (float): Final price of token1 per token0 after arbitrage.
        volume (float, optional): Total swap volume during the period. Defaults to 0.0.
        fee_rate (float, optional): Fee rate per swap (e.g. 0.0005 for 0.05%%). Defaults to 0.0005.

    Returns:
        dict: Results including final token amounts, values, and impermanent loss.
    """
    if token0_amount <= 0 or token1_amount <= 0:
        raise ValueError("Token amounts must be positive")
    if final_price <= 0:
        raise ValueError("Final price must be positive")

    # Constant product
    k = token0_amount * token1_amount

    # Pool rebalances to match the external price via arbitrage
    token0_final = math.sqrt(k / final_price)
    token1_final = final_price * token0_final

    # Value if simply holding the tokens
    value_if_hold = token0_amount * final_price + token1_amount

    # Value of LP position after price change
    value_after = token0_final * final_price + token1_final

    # Impermanent loss compared to holding
    impermanent_loss = (value_after / value_if_hold) - 1

    # Trading fees earned (assumes 100% share of pool)
    fees_earned = volume * fee_rate

    total_value_with_fees = value_after + fees_earned

    return {
        "token0_final": token0_final,
        "token1_final": token1_final,
        "value_if_hold": value_if_hold,
        "value_after": value_after,
        "impermanent_loss": impermanent_loss,
        "fees_earned": fees_earned,
        "total_value_with_fees": total_value_with_fees,
    }


def main():
    parser = argparse.ArgumentParser(description="Simulate LP returns on a Solidly-style DEX")
    parser.add_argument("--token0", type=float, required=True, help="Initial amount of token0 deposited")
    parser.add_argument("--token1", type=float, required=True, help="Initial amount of token1 deposited")
    parser.add_argument("--final_price", type=float, required=True, help="Final price of token1 per token0")
    parser.add_argument("--volume", type=float, default=0.0, help="Total swap volume during the period")
    parser.add_argument("--fee_rate", type=float, default=0.0005, help="Fee rate per swap (e.g. 0.0005 for 0.05%%)")

    args = parser.parse_args()

    results = simulate_lp(
        token0_amount=args.token0,
        token1_amount=args.token1,
        final_price=args.final_price,
        volume=args.volume,
        fee_rate=args.fee_rate,
    )

    print("Final token0:", results["token0_final"])
    print("Final token1:", results["token1_final"])
    print("Value if hold:", results["value_if_hold"])
    print("Value after price change:", results["value_after"])
    print("Impermanent loss (%):", results["impermanent_loss"] * 100)
    print("Fees earned:", results["fees_earned"])
    print("Total value including fees:", results["total_value_with_fees"])


if __name__ == "__main__":
    main()
