import json
import os
from json_to_md import *

file_path='test/profile_authentication/data/user_details.json'

def get_questions(file_path):

    if not os.path.exists(file_path):
        print(f"No file found at {file_path}")
        return False
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
  

    for i in range(len(data)):
        question = data[i]["question"]
        
        print(question)

        Answer = input("Answer: ")
    
        data[i]["answer"] = Answer

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
if __name__ == "__main__":
    get_questions(file_path)
