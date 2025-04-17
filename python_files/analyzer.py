import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class BudgetAnalyzer:
    def analyze_spending(self, transactions_df):
        """Analyze spending by category"""
        # Only consider expenses (negative amounts)
        expenses_df = transactions_df[transactions_df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()  # Make positive for analysis
        
        # Group by category and sum
        category_totals = expenses_df.groupby('category')['amount'].sum().reset_index()
        total_spent = category_totals['amount'].sum()
        
        # Calculate percentage
        category_totals['percentage'] = (category_totals['amount'] / total_spent * 100).round(2)
        
        # Sort by amount descending
        category_totals = category_totals.sort_values('amount', ascending=False)
        
        return category_totals
    
    def generate_savings_tips(self, spending_analysis):
        """Generate savings tips based on spending analysis"""
        tips = []
        
        # Convert to dictionary for easier access
        spending_dict = spending_analysis.set_index('category').to_dict('index')
        
        # Generate tips based on spending patterns
        if 'DINING' in spending_dict and spending_dict['DINING']['percentage'] > 15:
            tips.append("You're spending over 15% on dining out. Consider cooking at home more often.")
        
        if 'ENTERTAINMENT' in spending_dict and spending_dict['ENTERTAINMENT']['percentage'] > 10:
            tips.append("Your entertainment expenses are relatively high. Look for free or low-cost alternatives.")
        
        if 'SHOPPING' in spending_dict and spending_dict['SHOPPING']['amount'] > 100:
            tips.append("Your shopping expenses exceeded $100 this month. Consider implementing a waiting period before purchases.")
        
        # Add general tips if specific ones don't apply
        if len(tips) < 2:
            tips.append("Set up automatic transfers to your savings account on payday.")
            tips.append("Try the 50/30/20 rule: 50% on needs, 30% on wants, and 20% on savings.")
        
        return tips
    
    def generate_spending_chart(self, spending_analysis):
        """Generate a pie chart of spending by category"""
        plt.figure(figsize=(8, 6))
        plt.pie(spending_analysis['amount'], 
                labels=spending_analysis['category'], 
                autopct='%1.1f%%',
                startangle=90)
        plt.axis('equal')
        plt.title('Expenses by Category')
        
        # Save the chart to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        
        # Encode the image to base64 for HTML embedding
        encoded_img = base64.b64encode(img_data.getvalue()).decode('utf-8')
        plt.close()
        
        return encoded_img