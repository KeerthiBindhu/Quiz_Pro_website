function addQuestion() {
    const container = document.getElementById('questionsContainer');
    const questionCount = container.children.length;
    const questionDiv = document.createElement('div');
    questionDiv.classList.add('question');
    questionDiv.innerHTML = `
        <h3>Question ${questionCount + 1}</h3>
        <input class="ques_input" type="text" name="questions" placeholder="Enter question text" required>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][0]" placeholder="Option 1" required>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][1]" placeholder="Option 2" required>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][2]" placeholder="Option 3" required>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][3]" placeholder="Option 4" required>
        <input class='ans_input' type="text" name="questions[${questionCount}][answer]" placeholder="Enter answer option as [1,2,3,4]" required>
    `;
    container.appendChild(questionDiv);
}

function nextQuestion() {
    const container = document.getElementById('questionsContainer');
    const questionCount = container.children.length;
    const questionDiv = document.createElement('div');
    questionDiv.classList.add('question');
    questionDiv.innerHTML = `
        <h3>Question ${questionCount + 1}</h3>
        <input class="ques_input" type="text" name="questions[${questionCount}][text]" placeholder="Enter question text" readonly>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][0]" placeholder="Option 1" readonly>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][1]" placeholder="Option 2" readonly>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][2]" placeholder="Option 3" readonly>
        <input class="opt_input" type="text" name="questions[${questionCount}][options][3]" placeholder="Option 4" readonly>
        <input class='ans_input' type="text" name="questions[${questionCount}][answer]" placeholder="Enter answer option as [1,2,3,4]" required>
    `;
    container.appendChild(questionDiv);
}