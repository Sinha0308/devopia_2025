class TransactionCategorizer:
    def __init__(self):
        # Define categories and their keywords
        self.categories = {
            'GROCERY': ['GROCERY', 'SUPERMARKET', 'MARKET', 'FOOD'],
            'DINING': ['RESTAURANT', 'CAFE', 'STARBUCKS', 'MCDONALD', 'CHIPOTLE'],
            'SHOPPING': ['AMAZON', 'TARGET', 'MACY', 'CLOTHING', 'PURCHASE', 'STORE'],
            'ENTERTAINMENT': ['NETFLIX', 'SPOTIFY', 'MOVIE', 'TICKET', 'SUBSCRIPTION', 'COURSE'],
            'UTILITIES': ['ELECTRIC', 'WATER', 'GAS', 'INTERNET', 'UTILITY', 'BILL', 'PHONE'],
            'TRANSPORT': ['UBER', 'LYFT', 'BUS', 'TRAIN', 'FUEL', 'GAS STATION', 'RIDE'],
            'INCOME': ['SALARY', 'DEPOSIT', 'PAYMENT RECEIVED', 'REFUND', 'INTEREST'],
            'HOUSING': ['RENT', 'MORTGAGE', 'HOME']
        }
    
    def categorize(self, description):
        """Categorize a transaction based on its description"""
        description = description.upper()
        
        for category, keywords in self.categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return 'OTHER'