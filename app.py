from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
# import json  #imported in the functions file
# from flask_wtf import FlaskForm
# from wtforms import StringField,SubmitField,PasswordField,DateField,RadioField
# from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = 'mysecretkey'
USER_DIRECTORY =  'user_directory.json'
app.config['USER_DIRECTORY'] = USER_DIRECTORY

###Main App below

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rule = str(request.url_rule)
        print(f"route is {str(rule)}")
        print(rule == "/") 
        print(type(str(rule)))
        # print(session['email'])
        if rule ==  "/":
            if 'logged_in' in session:
                flash(f"Logged in as , {session['username']}","success")
        elif 'logged_in' not in session:
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
        username = request.form['name']
        email = request.form['email']
        #does the email exist in get user details using the user directory global file location
        user_details = func.get_user_details(app.config['USER_DIRECTORY'], email)
        print(f"Details for {email}: {user_details}")
        #if the user does not exist then add to the JSON of users
        if user_details == "User does not exist.":
            # form_data = request.form.to_dict()
            nested_dict = {}
            for item in request.form:
                print(item)
                print(request.form[item])
                nested_dict[item] = request.form[item]

            print(nested_dict)
            func.add_user_to_json(app.config['USER_DIRECTORY'],nested_dict)
            return redirect(url_for('login'))
        else:
            flash("Email address already used -  Please Login", "warning")
     
    return render_template('signup.html')
#--------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        is_valid = func.check_credentials(app.config['USER_DIRECTORY'], email, password)
        
        print(f"is valid returns {is_valid} and it is {type(is_valid)}")
        # is_valid.pop("password")
        print(f"is valid returns {is_valid} and it is {type(is_valid)}")
        #Check if the user exists and the password is valid
        if is_valid != False and is_valid != "User does not exist.":
            is_valid.pop("password")
            session['logged_in'] = True
            session['email'] = email
            session['username'] = is_valid["name"]
            session['user_data'] = is_valid
            # session['username'] = "Carter Glass"
            flash("Login successful", "success")
            return redirect(url_for('dashboard'))
        elif is_valid == "User does not exist.":
            flash("User does not Exist -  Sign Up to Begin!!", "danger")
        else:
            flash("User exists - Invalid Password!!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    print(session)
    session.pop('logged_in', None)
    session.pop('email', None)
    flash("You have been logged out", "info")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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
