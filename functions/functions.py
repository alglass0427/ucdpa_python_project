import json

# Function to write JSON data to a file
def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to read JSON data from a file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
            return {"user_data": []}
    

# Function to add a new user to the JSON file
def add_user_to_json(file_path, new_user_data):
    # Read the existing data from the file
    existing_data = read_json_file(file_path)
    
    # Append the new user data to the "user_data" list
    existing_data['user_data'].append(new_user_data)
    
    # Write the updated data back to the file
    write_json_file(file_path, existing_data)

# Function to check if email and password combination exists
def check_credentials(file_path, email, password):
    data = read_json_file(file_path)
    for user in data["user_data"]:
        if user["email"] == email:
            if user["password"] == password:
                return user["name"]
            else:
                return False
    return "User does not exist."

# Function to get user details by email
def get_user_details(file_path, email):
    data = read_json_file(file_path)
    for user in data["user_data"]:
        if user["email"] == email:
            return user
    return "User does not exist."

