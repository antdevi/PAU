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

let currentQuestionIndex = 0;
let incorrectQuestions = [];
let allQuestions = []; // This will hold the questions from your JSON file.
let answeredQuestions = []; // To track answered questions

// Function to load questions from the backend (JSON file)
async function loadQuestions() {
    try {
        const response = await fetch('/get_question'); // Fetch the question from the server
        const data = await response.json();

        if (data.error) {
            alert(data.error); // Display any error message from the backend
            return;
        }

        // Display the question and options
        document.getElementById("question-text").innerText = data.question;
        let optionsContainer = document.getElementById("options-container");
        optionsContainer.innerHTML = ""; // Clear previous options

        data.options.forEach(option => {
            let button = document.createElement("button");
            button.innerText = option;
            button.classList.add("option-button");
            button.onclick = () => selectOption(option, data); // When an option is selected
            optionsContainer.appendChild(button);
        });
    } catch (error) {
        console.error('Error loading question:', error);
    }
}
// Submit the answer's explanation (if any)
function submitPythonAnswer() {
    let explanation = document.getElementById("explanation-box").value.trim();
    if (explanation === "") {
        alert("Please provide an explanation before submitting.");
        return;
    }
    alert("Your answer has been submitted.");
}

// Initialize and load questions
document.addEventListener("DOMContentLoaded", loadQuestions);

// Logout function
function logout() {
    window.location.href = "/logout";
}
