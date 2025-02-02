# Generating a comprehensive set of 1000 Python MCQs

import random
import json

# Categories of Python concepts
categories = {
    "Basics": [
        ("What is the correct syntax to output 'Hello World' in Python?", 
         ["print('Hello World')", "echo 'Hello World'", "printf('Hello World')", "System.out.println('Hello World')"], "print('Hello World')"),
        ("Which of the following is a valid variable name in Python?", 
         ["1variable", "variable_1", "variable-1", "@variable"], "variable_1"),
        ("Which symbol is used for comments in Python?", 
         ["//", "#", "/* */", "--"], "#")
    ],
    "Data Types": [
        ("Which data type is mutable in Python?", 
         ["Tuple", "String", "List", "Integer"], "List"),
        ("What is the output of type([])?", 
         ["list", "tuple", "dictionary", "set"], "list"),
        ("Which function is used to convert a string to an integer in Python?", 
         ["toInt()", "str_to_int()", "int()", "convert()"], "int()")
    ],
    "Control Flow": [
        ("Which keyword is used to exit a loop in Python?", 
         ["stop", "break", "exit", "end"], "break"),
        ("What will range(5) return?", 
         ["A list of numbers from 0 to 5", "An iterator of numbers from 0 to 4", "A tuple", "An error"], "An iterator of numbers from 0 to 4"),
        ("Which statement is used to skip the rest of a loop iteration and start the next one?", 
         ["break", "continue", "skip", "pass"], "continue")
    ],
    "Functions": [
        ("Which keyword is used to define a function in Python?", 
         ["function", "def", "define", "func"], "def"),
        ("What does the return statement do in a function?", 
         ["Stops the function", "Returns a value and stops execution", "Prints the value", "None of the above"], "Returns a value and stops execution"),
        ("Which type of function doesn’t require an explicit return statement?", 
         ["Generator", "Lambda", "Recursive", "Static"], "Lambda")
    ],
    "Object-Oriented Programming": [
        ("Which method is the constructor in a Python class?", 
         ["__init__", "__start__", "constructor", "__main__"], "__init__"),
        ("What is the parent class of all Python classes?", 
         ["object", "base", "parent", "super"], "object"),
        ("Which keyword is used to inherit a class in Python?", 
         ["extends", "inherits", "super", "class"], "super")
    ],
    "Exception Handling": [
        ("Which keyword is used to handle exceptions in Python?", 
         ["catch", "except", "try", "handle"], "except"),
        ("What does the 'finally' block do?", 
         ["Executes if an error occurs", "Executes whether an error occurs or not", "Skips errors", "Handles errors"], "Executes whether an error occurs or not")
    ],
    "File Handling": [
        ("Which mode is used to open a file for writing only?", 
         ["r", "w", "a", "rw"], "w"),
        ("How do you properly close a file in Python?", 
         ["file.close()", "close.file()", "file.stop()", "stop.file()"], "file.close()"),
        ("Which function is used to read an entire file into a string?", 
         ["readFile()", "read()", "load()", "get()"], "read()")
    ],
    "Advanced Topics": [
        ("What is the purpose of the Python Global Interpreter Lock (GIL)?", 
         ["To allow multithreading", "To prevent deadlocks", "To manage memory", "To ensure only one thread executes at a time"], "To ensure only one thread executes at a time"),
        ("Which Python module is used for multiprocessing?", 
         ["os", "sys", "threading", "multiprocessing"], "multiprocessing")
    ]
}

# Generate 1000 MCQs by duplicating and mixing the categories
mcq_list = []
question_id = 1

while len(mcq_list) < 1000:
    for category, questions in categories.items():
        for question, options, correct in questions:
            mcq_list.append({
                "id": question_id,
                "category": category,
                "question": question,
                "options": options,
                "correct_answer": correct
            })
            question_id += 1
            if len(mcq_list) >= 1000:
                break
        if len(mcq_list) >= 1000:
            break

# Save the MCQs as a JSON file
json_mcq_file = "/Documents/gitdemo/PAU"
with open(json_mcq_file, "w") as json_file:
    json.dump(mcq_list, json_file, indent=4)

# Provide the file path for download
json_mcq_file
