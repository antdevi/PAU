from ai_engine import *
from login_checker_engine import *

user_details = open("test/system_instruction/input_user.md", "r").read()
system_prompt= open("test/system_instruction/system_inst_userdetails.md", "r").read()
file_path = 'test/userdata/user.json'

login_checker(file_path)

response = query_aiengines(user_details, system_prompt)

with open("test/system_instruction/output.md", "w") as f:
    f.write(response)

