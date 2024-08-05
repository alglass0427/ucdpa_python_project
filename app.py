from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
# import json  #imported in the functions file
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

app = Flask(__name__)
app.secret_key = 'mysecretkey'
USER_DIRECTORY =  'user_directory.json'
# Dummy user data


# users = {1: {'name': 'John', 'age': '10', 'gender': 'Male','password':'password','email':'user@example.com'},
#          2: {'name': 'Alan', 'age': '38', 'gender': 'Male','password':'password','email':'alwglass@gmail.com'}}
# print(f"User {users[2]['email']} , {users[2]['password']}")

# Actual list of user
# Read the string from the .txt file
# with open('user_directory.txt', 'r') as file:
#     user_directory_str = file.read()
# # Convert the JSON string back to a dictionary
# users = json.loads(user_directory_str)

# # Print the dictionary to verify
# print(users["alwglass@gmail.com"]["password"])


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
        user_details = func.get_user_details(USER_DIRECTORY, email)
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
            func.add_user_to_json(USER_DIRECTORY,nested_dict)
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
        is_valid = func.check_credentials(USER_DIRECTORY, email, password)
        
        print(f"is valid returns {is_valid} and it is {type(is_valid)}")
        is_valid.pop("password")
        print(f"is valid returns {is_valid} and it is {type(is_valid)}")
        #Check if the user exists and the password is valid
        if is_valid != False and is_valid != "User does not exist.":  
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

@app.route('/lesson/<lesson_id>')
@login_required
def lesson(lesson_id):
    # Dummy lesson content
    lessons = {
        "1": "Lesson 1 content goes here.",
        "2": "Lesson 2 content goes here.",
        "3": "Lesson 3 content goes here."
    }
    return render_template('lesson.html', lesson_content=lessons.get(lesson_id, "Lesson not found."))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/validator')
def validator():
    lower_letter = False
    upper_letter = False
    num_end = False
    username = request.args.get("username")

    lower_letter = any(c.islower() for c in username) 
    ##short hand for looping through user name
    # for letter in username:
    #     if letter.lower() == letter:
    upper_letter = any(c.isupper() for c in username)
    num_end =  username[-1].isdigit()

    report = lower_letter and upper_letter and num_end

    return render_template('validator.html', report = report , lower = lower_letter , upper = upper_letter, num_end = num_end)



if __name__ == '__main__':
    app.run(debug=True)
