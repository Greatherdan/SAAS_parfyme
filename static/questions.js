const questions = [
    "What is your favorite scent?",
    "How would you describe your preferred intensity level? (e.g., Very Weak, Weak, Moderate, Strong, Very Strong)",
    "Do you have any specific notes or ingredients you like in a scent?",
    "On what occasions do you usually wear perfume?",
    "What scents do you generally like?",
    "Are there any scents you dislike?",
    "What is your gender?",
    "How important is longevity for you when it comes to perfume?",
    "What is your budget for a perfume?",
    "Is there any specific scent that reminds you of a special moment or event in your life that you would like to experience again?"
];
    
let currentQuestionIndex = 0;
const userResponses = [];

function displayQuestion() {
    const questionContainer = document.getElementById("question-container");
    questionContainer.innerHTML = `<p>${questions[currentQuestionIndex]}</p>`;
}

function getNextQuestion() {
    const userAnswer = document.getElementById("user-answer").value;
    userResponses.push(userAnswer);

    document.getElementById("user-answer").value = '';
    currentQuestionIndex++;

    const sendButton = document.getElementById("send-button");
    sendButton.disabled = true;

    if (currentQuestionIndex < questions.length) {
        displayQuestion();
    } else {
        alert("Thank you for answering the questions!");
        console.log("User Responses:", userResponses);
        sendUserResponses();
    }
}

function sendUserResponses() {
    const userResponsesData = { user_responses: userResponses };

    fetch('http://localhost:5000/process_responses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userResponsesData),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Recommendation data:', data);
            displayRecommendations(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function displayRecommendations(data) {
    const responseContainer = document.getElementById("response-container");
    responseContainer.innerHTML = `<p>GPT-3 Recommendation: ${data.gpt3_recommendation}</p>`;
    responseContainer.style.display = "block";
}

// Call displayQuestion() when the page loads
window.onload = displayQuestion;
