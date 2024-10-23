# cli.py

from liquidity_pool import LiquidityPool

pools = {}

def load_pools():
    # Load pools from existing files if available
    import glob
    global pools
    for filename in glob.glob('*_state.json'):
        pool_name = filename.split('_state.json')[0]
        pool = LiquidityPool.load_state(pool_name)
        if pool:
            pools[pool_name] = pool

def create_pool(pool_name, token_x, token_y, amount_x, amount_y, fee_percentage=0.3):
    global pools
    if pool_name in pools:
        print(f"A pool named {pool_name} already exists.")
        return
    
    pool = LiquidityPool(token_x, token_y, amount_x, amount_y, fee_percentage)
    pools[pool_name] = pool
    pool.save_state(pool_name)
    print(f"Created pool '{pool_name}' with {amount_x} {token_x} and {amount_y} {token_y}, Fee: {fee_percentage}%.")

def add_liquidity(pool_name, amount_x, amount_y):
    global pools
    if pool_name not in pools:
        print(f"No pool named '{pool_name}' exists. Please create a pool first.")
        return
    pool = pools[pool_name]
    pool.add_liquidity(amount_x, amount_y)
    pool.save_state(pool_name)
    print(f"Added {amount_x} of {pool.token_x} and {amount_y} of {pool.token_y} to the pool '{pool_name}'.")

def swap_tokens(pool_name, token, amount):
    global pools
    if pool_name not in pools:
        print(f"No pool named '{pool_name}' exists. Please create a pool first.")
        return
    pool = pools[pool_name]
    try:
        tokens_received = pool.swap_tokens(token, amount)
        pool.save_state(pool_name)
        print(f"Swapped {amount} {token} in pool '{pool_name}', received {tokens_received:.4f} in return.")
    except ValueError as e:
        print(f"Error: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Liquidity Pool CLI with Fees and Multiple Pools")
    
    parser.add_argument('--create-pool', nargs=6, metavar=('POOL_NAME', 'TOKEN_X', 'TOKEN_Y', 'AMOUNT_X', 'AMOUNT_Y', 'FEE_PERCENTAGE'),
                        help="Create a new liquidity pool")
    parser.add_argument('--add-liquidity', nargs=3, metavar=('POOL_NAME', 'AMOUNT_X', 'AMOUNT_Y'),
                        help="Add liquidity to an existing pool")
    parser.add_argument('--swap', nargs=3, metavar=('POOL_NAME', 'TOKEN', 'AMOUNT'),
                        help="Swap tokens in a specific pool")
    
    args = parser.parse_args()
    
    load_pools()  # Load existing pools on startup
    
    if args.create_pool:
        pool_name, token_x, token_y, amount_x, amount_y, fee_percentage = args.create_pool
        amount_x = float(amount_x)
        amount_y = float(amount_y)
        fee_percentage = float(fee_percentage)
        create_pool(pool_name, token_x, token_y, amount_x, amount_y, fee_percentage)
    
    if args.add_liquidity:
        pool_name, amount_x, amount_y = args.add_liquidity
        amount_x = float(amount_x)
        amount_y = float(amount_y)
        add_liquidity(pool_name, amount_x, amount_y)

    if args.swap:
        pool_name, token, amount = args.swap
        amount = float(amount)
        swap_tokens(pool_name, token, amount)

if __name__ == "__main__":
    main()
