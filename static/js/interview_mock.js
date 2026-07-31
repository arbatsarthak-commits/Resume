/**
 * ResumeIQ AI - Mock Interview Session
 * Handles the interactive mock interview flow: question → answer → evaluate → next
 */

// Session state
const state = {
  questions: [],
  currentIndex: 0,
  answers: [],
  evaluations: [],
  type: "technical",
  difficulty: "medium",
  resumeText: null,
  jdText: null,
  mcqMode: false,
  mcqSelected: -1,
  isComplete: false
};

// DOM elements
const elements = {};

function initElements() {
  elements.questionText = document.getElementById("question-text");
  elements.questionCounter = document.getElementById("question-counter");
  elements.totalQuestions = document.getElementById("total-questions");
  elements.progressBar = document.getElementById("progress-bar-fill");
  elements.questionCategory = document.getElementById("question-category");
  elements.questionDifficulty = document.getElementById("question-difficulty");
  elements.answerInput = document.getElementById("answer-input");
  elements.submitBtn = document.getElementById("submit-answer-btn");
  elements.feedbackCard = document.getElementById("feedback-card");
  elements.mcqOptions = document.getElementById("mcq-options");
  elements.mcqChoices = document.getElementById("mcq-choices");
  elements.sessionComplete = document.getElementById("session-complete");
  elements.voiceBtn = document.getElementById("voice-btn");
  elements.voiceStatus = document.getElementById("voice-status");
  elements.nextBtn = document.getElementById("next-question-btn");

  // Evaluation elements
  elements.evalCommunication = document.getElementById("eval-communication");
  elements.evalCompleteness = document.getElementById("eval-completeness");
  elements.evalAccuracy = document.getElementById("eval-accuracy");
  elements.evalConfidence = document.getElementById("eval-confidence");
  elements.evalGrammar = document.getElementById("eval-grammar");
  elements.evalOverall = document.getElementById("eval-overall");
  elements.evalGoodPoints = document.getElementById("eval-good-points");
  elements.evalWeakPoints = document.getElementById("eval-weak-points");
  elements.evalBetterAnswer = document.getElementById("eval-better-answer");
  elements.evalBetterAnswerWrap = document.getElementById("eval-better-answer-wrap");

  // Final elements
  elements.finalAvgScore = document.getElementById("final-avg-score");
  elements.finalQuestionsCount = document.getElementById("final-questions-count");
  elements.finalReadiness = document.getElementById("final-readiness");
}

document.addEventListener("DOMContentLoaded", async () => {
  initElements();

  // Get URL parameters
  const params = new URLSearchParams(window.location.search);
  state.type = params.get("type") || "technical";
  state.difficulty = params.get("difficulty") || "medium";
  state.resumeText = params.get("resume") || null;
  state.jdText = params.get("jd") || null;

  // Load questions
  await loadQuestions();
});

async function loadQuestions() {
  showLoading(true);

  const result = await fetchQuestions(
    state.type,
    state.resumeText,
    state.jdText,
    5,
    state.difficulty
  );

  showLoading(false);

  if (!result.success || !result.questions || result.questions.length === 0) {
    elements.questionText.textContent = "No questions could be generated. Please try a different interview type.";
    elements.submitBtn.disabled = true;
    return;
  }

  state.questions = result.questions;

  // Check if MCQ mode
  state.mcqMode = result.questions[0].type === "mcq" && result.questions[0].options?.length > 0;

  if (state.mcqMode) {
    elements.mcqOptions.style.display = "block";
    elements.answerInput.style.display = "none";
  }

  elements.totalQuestions.textContent = state.questions.length;
  showQuestion(0);
}

