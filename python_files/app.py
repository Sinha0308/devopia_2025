from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
from categorizer import TransactionCategorizer
from analyzer import BudgetAnalyzer
from predictor import SpendingPredictor

app = Flask(__name__)
app.secret_key = 'mybudgetai_secret_key'  # Required for flashing messages and sessions

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize our components
categorizer = TransactionCategorizer()
analyzer = BudgetAnalyzer()
predictor = SpendingPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the uploaded file
        try:
            # Read the CSV file
            transactions_df = pd.read_csv(filepath)
            
            # Convert date column to datetime
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])
            
            # Categorize transactions
            transactions_df['category'] = transactions_df['description'].apply(categorizer.categorize)
            
            # Store in session
            session['transactions'] = transactions_df.to_json(orient='records', date_format='iso')
            
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Only CSV files are allowed')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'transactions' not in session:
        flash('No transactions data. Please upload a CSV file first.')
        return redirect(url_for('index'))
    
    # Retrieve and parse transactions from session
    transactions_df = pd.read_json(session['transactions'])
    
    # Analyze spending
    spending_analysis = analyzer.analyze_spending(transactions_df)
    
    # Generate savings tips
    savings_tips = analyzer.generate_savings_tips(spending_analysis)
    
    # Predict next month's spending
    predictions = predictor.predict_next_month(transactions_df)
    
    # Generate spending chart
    spending_chart = analyzer.generate_spending_chart(spending_analysis)
    
    return render_template(
        'dashboard.html',
        transactions=transactions_df.to_dict('records'),
        spending_analysis=spending_analysis.to_dict('records'),
        savings_tips=savings_tips,
        predictions=predictions.to_dict('records'),
        spending_chart=spending_chart
    )

if __name__ == '__main__':
    app.run(debug=True)