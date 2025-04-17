import pandas as pd
import numpy as np

class SpendingPredictor:
    def predict_next_month(self, transactions_df):
        """Simple prediction of next month's spending based on categories"""
        # Only consider expenses
        expenses_df = transactions_df[transactions_df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()  # Make positive for analysis
        
        # Group by category and calculate average
        category_avg = expenses_df.groupby('category')['amount'].agg(['sum', 'count', 'mean']).reset_index()
        
        # Generate predictions with some randomness for realism
        predictions = []
        for _, row in category_avg.iterrows():
            # Add some variability (±10%)
            variability = 0.1
            random_factor = 1 + (np.random.random() * variability * 2 - variability)
            predicted_amount = row['mean'] * random_factor
            
            predictions.append({
                'category': row['category'],
                'current_month_total': round(row['sum'], 2),
                'transaction_count': row['count'],
                'predicted_next_month': round(predicted_amount, 2)
            })
        
        return pd.DataFrame(predictions)