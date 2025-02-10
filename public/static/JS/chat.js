// public/static/JS/chat.js

// Wait for the DOM to fully load before binding event listeners.
document.addEventListener("DOMContentLoaded", function() {
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
  
    // Send message when the Enter key is pressed in the input field.
    userInput.addEventListener("keydown", function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
      }
    });
  
    // Send message when the Send button is clicked.
    sendButton.addEventListener("click", function() {
      sendMessage();
    });
  });
  
  // Append a new message to the chatbox.
  // The 'sender' parameter should be either "user" or "bot" (used for styling).
  function appendMessage(sender, message) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + sender; // e.g., "message user" or "message bot"
    messageDiv.textContent = message;
    chatbox.appendChild(messageDiv);
  
    // Auto-scroll to the bottom of the chatbox.
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  
  // Send the user's message to the LM Studio endpoint via the chatbot route.
  function sendMessage() {
    const inputField = document.getElementById("userInput");
    const message = inputField.value.trim();
    if (message === "") return; // Do nothing if the input is empty.
  
    // Append the user's message to the chatbox.
    appendMessage("user", message);
  
    // Clear the input field.
    inputField.value = "";
  
    // Append a temporary message indicating that the bot is typing.
    appendMessage("bot", "Bot is typing...");
  
    // Send a POST request to the /chat endpoint.
    // Adjust the URL if your blueprint URL prefix differs.
    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(data => {
        // Remove the temporary "Bot is typing..." message.
        const chatbox = document.getElementById("chatbox");
        if (
          chatbox.lastChild &&
          chatbox.lastChild.textContent === "Bot is typing..."
        ) {
          chatbox.removeChild(chatbox.lastChild);
        }
        // Append the bot's actual response.
        appendMessage("bot", data.response);
      })
      .catch(error => {
        console.error("Error:", error);
        // Update the temporary message with an error message.
        const chatbox = document.getElementById("chatbox");
        if (
          chatbox.lastChild &&
          chatbox.lastChild.textContent === "Bot is typing..."
        ) {
          chatbox.lastChild.textContent = "Error: Could not get response.";
        }
      });
  }
  