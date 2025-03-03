from ai_engine import *

input_aux = open ("test/data/output.md", "r").read()
input = "Here is the content from which you need to generate 3 revision questions: \n" + input_aux
system_prompt_question = open ("test/data/system_prompt_question.md", "r").read()

questions = query_aiengines(input, system_prompt_question)
with open("test/data/questions.md", "w") as f:
    f.write(questions)  
    print("Processing please wait...")
