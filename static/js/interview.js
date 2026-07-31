/**
 * ResumeIQ AI - Interview Platform
 * Main interview logic for question generation and session management
 */

const INTERVIEW_API = "/api/interview";

/**
 * Fetch interview questions from the API.
 */
async function fetchQuestions(type, resumeData = null, jdText = null, count = 5, difficulty = "medium") {
  const payload = {
    type: type,
    count: count,
    difficulty: difficulty
  };

  if (resumeData) payload.resume_data = { text: resumeData };
  if (jdText) payload.jd_text = jdText;

  try {
    const response = await fetch(`${INTERVIEW_API}/questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return await response.json();
  } catch (err) {
    console.error("Failed to fetch questions:", err);
    return { success: false, error: "Connection error." };
  }
}

/**
 * Evaluate an answer via the API.
 */
async function evaluateAnswer(question, answer) {
  try {
    const response = await fetch(`${INTERVIEW_API}/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, answer })
    });
    return await response.json();
  } catch (err) {
    console.error("Failed to evaluate answer:", err);
    return { success: false, error: "Connection error." };
  }
}

/**
 * Calculate interview readiness score.
 */
async function calculateReadiness(resumeScore, atsScore, performances, jobMatchScore, skillCoverage) {
  try {
    const response = await fetch(`${INTERVIEW_API}/readiness`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_score: resumeScore,
        ats_score: atsScore,
        interview_performance: performances,
        job_match_score: jobMatchScore,
        skill_coverage: skillCoverage
      })
    });
    return await response.json();
  } catch (err) {
    console.error("Failed to calculate readiness:", err);
    return { success: false, error: "Connection error." };
  }
}

/**
 * Save an interview session to history.
 */
async function saveSession(sessionData) {
  try {
    const response = await fetch(`${INTERVIEW_API}/session/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(sessionData)
    });
    return await response.json();
  } catch (err) {
    console.error("Failed to save session:", err);
    return { success: false };
  }
}
