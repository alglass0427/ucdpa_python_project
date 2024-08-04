from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from functions.functions import write_json_file
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        gender = request.form['gender']
        nested_dict = {}
        new_dict = {}
        nested_dict.update(name = username)
        nested_dict.update(DOB = dob)
        nested_dict.update(gender = gender)
        nested_dict.update(email = email)
        nested_dict.update(password = password)
        new_dict[email] = nested_dict
        print(new_dict)


        with open('user_directory.txt', 'r') as file:
            user_directory_str = file.read()
            users = user_directory_str
        # Convert the JSON string back to a dictionary
        users = json.loads(user_directory_str)
        print(users)
        users.update(new_dict)
        print(users)

        with open('user_directory.txt', 'w') as file:
            for key, value in users.items():
                file.write(f'{key}: {value}\n')


        # "jdoe@example.com": {"name": "John Doe","DOB": "10/10/1987", "gender": "Male","email": "jdoe@example.com","password":"abcd"}
        # print(request.form)
        # for x in request.form:
        #     print(x)
        #     # print(y)
        #     for y in x:
        #         print(y)

        # print(users[email]) 
        # if email in users and users[email]["password"] == password:
        #     session['logged_in'] = True
        #     session['email'] = email
        #     session['username'] = "A USER"
        #     flash("Login successful", "success")
        #     return redirect(url_for('dashboard'))
        # else:
        #     flash("Invalid credentials", "danger")
    return render_template('signup.html')
#--------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Actual list of user
        # Read the string from the .txt file
        with open('user_directory.txt', 'r') as file:
            user_directory_str = file.read()
            users = user_directory_str
        # Convert the JSON string back to a dictionary
        users = json.loads(user_directory_str)
        print(users)

        # Print the dictionary to verify
        print(users["alwglass@gmail.com"]["password"])
        # print(users[email]) 
        if email in users:
            if users[email]["password"] == password:
                session['logged_in'] = True
                session['email'] = email
                session['username'] = users[email]["name"]
                flash("Login successful", "success")
                return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
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
