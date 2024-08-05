from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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
    # file_path = 'user_directory.json'
    
    
    # print(f"Details for {email}: {user_details}")
    if request.method == 'POST':

        username = request.form['name']
        email = request.form['email']
        user_details = func.get_user_details(USER_DIRECTORY, email)
        print(f"Details for {email}: {user_details}")
        if user_details == "User does not exist.":
            password = request.form['password']
            dob = request.form['dob']
            gender = request.form['gender']
            nested_dict = {}
            nested_dict.update(name = username)
            nested_dict.update(DOB = dob)
            nested_dict.update(gender = gender)
            nested_dict.update(email = email)
            nested_dict.update(password = password)
            print(nested_dict)
            func.add_user_to_json(USER_DIRECTORY,nested_dict)
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

        print(is_valid)
        # Actual list of user
        # Read the string from the .txt file
        # with open('user_directory.txt', 'r') as file:
        # with open(file_path, 'r') as file:
        #     users = json.load(file)

        # Print the dictionary to verify
        # print(users["user_data"][3])
            #   ["ber@gmail.com"]["password"])
        # ['alwglass@gmail.com']['password'])
        # print(users[email]) 
        if is_valid != False and is_valid != "User does not exist.":
            session['logged_in'] = True
            session['email'] = email
            session['username'] = is_valid
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

if __name__ == '__main__':
    app.run(debug=True)
