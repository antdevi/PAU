// public/static/JS/chat.js

// Wait for the DOM to fully load before binding event listeners.
document.addEventListener("DOMContentLoaded", function() {
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    loadNotes();
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
  function openTab(tabName) {
    // Hide all tab content sections
    let tabContents = document.querySelectorAll(".tab-content");
    tabContents.forEach(tab => {
        tab.style.display = "none";
    });

    // Remove active class from all tab buttons
    let tabButtons = document.querySelectorAll(".tab-buttons button");
    tabButtons.forEach(button => {
        button.classList.remove("active-tab");
    });

    // Show the selected tab content
    let selectedTab = document.getElementById(tabName + "Tab");
    if (selectedTab) {
        selectedTab.style.display = "block";
    }

    // Add active class to the clicked tab button
    let activeButton = document.querySelector(`button[onclick="openTab('${tabName}')"]`);
    if (activeButton) {
        activeButton.classList.add("active-tab");
    }
}

// Automatically open the "Notes" tab when the page loads
document.addEventListener("DOMContentLoaded", function () {
    openTab("notes");  // Change this if you want a different default tab
});

  function saveNote() {
    let title = document.getElementById("noteTitle").value.trim();
    let content = document.getElementById("noteContent").value.trim();

    if (title === "" || content === "") {
        alert("Title and Content cannot be empty!");
        return;
    }

    let note = {
        title: title,
        content: content,
        id: Date.now()
    };

    fetch("/notes/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(note)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotes();
            document.getElementById("noteTitle").value = "";
            document.getElementById("noteContent").value = "";
        } else {
            alert("Error saving note!");
        }
    });
}

// Function to load notes from the server
function loadNotes() {
    fetch("/notes/get")
    .then(response => response.json())
    .then(notes => {
        let notesList = document.getElementById("notesList");
        notesList.innerHTML = "";

        notes.forEach(note => {
            let listItem = document.createElement("li");
            listItem.innerHTML = `
                <input type="checkbox" class="note-checkbox" value="${note.id}">
                <strong>${note.title}</strong> - ${note.content.substring(0, 50)}...
            `;
            notesList.appendChild(listItem);
        });
    });
}

// Function to search notes
function searchNotes() {
    let query = document.getElementById("search-notes").value.toLowerCase();
    let notes = document.querySelectorAll("#notesList li");

    notes.forEach(note => {
        let text = note.textContent.toLowerCase();
        note.style.display = text.includes(query) ? "block" : "none";
    });
}

// Function to delete selected notes
function deleteSelectedNotes() {
    let selected = document.querySelectorAll(".note-checkbox:checked");
    let ids = Array.from(selected).map(cb => cb.value);

    if (ids.length === 0) {
        alert("Please select at least one note to delete.");
        return;
    }

    fetch("/notes/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ids })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotes();
        } else {
            alert("Error deleting notes!");
        }
    });
}

// Function to open selected notes
// Function to open selected notes and display them in selected-notes-display
function openSelectedNotes() {
  let selectedCheckboxes = document.querySelectorAll(".note-checkbox:checked");
  let ids = Array.from(selectedCheckboxes).map(cb => cb.value);

  if (ids.length === 0) {
      alert("Please select at least one note to open.");
      return;
  }

  fetch("/notes/open", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ ids: ids })  // Ensure correct payload format
  })
  .then(response => response.json())
  .then(notes => {
      let notesDisplay = document.getElementById("selected-notes-display");
      notesDisplay.innerHTML = ""; // Clear previous content

      if (notes.length === 0) {
          notesDisplay.innerHTML = "<p>No notes found!</p>";
          return;
      }

      notes.forEach(note => {
          let noteDiv = document.createElement("div");
          noteDiv.classList.add("note-container");
          noteDiv.innerHTML = `
              <h3>${note.title}</h3>
              <p>${note.content.replace(/\n/g, "<br>")}</p>
          `;

          notesDisplay.appendChild(noteDiv);
      });

      // Add close button at the bottom
      let closeButton = document.createElement("button");
      closeButton.textContent = "Close Notes";
      closeButton.classList.add("close-notes-button");
      closeButton.onclick = function () {
          notesDisplay.style.display = "none";
      };

      notesDisplay.appendChild(closeButton);

      // Show the notes display
      notesDisplay.style.display = "block";
  })
  .catch(error => {
      console.error("Error opening notes:", error);
      alert("Failed to open notes. Check console for details.");
  });
}
function revisionSection() {
  window.location.href = "/revision"; // Redirects to revision module selection page
}