function showQuestion(index) {
  if (index >= state.questions.length) {
    endSession();
    return;
  }

  const q = state.questions[index];
  state.currentIndex = index;

  elements.questionText.textContent = q.question;
  elements.questionCategory.textContent = q.category || "General";
  elements.questionDifficulty.textContent = q.difficulty || "medium";
  elements.questionCounter.textContent = `Question ${index + 1} of ${state.questions.length}`;
  elements.progressBar.style.width = `${((index + 1) / state.questions.length) * 100}%`;
  elements.answerInput.value = "";
  elements.feedbackCard.style.display = "none";
  elements.submitBtn.disabled = false;
  elements.submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> SUBMIT ANSWER';

  // Reset MCQ
  state.mcqSelected = -1;
  if (state.mcqMode) {
    elements.mcqChoices.innerHTML = q.options.map((opt, i) => `
      <label style="display: flex; align-items: center; gap: 0.8rem; padding: 0.7rem 1rem; border: 1px solid var(--border); border-radius: 8px; cursor: pointer; transition: all 0.2s;" 
             onmouseover="this.style.borderColor='var(--primary)'" 
             onmouseout="this.style.borderColor='var(--border)'">
        <input type="radio" name="mcq" value="${i}" onchange="selectMCQ(${i})" />
        <span>${opt}</span>
      </label>
    `).join('');
  }

  elements.answerInput.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function selectMCQ(index) {
  state.mcqSelected = index;
}

async function submitAnswer() {
  let answer = "";

  if (state.mcqMode) {
    if (state.mcqSelected === -1) {
      alert("Please select an answer.");
      return;
    }
    answer = state.questions[state.currentIndex].options[state.mcqSelected];
  } else {
    answer = elements.answerInput.value.trim();
    if (!answer) {
      alert("Please type your answer before submitting.");
      return;
    }
  }

  elements.submitBtn.disabled = true;
  elements.submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Evaluating...';

  const result = await evaluateAnswer(state.questions[state.currentIndex], answer);

  if (!result.success || !result.evaluation) {
    elements.submitBtn.disabled = false;
    elements.submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> SUBMIT ANSWER';
    alert("Failed to evaluate answer. Please try again.");
    return;
  }

  const evalData = result.evaluation;

  // Store in session
  state.answers.push(answer);
  state.evaluations.push(evalData);

  // Display feedback
  showFeedback(evalData);
}

function showFeedback(evalData) {
  elements.evalCommunication.textContent = evalData.communication;
  elements.evalCompleteness.textContent = evalData.completeness;
  elements.evalAccuracy.textContent = evalData.technical_accuracy;
  elements.evalConfidence.textContent = evalData.confidence;
  elements.evalGrammar.textContent = evalData.grammar;
  elements.evalOverall.textContent = evalData.overall_score;

  // Color coding
  const scoreEls = [
    elements.evalCommunication, elements.evalCompleteness,
    elements.evalAccuracy, elements.evalConfidence,
    elements.evalGrammar, elements.evalOverall
  ];
  scoreEls.forEach(el => {
    const val = parseInt(el.textContent);
    el.style.color = val >= 70 ? "var(--success)" : val >= 40 ? "var(--warning)" : "var(--danger)";
  });

  // Good points
  elements.evalGoodPoints.innerHTML = evalData.good_points?.length
    ? evalData.good_points.map(p => `<li>${p}</li>`).join('')
    : '<li style="color: var(--muted);">No specific good points identified.</li>';

  // Weak points
  elements.evalWeakPoints.innerHTML = evalData.weak_points?.length
    ? evalData.weak_points.map(p => `<li>${p}</li>`).join('')
    : '<li style="color: var(--muted);">No specific improvements needed.</li>';

  // Better answer
  if (evalData.better_answer) {
    elements.evalBetterAnswer.textContent = evalData.better_answer;
    elements.evalBetterAnswerWrap.style.display = "block";
  } else {
    elements.evalBetterAnswerWrap.style.display = "none";
  }

  elements.feedbackCard.style.display = "block";
  elements.submitBtn.innerHTML = '<i class="fa-solid fa-check"></i> SUBMITTED';
  elements.nextBtn.textContent = state.currentIndex < state.questions.length - 1
    ? '<i class="fa-solid fa-arrow-right"></i> NEXT QUESTION'
    : '<i class="fa-solid fa-flag-checkered"></i> FINISH INTERVIEW';

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function nextQuestion() {
  showQuestion(state.currentIndex + 1);
}

async function endSession() {
  elements.feedbackCard.style.display = "none";
  elements.mcqOptions.style.display = "none";
  elements.answerInput.style.display = "none";
  elements.submitBtn.style.display = "none";
  elements.voiceBtn.style.display = "none";
  elements.questionText.textContent = "Session complete!";

  const avgScore = state.evaluations.length > 0
    ? Math.round(state.evaluations.reduce((sum, e) => sum + e.overall_score, 0) / state.evaluations.length)
    : 0;

  // Calculate readiness
  const readinessResult = await calculateReadiness(null, null, state.evaluations, null, null);
  const readiness = readinessResult.success ? readinessResult.readiness : { readiness_score: 0, level: "N/A" };

  // Save session
  await saveSession({
    type: state.type,
    average_score: avgScore,
    questions: state.questions,
    answers: state.answers,
    evaluations: state.evaluations,
    readiness: readiness,
    summary: {
      total_questions: state.questions.length,
      answered: state.answers.length,
      average_score: avgScore,
      readiness_score: readiness.readiness_score
    }
  });

  // Show completion
  elements.finalAvgScore.textContent = `${avgScore}%`;
  elements.finalQuestionsCount.textContent = state.answers.length;
  elements.finalReadiness.textContent = `${readiness.readiness_score || 0}%`;
  elements.sessionComplete.style.display = "block";

  state.isComplete = true;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showLoading(isLoading) {
  if (isLoading) {
    elements.questionText.textContent = "Generating interview questions...";
    elements.submitBtn.disabled = true;
  }
}
