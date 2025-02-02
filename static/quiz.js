let currentQuestion = null;
let selectedOption = null;
let score = 0;

// Fetch a random question from the server
function fetchQuestion() {
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            currentQuestion = data;  // Store the question object
            displayQuestion(data);  // Display the question
        })
        .catch(error => console.error('Error fetching question:', error));
}

// Display the current question and options
function displayQuestion(question) {
    document.getElementById('question-text').innerText = question.text;

    const optionsContainer = document.getElementById('options');
    optionsContainer.innerHTML = '';  // Clear previous options

    // Loop through the options and create buttons
    question.options.forEach((option, index) => {
        const optionElem = document.createElement('button');
        optionElem.innerText = option;
        optionElem.onclick = () => selectOption(index, optionElem, option);
        optionsContainer.appendChild(optionElem);
    });

    // Disable the Next Question button initially
    document.getElementById('next-question').disabled = true;
}

// Handle option selection
function selectOption(index, buttonElem, option) {
    selectedOption = option;  // Store the selected option
    resetButtonStyles();  // Reset button styles to remove previous selections
    buttonElem.classList.add('selected');  // Add selected class to the clicked option

    // Check if the selected option is correct
    if (selectedOption === currentQuestion.correct_answer) {
        buttonElem.classList.add('correct');  // Add correct class if the answer is correct
    } else {
        buttonElem.classList.add('incorrect');  // Add incorrect class if the answer is wrong
    }

    // Enable the Next Question button after an option is selected
    document.getElementById('next-question').disabled = false;
}

// Reset button styles
function resetButtonStyles() {
    const buttons = document.querySelectorAll('#options button');
    buttons.forEach(button => {
        button.classList.remove('selected', 'correct', 'incorrect');
    });
}

// Submit the answer and store it in the backend
function submitAnswer() {
    if (selectedOption === null) {
        alert("Please select an option.");
        return;
    }

    const subjectiveAnswer = document.getElementById('subjective-answer').value;

    // Log the selected answer and correct answer for debugging
    console.log("Selected Answer: " + selectedOption);
    console.log("Correct Answer: " + currentQuestion.correct_answer);

    // Validate that the correct answer is selected
    if (selectedOption !== currentQuestion.correct_answer) {
        alert("Please select the correct answer.");
        return;
    }

    // Validate that the subjective answer box is filled
    if (subjectiveAnswer.trim() === "") {
        alert("Please provide an answer in the subjective answer box.");
        return;
    }

    // Prepare the answer data
    const answerData = {
        question: currentQuestion.text,
        selected_option: selectedOption,
        subjective_answer: subjectiveAnswer,
        score: 0 // Initialize score for this question
    };

    // If the answer is correct, award 10 marks
    if (selectedOption === currentQuestion.correct_answer) {
        score += 10;  // Increase score for correct answer
        answerData.score = 10; // Store score for this question
    }

    // Log the score for debugging
    console.log("Current Score: " + score);

    // Submit the answer to the backend and store score in a separate JSON file
    fetch('/submit_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(answerData)
    })
    .then(response => response.json())
    .then(() => {
        alert("Answer submitted!");

        // Update the score button text with the current score
        document.getElementById('score-button').innerText = "Score: " + score;

        // Clear the subjective answer box after submitting
        document.getElementById('subjective-answer').value = ''; // Clear the subjective answer box

        // Fetch the next question after submission
        fetchQuestion();
    })
    .catch(error => console.error('Error submitting answer:', error));
}
fetchQuestion()