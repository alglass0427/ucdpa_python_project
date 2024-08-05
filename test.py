username = "test1"
email = "test1"
password = "test1"
dob = "test1"
gender = "test1"
nested_dict = {}
new_dict = {}
nested_dict.update(name = username)
nested_dict.update(DOB = dob)
nested_dict.update(gender = gender)
nested_dict.update(email = email)
nested_dict.update(password = password)
new_dict[email] = nested_dict
print(nested_dict)
print(new_dict)


import json
# email = ""
# password = request.form['password']
file_path = 'user_directory.json'


        # Function to read JSON data from a file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
            return {"user_data": []}

# Function to check if email and password combination exists
def check_credentials(file_path, email, password):
    data = read_json_file(file_path)
    for user in data["user_data"]:
        if user["email"] == email and user["password"] == password:
            return True
    return False

is_valid = check_credentials(file_path,"alglass@gmail.com","password")

print(f"Credentials valid: {is_valid}")