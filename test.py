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