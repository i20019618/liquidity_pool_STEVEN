# liquidity_pool.py

import json
import os

# liquidity_pool.py

class LiquidityPool:
    def __init__(self, token_x, token_y, amount_x, amount_y, fee_percentage=0.3):
        self.token_x = token_x
        self.token_y = token_y
        self.amount_x = amount_x
        self.amount_y = amount_y
        self.k = amount_x * amount_y  # xy = k
        self.fee_percentage = fee_percentage / 100  # Convert to a decimal for easy calculation
    
    def add_liquidity(self, amount_x, amount_y):
        self.amount_x += amount_x
        self.amount_y += amount_y
        self.k = self.amount_x * self.amount_y
    
    def swap_tokens(self, token, amount):
        if token == self.token_x:
            # Swapping x tokens to get y tokens
            new_x = self.amount_x + amount  # Adding x to the pool (buying y)
            new_y = self.k / new_x
            tokens_to_receive = self.amount_y - new_y
            
            if tokens_to_receive <= 0:
                raise ValueError("Insufficient liquidity or invalid swap.")
            
            # Apply transaction fee
            tokens_to_receive -= tokens_to_receive * self.fee_percentage
            
            self.amount_x = new_x
            self.amount_y = new_y
            return tokens_to_receive

        elif token == self.token_y:
            # Swapping y tokens to get x tokens
            new_y = self.amount_y + amount  # Adding y to the pool (buying x)
            new_x = self.k / new_y
            tokens_to_receive = self.amount_x - new_x
            
            if tokens_to_receive <= 0:
                raise ValueError("Insufficient liquidity or invalid swap.")
            
            # Apply transaction fee
            tokens_to_receive -= tokens_to_receive * self.fee_percentage
            
            self.amount_x = new_x
            self.amount_y = new_y
            return tokens_to_receive

        else:
            raise ValueError("Token not found in pool")
    
    def save_state(self, pool_name):
        """Save the pool state to a file based on pool name."""
        data = {
            'token_x': self.token_x,
            'token_y': self.token_y,
            'amount_x': self.amount_x,
            'amount_y': self.amount_y,
            'fee_percentage': self.fee_percentage * 100  # Convert back to percentage
        }
        with open(f'{pool_name}_state.json', 'w') as f:
            json.dump(data, f)
    
    @staticmethod
    def load_state(pool_name):
        """Load the pool state from a file based on pool name."""
        filename = f'{pool_name}_state.json'
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            data = json.load(f)
            # Set a default fee_percentage if it is missing (0.3% by default)
            fee_percentage = data.get('fee_percentage', 0.3)
            return LiquidityPool(data['token_x'], data['token_y'], data['amount_x'], data['amount_y'], fee_percentage)
