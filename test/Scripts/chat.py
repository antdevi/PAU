from ai_engine import *

user_message =open("data/input.md", "r").read()
system_prompt =open("data/system_prompt.md", "r").read()

response = query_aiengines(user_message, system_prompt)

with open("data/output.md", "w") as f:
    f.write(response)
