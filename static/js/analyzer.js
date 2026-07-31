document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("analyzer-form");
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("resume-file");
  const fileInfo = document.getElementById("file-info");
  const errorAlert = document.getElementById("error-alert");
  const errorMessage = document.getElementById("error-message");
  const processingIndicator = document.getElementById("processing-indicator");
  const analyzeBtn = document.getElementById("analyze-btn");

  if (!dropzone || !fileInput) return;

  // Drag & Drop events
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
  });

  dropzone.addEventListener('drop', handleDrop, false);

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
      fileInput.files = files;
      updateFileInfo(files[0]);
    }
  }

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      updateFileInfo(fileInput.files[0]);
    }
  });

  function updateFileInfo(file) {
    hideError();
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx'].includes(ext)) {
      showError("Please upload a valid PDF or DOCX file.");
      fileInput.value = "";
      fileInfo.style.display = "none";
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      showError("File size exceeds 5MB limit. Please upload a smaller document.");
      fileInput.value = "";
      fileInfo.style.display = "none";
      return;
    }

    const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
    fileInfo.innerHTML = `<i class="fa-solid fa-file-pdf"></i> Selected: <strong>${file.name}</strong> (${sizeMb} MB)`;
    fileInfo.style.display = "block";
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    if (!fileInput.files || fileInput.files.length === 0) {
      showError("Please select a PDF or DOCX resume file to analyze.");
      return;
    }

    const formData = new FormData(form);

    // Show processing indicator
    processingIndicator.style.display = "block";
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = "0.6";

    try {
      const response = await fetch("/api/resumes/analyze", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        showError(result.error || "Analysis could not be completed. Please try again.");
        processingIndicator.style.display = "none";
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = "1";
        return;
      }

      // Successful analysis! Redirect to Dashboard with analysis_id
      window.location.href = `/dashboard/${result.analysis_id}`;

    } catch (err) {
      showError("Connection error. Analysis could not be completed. Please try again.");
      processingIndicator.style.display = "none";
      analyzeBtn.disabled = false;
      analyzeBtn.style.opacity = "1";
    }
  });

  function showError(msg) {
    errorMessage.textContent = msg;
    errorAlert.style.display = "block";
  }

  function hideError() {
    errorAlert.style.display = "none";
  }
});
