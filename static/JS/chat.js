document.addEventListener("DOMContentLoaded", loadNotes);

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.getElementById(tabId).style.display = 'block';
}

function saveNote() {
    let noteInput = document.getElementById("noteInput").value.trim();
    if (noteInput === "") return;

    let notes = JSON.parse(localStorage.getItem("notes")) || [];
    notes.push(noteInput);
    localStorage.setItem("notes", JSON.stringify(notes));

    document.getElementById("noteInput").value = "";
    loadNotes();
}

function loadNotes() {
    let notesList = document.getElementById("saved-notes");
    notesList.innerHTML = "";

    let notes = JSON.parse(localStorage.getItem("notes")) || [];

    notes.forEach((note, index) => {
        let listItem = document.createElement("div");
        listItem.classList.add("note-item");

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.classList.add("note-checkbox");
        checkbox.dataset.index = index;

        let label = document.createElement("label");
        label.textContent = note;
        label.classList.add("note-label");

        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        notesList.appendChild(listItem);
    });
}

function deleteSelectedNotes() {
    let notes = JSON.parse(localStorage.getItem("notes")) || [];
    let checkboxes = document.querySelectorAll(".note-checkbox:checked");

    let selectedIndexes = Array.from(checkboxes).map(cb => parseInt(cb.dataset.index));

    // Filter out selected notes
    notes = notes.filter((_, index) => !selectedIndexes.includes(index));

    localStorage.setItem("notes", JSON.stringify(notes));
    loadNotes(); // Refresh the UI
}

function searchNotes() {
    let searchInput = document.getElementById("search-notes").value.toLowerCase();
    let notes = JSON.parse(localStorage.getItem("notes")) || [];
    let notesList = document.getElementById("saved-notes");

    notesList.innerHTML = "";

    notes.filter(note => note.toLowerCase().includes(searchInput)).forEach((note, index) => {
        let listItem = document.createElement("div");
        listItem.classList.add("note-item");

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.classList.add("note-checkbox");
        checkbox.dataset.index = index;

        let label = document.createElement("label");
        label.textContent = note;
        label.classList.add("note-label");

        listItem.appendChild(checkbox);
        listItem.appendChild(label);
        notesList.appendChild(listItem);
    });
}

async function sendMessage() {
    let messageInput = document.getElementById("message");
    let messageText = messageInput.value.trim();

    if (messageText === "") return; // Prevent empty messages
    
    let chatBox = document.getElementById("chat-box");

    // Add user message
    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = messageText;
    chatBox.appendChild(userMessage);

    messageInput.value = ""; // Clear input field

    // Call Flask API to get AI response
    try {
        let response = await fetch("/get_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: messageText })
        });

        let data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        // Display bot response
        let botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = "PAU: " + data.response;
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
    } catch (error) {
        console.error("Error:", error);
        let errorMessage = document.createElement("div");
        errorMessage.className = "bot-message";
        errorMessage.textContent = "Error: Unable to fetch response.";
        chatBox.appendChild(errorMessage);
    }
}
// Logout function
function logout() {
    window.location.href = "/logout";
}
function redirectToQuiz() {
    window.location.href = "http://127.0.0.1:5001/";
}
function openSelectedNotes() {
    let selectedNotes = [];
    let checkboxes = document.querySelectorAll(".note-checkbox:checked");

    checkboxes.forEach(cb => {
        let noteText = cb.nextElementSibling.textContent;
        selectedNotes.push(noteText);
    });

    let selectedNotesContainer = document.getElementById("selected-notes-display");
    selectedNotesContainer.innerHTML = "";

    if (selectedNotes.length === 0) {
        selectedNotesContainer.innerHTML = "<p>No notes selected.</p>";
        return;
    }

    selectedNotes.forEach(note => {
        let noteItem = document.createElement("div");
        noteItem.classList.add("note-item");
        noteItem.textContent = note;
        selectedNotesContainer.appendChild(noteItem);
    });

    // Add a close button
    let closeButton = document.createElement("button");
    closeButton.textContent = "Close";
    closeButton.classList.add("close-notes-button");
    closeButton.onclick = closeSelectedNotes;
    selectedNotesContainer.appendChild(closeButton);
}

function closeSelectedNotes() {
    let selectedNotesContainer = document.getElementById("selected-notes-display");
    selectedNotesContainer.innerHTML = ""; // Clears the displayed notes
}
