from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
import functions.stock_functions as stock_func    ###Functions file in functions folder to seperate functions from app.py
import os
import json
# import yfinance as yf


# import json  #imported in the functions file
# from flask_wtf import FlaskForm
# from wtforms import StringField,SubmitField,PasswordField,DateField,RadioField
# from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = 'mysecretkey'
CURRENT_DIR =  os.getcwd()
USER_DIRECTORY =  'user_directory.json'
PERSISTENT_DIR =  os.path.join(CURRENT_DIR, 'persistent')
USER_DATA_FOLDER = os.path.join(PERSISTENT_DIR, 'users')
ACCOUNTS_FILE = os.path.join(PERSISTENT_DIR, 'accounts', 'accounts.json')
app.config['USER_DIRECTORY'] = USER_DIRECTORY


# Ensure directories exist
# print(f"Creating user data folder at {USER_DATA_FOLDER}")
if not os.path.exists(USER_DATA_FOLDER):
    print(f"Creating user data folder at {USER_DATA_FOLDER}")
    os.makedirs(USER_DATA_FOLDER)


if not os.path.exists(os.path.dirname(ACCOUNTS_FILE)):
    print(f"Creating accounts directory at {ACCOUNTS_FILE}")
    os.makedirs(os.path.dirname(ACCOUNTS_FILE))

if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, 'w') as f:
        print(f"Creating accounts file at {ACCOUNTS_FILE}")
        json.dump({}, f)  # Initialize with an empty dictionary


###Main App below

# Login required decorator to ensure usure is in session
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rule = str(request.url_rule)
        print(f"route is {str(rule)}")
        print(rule == "/") 
        print(type(str(rule)))
        # print(session['email'])
        if rule ==  "/":
            if 'username' in session:
                flash(f"Logged in as , {session['username']}","success")
        elif 'username' not in session:
            flash("Please log in first", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')


# ----------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #check if The user exists already
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        # password = request.form['password']
        accounts = stock_func.load_user_accounts()
        
        user_details =  {}
        
        for key, value in request.form.items():            
            user_details[key] = value
            print(user_details)
 
        
        if email in accounts:
            flash('Username already exists', 'warning')
            return redirect(url_for('signup'))
        
        accounts[email] = user_details
        # accounts[username] = username
        print(f"Details for {accounts[email] }")
        stock_func.save_user_accounts(accounts)
        # stock_func.save_user_portfolio(email, [])
        stock_func.save_user_portfolio(email, {})
        session['username'] = username
        session['email'] = email
        
        return redirect(url_for('login'))
        #if the user does not exist then add to the JSON of users
     
    return render_template('signup.html')
#--------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        accounts = stock_func.load_user_accounts()
        # print(f" load user accounts function : accounts are , {accounts[username]} ")
        
        if email in accounts and accounts[email]["password"] == password:
            session['email'] = email
            session['username'] = accounts[email]["fullname"]
            return redirect(url_for('dashboard_1'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    print(session)
    session.pop('username', None)
    session.pop('email', None)
    flash("You have been logged out", "info")
    return redirect(url_for('index'))

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')

@app.route('/dashboard_1')
@login_required
def dashboard_1():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    email = session['email']
    user_data = stock_func.load_user_portfolio(email)
    print(f"User Data:{user_data}")
    
    # Fetch the prices for all stocks in the user's portfolio
    #stock_func.get_stock_price(stock)
    ##BACKWARDS FOR LOOP get the stock and the price for each stock in the portfolio
    #Seperate this to get the response in one API Call
    # stocks_with_prices = [(stock, "") for stock in user_data['portfolio']]
    # stock_func.get_stock_price(stock)
    stocks_with_prices = [(stock,user_data,stock_func.get_stock_price(stock)) for stock in user_data]
    print(f"This is the Stock data passed to the Dashboard ::::: {stocks_with_prices} ")

    return render_template('dashboard_1.html', username=username, stocks=stocks_with_prices)

# this will add the Stock then , update the list , 
# then call dashboard_1 which will get the updated list and get the prices 

@app.route('/add_stock', methods=['POST'])
def add_stock():
    print("INSIDE ADD STOCK")
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['email']
    stock_code = request.form['stock_code'].upper()
    buy_price = request.form['buy_price']
    no_of_shares = request.form['no_of_shares']

    user_data = stock_func.load_user_portfolio(username)
    print(f"User Data:{user_data}")
    # if stock_code and stock_code not in user_data['portfolio']:
    if stock_code and stock_code not in user_data:
        stock_add_details =  {}
        # stock_add = {}
        for key, value in request.form.items():            
            stock_add_details[key] = value
            print(stock_add_details)
            user_data[stock_code] = stock_add_details
            # print(f"Stock Add:{stock_add}")
            #Stock Add:{'B': {'stock_code': 'b', 'buy_price': 'b', 'no_of_shares': 'b'}}
        # user_data['portfolio'].append(stock_code)
        stock_func.save_user_portfolio(username, user_data)
    
    return redirect(url_for('dashboard_1'))

@app.route('/remove_stock/<string:stock_code>')
def remove_stock(stock_code):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['email']
    user_data = stock_func.load_user_portfolio(username)

    if stock_code in user_data:
        user_data.pop(stock_code)
        stock_func.save_user_portfolio(username, user_data)
    
    return redirect(url_for('dashboard_1'))



@app.route('/portfolio/<portfolio_id>')
@login_required
def portfolio(portfolio_id):
    # Dummy lesson content
    portfolios = {
        "1": "Portfolio 1 content goes here.",
        "2": "Portfolio 2 content goes here.",
        "3": "Portfolio 3 content goes here."
    }
    return render_template('portfolio.html', portfolio_content=portfolios.get(portfolio_id, "Portfolio not found."))

# new Redirect For 404 Error 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


###practice For passing between templates
@app.route('/validator')
def validator():
    lower_letter = False
    upper_letter = False
    num_end = False
    report = False
    # try:
    username = request.args.get("username")
    print(username)
    if username != "":
        lower_letter = any(c.islower() for c in username) 
        ##short hand for looping through user name
        # for letter in username:
        #     if letter.lower() == letter:
        upper_letter = any(c.isupper() for c in username)
        num_end =  username[-1].isdigit()

        report = lower_letter and upper_letter and num_end

    return render_template('validator.html', report = report , lower = lower_letter , upper = upper_letter, num_end = num_end)
    # except TypeError:
    #     print("No Users Exist!!!")





if __name__ == '__main__':
    app.run(debug=True)
