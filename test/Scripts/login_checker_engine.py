import json
from questions import *
from json_to_md import *
import os

file_path = 'test/userdata/user.json'
user_file_path = 'test/userdata/user_details.json'
md_file_path = "test/system_instruction/input_user.md"

def login_checker(file_path):

    if not os.path.exists(file_path):
        print(f"No file found at {file_path}")
        return False

    #read the json file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    #extract the parameters to check 
    login_count = data [0]["login_count"]

    #update the login count
    data[0]["login_count"] = login_count + 1

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    if login_count == 0:
        print("HI I'm PAU, i would like to know more about you")
        get_questions(user_file_path)
    else:
        print("Welcome back! You have logged in {} times".format(login_count))

    json_to_markdown(user_file_path, md_file_path)

if __name__ == "__main__":
    login_checker(file_path)