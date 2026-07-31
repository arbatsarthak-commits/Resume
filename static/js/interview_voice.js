/**
 * ResumeIQ AI - Interview Voice Support
 * Uses Web Speech API for speech-to-text transcription
 */

let recognition = null;
let isListening = false;

/**
 * Initialize speech recognition.
 */
function initVoice() {
  if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
    const statusEl = document.getElementById("voice-status");
    if (statusEl) {
      statusEl.textContent = "Voice not supported in this browser.";
    }
    const voiceBtn = document.getElementById("voice-btn");
    if (voiceBtn) {
      voiceBtn.disabled = true;
      voiceBtn.style.opacity = "0.5";
    }
    return false;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
    let interimTranscript = "";
    let finalTranscript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript;
      } else {
        interimTranscript += transcript;
      }
    }

    const answerInput = document.getElementById("answer-input");
    if (answerInput && finalTranscript) {
      // Append final transcript to existing text
      const existing = answerInput.value;
      answerInput.value = existing ? existing + " " + finalTranscript : finalTranscript;
      answerInput.dispatchEvent(new Event("input"));
    }

    if (interimTranscript) {
      const statusEl = document.getElementById("voice-status");
      if (statusEl) {
        statusEl.textContent = `Listening: ${interimTranscript}`;
      }
    }
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    stopVoice();
    const statusEl = document.getElementById("voice-status");
    if (statusEl) {
      if (event.error === "not-allowed") {
        statusEl.textContent = "Microphone access denied. Please allow microphone permissions.";
      } else {
        statusEl.textContent = `Error: ${event.error}. Please type your answer.`;
      }
    }
  };

  recognition.onend = () => {
    if (isListening) {
      // Auto-restart if still listening
      try {
        recognition.start();
      } catch (e) {
        isListening = false;
        updateVoiceUI();
      }
    } else {
      updateVoiceUI();
    }
  };

  return true;
}

/**
 * Toggle voice recognition on/off.
 */
function toggleVoice() {
  if (!recognition) {
    const initialized = initVoice();
    if (!initialized) return;
  }

  if (isListening) {
    stopVoice();
  } else {
    startVoice();
  }
}

/**
 * Start voice recognition.
 */
function startVoice() {
  if (!recognition) return;

  try {
    recognition.start();
    isListening = true;
    updateVoiceUI();
  } catch (e) {
    console.error("Failed to start voice recognition:", e);
  }
}

/**
 * Stop voice recognition.
 */
function stopVoice() {
  if (!recognition) return;

  try {
    recognition.stop();
  } catch (e) {
    // Ignore errors on stop
  }

  isListening = false;
  updateVoiceUI();
}

/**
 * Update voice button UI based on state.
 */
function updateVoiceUI() {
  const voiceBtn = document.getElementById("voice-btn");
  const voiceLabel = document.getElementById("voice-label");
  const voiceStatus = document.getElementById("voice-status");

  if (!voiceBtn || !voiceLabel) return;

  if (isListening) {
    voiceBtn.style.borderColor = "var(--danger)";
    voiceBtn.style.background = "rgba(248, 113, 113, 0.15)";
    voiceLabel.textContent = "Stop Recording";
    if (voiceStatus) {
      voiceStatus.textContent = "Listening... Speak clearly.";
    }
  } else {
    voiceBtn.style.borderColor = "var(--border)";
    voiceBtn.style.background = "";
    voiceLabel.textContent = "Speak Answer";
    if (voiceStatus) {
      voiceStatus.textContent = "";
    }
  }
}

// Initialize voice on load
document.addEventListener("DOMContentLoaded", () => {
  if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    initVoice();
  }
});
