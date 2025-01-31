import requests
import json

# LM Studio API endpoint
LLAMA_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# System instruction (modify if needed)
system_message = {"role": "system", "content": "Always answer in rhymes."}

# Chat history
messages = [system_message]

def chat_with_llama():
    print("Chat with Llama 3.2 1B (Type 'exit' to quit)\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Request payload
        payload = {
            "model": "llama-3.2-1b-instruct",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 200,
            "stream": False
        }

        # Send request to LM Studio
        response = requests.post(LLAMA_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        if response.status_code == 200:
            # Extract the model's reply
            reply = response.json()["choices"][0]["message"]["content"]
            print(f"Llama: {reply}\n")
            
            # Add model response to history
            messages.append({"role": "assistant", "content": reply})
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    chat_with_llama()
