from flask import Flask, request, jsonify
from openai import OpenAI
from datetime import datetime
import os

app = Flask(__name__)
# Set up the client to connect to the local chatbot
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# System instruction for the chatbot
system_instruction = {"role": "system", "content": "Always answer in rhymes."}


# File to save the chats
chat_log_file = "C:/Users/ANTARA DAS/Desktop/chat_log.txt"

name = input("Enter your name: ")

# Dynamic interaction with the user
while True:
    # Get user input
    user_input = input(f"{name}: ")
    
    # Exit the loop if the user types 'exit'
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    # Show "Thinking..." while waiting for a response
    print("Thinking...", end="", flush=True)
    
    # Create the chat request
    completion = client.chat.completions.create(
        model="model-identifier",
        messages=[
            system_instruction,
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
    )
    
    # Once response is ready, clear the "Thinking..." message
    print("\r", end="")  # Clears the "Thinking..." text
    
    # Corrected way to access the bot's response
    bot_response = completion.choices[0].message.content
    
    # Print the chatbot's response
    print(f"Bot: {bot_response}")
    m=datetime.now().strftime("%y-%m-%d %H:%M:%S") 
    # Save the conversation to the file
    with open(chat_log_file, "a") as file:
        file.write(f"[{m}] {name}: {user_input}\n")
        file.write(f"[{m}] Bot: {bot_response}\n")
        file.write("\n")  # Add a newline for readability