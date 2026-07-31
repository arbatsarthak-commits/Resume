document.addEventListener("DOMContentLoaded", () => {
  const eduContainer = document.getElementById("education-container");
  const expContainer = document.getElementById("experience-container");
  const projContainer = document.getElementById("projects-container");
  const livePreview = document.getElementById("live-preview");

  // Initial Sample Data for Education
  addEducationItem("Stanford University", "Bachelor of Science", "Computer Science", "2020", "2024", "3.9 / 4.0");
  
  // Initial Sample Data for Experience
  addExperienceItem("TechCorp Solutions", "Software Engineer", "San Francisco, CA", "2024", "Present", "Developed scalable microservices using Python, Flask, and AWS Lambda.\nEngineered REST API endpoints processing 500k+ daily transactions.\nOptimized SQL database queries reducing latency by 35%.");

  // Initial Sample Data for Projects
  addProjectItem("ResumeIQ Cloud Platform", "Python, Flask, AWS Lambda, S3, Docker", "Built a dual-mode ATS resume analyzer and builder supporting PDF/DOCX parsing and deterministic scoring.", "https://github.com/johndoe/resumeiq");

  // Attach event listeners for real-time live preview synchronization
  document.querySelectorAll("input, textarea, select").forEach(input => {
    input.addEventListener("input", renderLivePreview);
    input.addEventListener("change", renderLivePreview);
  });

  // Dynamic Add Buttons
  document.getElementById("add-education-btn")?.addEventListener("click", () => addEducationItem());
  document.getElementById("add-experience-btn")?.addEventListener("click", () => addExperienceItem());
  document.getElementById("add-project-btn")?.addEventListener("click", () => addProjectItem());

  // Template switch listener
  document.getElementById("template-select")?.addEventListener("change", renderLivePreview);

  // PDF Download Trigger
  document.getElementById("download-pdf-btn")?.addEventListener("click", downloadPDF);

  renderLivePreview();

  // --- Dynamic Item Creators ---
  function addEducationItem(inst="", degree="", field="", start="", end="", gpa="") {
    const item = document.createElement("div");
    item.className = "dynamic-item";
    item.innerHTML = `
      <div class="grid-2">
        <div class="form-group"><label>Institution</label><input type="text" class="form-control edu-inst" value="${inst}" placeholder="University Name" /></div>
        <div class="form-group"><label>Degree</label><input type="text" class="form-control edu-degree" value="${degree}" placeholder="B.S. / M.S." /></div>
        <div class="form-group"><label>Field of Study</label><input type="text" class="form-control edu-field" value="${field}" placeholder="Computer Science" /></div>
        <div class="form-group"><label>Dates</label><input type="text" class="form-control edu-dates" value="${start && end ? start + ' - ' + end : ''}" placeholder="2020 - 2024" /></div>
        <div class="form-group"><label>CGPA / Percentage</label><input type="text" class="form-control edu-gpa" value="${gpa}" placeholder="3.8 / 4.0" /></div>
      </div>
      <div class="dynamic-item-actions">
        <button type="button" class="btn btn-danger btn-sm delete-btn"><i class="fa-solid fa-trash"></i> Delete</button>
      </div>
    `;
    item.querySelector(".delete-btn").addEventListener("click", () => { item.remove(); renderLivePreview(); });
    item.querySelectorAll("input").forEach(i => i.addEventListener("input", renderLivePreview));
    eduContainer.appendChild(item);
    renderLivePreview();
  }

  function addExperienceItem(comp="", role="", loc="", start="", end="", desc="") {
    const item = document.createElement("div");
    item.className = "dynamic-item";
    item.innerHTML = `
      <div class="grid-2">
        <div class="form-group"><label>Company</label><input type="text" class="form-control exp-company" value="${comp}" placeholder="Company Name" /></div>
        <div class="form-group"><label>Role / Position</label><input type="text" class="form-control exp-role" value="${role}" placeholder="Software Engineer" /></div>
        <div class="form-group"><label>Location</label><input type="text" class="form-control exp-location" value="${loc}" placeholder="San Francisco, CA" /></div>
        <div class="form-group"><label>Dates</label><input type="text" class="form-control exp-dates" value="${start && end ? start + ' - ' + end : ''}" placeholder="2022 - Present" /></div>
      </div>
      <div class="form-group">
        <label>Description (Bullet points on new lines)</label>
        <textarea class="form-control exp-desc" rows="3" placeholder="Bullet points describing your achievements...">${desc}</textarea>
      </div>
      <div class="dynamic-item-actions">
        <button type="button" class="btn btn-danger btn-sm delete-btn"><i class="fa-solid fa-trash"></i> Delete</button>
      </div>
    `;
    item.querySelector(".delete-btn").addEventListener("click", () => { item.remove(); renderLivePreview(); });
    item.querySelectorAll("input, textarea").forEach(i => i.addEventListener("input", renderLivePreview));
    expContainer.appendChild(item);
    renderLivePreview();
  }

  function addProjectItem(name="", tech="", desc="", url="") {
    const item = document.createElement("div");
    item.className = "dynamic-item";
    item.innerHTML = `
      <div class="grid-2">
        <div class="form-group"><label>Project Name</label><input type="text" class="form-control proj-name" value="${name}" placeholder="Project Title" /></div>
        <div class="form-group"><label>Tech Stack</label><input type="text" class="form-control proj-tech" value="${tech}" placeholder="Python, React, AWS" /></div>
      </div>
      <div class="form-group">
        <label>GitHub / Live URL</label>
        <input type="url" class="form-control proj-url" value="${url}" placeholder="https://github.com/username/repo" />
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea class="form-control proj-desc" rows="2" placeholder="Brief project summary and results...">${desc}</textarea>
      </div>
      <div class="dynamic-item-actions">
        <button type="button" class="btn btn-danger btn-sm delete-btn"><i class="fa-solid fa-trash"></i> Delete</button>
      </div>
    `;
    item.querySelector(".delete-btn").addEventListener("click", () => { item.remove(); renderLivePreview(); });
    item.querySelectorAll("input, textarea").forEach(i => i.addEventListener("input", renderLivePreview));
    projContainer.appendChild(item);
    renderLivePreview();
  }

  // --- Collect Form Data ---
  function getFormData() {
    const personal = {
      full_name: document.getElementById("full_name").value,
      email: document.getElementById("email").value,
      phone: document.getElementById("phone").value,
      location: document.getElementById("location").value,
      linkedin: document.getElementById("linkedin").value,
      github: document.getElementById("github").value,
      portfolio: document.getElementById("portfolio").value
    };

    const summary = document.getElementById("summary").value;

    const education = [];
    document.querySelectorAll("#education-container .dynamic-item").forEach(el => {
      const datesVal = el.querySelector(".edu-dates").value || "";
      const dateParts = datesVal.split("-");
      education.push({
        institution: el.querySelector(".edu-inst").value,
        degree: el.querySelector(".edu-degree").value,
        field: el.querySelector(".edu-field").value,
        start_date: (dateParts[0] || "").trim(),
        end_date: (dateParts[1] || "").trim(),
        cgpa: el.querySelector(".edu-gpa").value
      });
    });

    const experience = [];
    document.querySelectorAll("#experience-container .dynamic-item").forEach(el => {
      const datesVal = el.querySelector(".exp-dates").value || "";
      const dateParts = datesVal.split("-");
      experience.push({
        company: el.querySelector(".exp-company").value,
        role: el.querySelector(".exp-role").value,
        location: el.querySelector(".exp-location").value,
        start_date: (dateParts[0] || "").trim(),
        end_date: (dateParts[1] || "").trim(),
        description: el.querySelector(".exp-desc").value
      });
    });

    const projects = [];
    document.querySelectorAll("#projects-container .dynamic-item").forEach(el => {
      projects.push({
        name: el.querySelector(".proj-name").value,
        tech_stack: el.querySelector(".proj-tech").value,
        github_url: el.querySelector(".proj-url").value,
        description: el.querySelector(".proj-desc").value
      });
    });

    const skills = {
      Languages: document.getElementById("skills_languages").value.split(",").map(s=>s.trim()).filter(Boolean),
      Frameworks: document.getElementById("skills_frameworks").value.split(",").map(s=>s.trim()).filter(Boolean),
      Cloud: document.getElementById("skills_cloud").value.split(",").map(s=>s.trim()).filter(Boolean),
      Tools: document.getElementById("skills_tools").value.split(",").map(s=>s.trim()).filter(Boolean)
    };

    const certsRaw = document.getElementById("certifications").value.split("\n").map(s=>s.trim()).filter(Boolean);
    const achRaw = document.getElementById("achievements").value.split("\n").map(s=>s.trim()).filter(Boolean);

    return {
      template_id: document.getElementById("template-select").value,
      personal,
      summary,
      education,
      experience,
      projects,
      skills,
      certifications: certsRaw,
      achievements: achRaw
    };
  }

  // --- Render Desktop Live Preview ---
  function renderLivePreview() {
    const data = getFormData();
    const p = data.personal;

    let contactStr = [p.email, p.phone, p.location, p.linkedin, p.github, p.portfolio].filter(Boolean).join(" | ");

    let html = `
      <div style="font-family: Arial, sans-serif; color: #111827;">
        <h1 style="font-size: 1.6rem; font-weight: bold; margin-bottom: 0.2rem; text-transform: uppercase; color: #0f172a;">${p.full_name || 'JOHN DOE'}</h1>
        <p style="font-size: 0.8rem; color: #4b5563; margin-bottom: 0.8rem;">${contactStr}</p>
        <hr style="border: 0; border-top: 2px solid #2563eb; margin-bottom: 1rem;" />
    `;

    if (data.summary) {
      html += `
        <h3 style="font-size: 0.95rem; font-weight: bold; color: #2563eb; margin-bottom: 0.3rem;">PROFESSIONAL SUMMARY</h3>
        <p style="font-size: 0.85rem; line-height: 1.4; margin-bottom: 0.8rem; color: #374151;">${data.summary}</p>
      `;
    }

    if (data.education.length) {
      html += `<h3 style="font-size: 0.95rem; font-weight: bold; color: #2563eb; margin-bottom: 0.3rem;">EDUCATION</h3>`;
      data.education.forEach(e => {
        html += `
          <div style="margin-bottom: 0.5rem; font-size: 0.85rem;">
            <strong>${e.institution}</strong> — <i>${e.degree} ${e.field}</i> (${e.start_date})
            ${e.cgpa ? `<br/><span style="color: #6b7280;">GPA: ${e.cgpa}</span>` : ''}
          </div>
        `;
      });
    }

    if (data.experience.length) {
      html += `<h3 style="font-size: 0.95rem; font-weight: bold; color: #2563eb; margin-top: 0.8rem; margin-bottom: 0.3rem;">WORK EXPERIENCE</h3>`;
      data.experience.forEach(e => {
        const bullets = e.description ? e.description.split("\n").filter(Boolean).map(b => `<li>${b}</li>`).join('') : '';
        html += `
          <div style="margin-bottom: 0.6rem; font-size: 0.85rem;">
            <strong>${e.role}</strong> | ${e.company} <span style="color: #6b7280; font-size: 0.8rem;">(${e.start_date})</span>
            ${bullets ? `<ul style="padding-left: 1.1rem; margin-top: 0.2rem; color: #374151;">${bullets}</ul>` : ''}
          </div>
        `;
      });
    }

    if (data.projects.length) {
      html += `<h3 style="font-size: 0.95rem; font-weight: bold; color: #2563eb; margin-top: 0.8rem; margin-bottom: 0.3rem;">PROJECTS</h3>`;
      data.projects.forEach(pr => {
        html += `
          <div style="margin-bottom: 0.5rem; font-size: 0.85rem;">
            <strong>${pr.name}</strong> ${pr.tech_stack ? `| <i>${pr.tech_stack}</i>` : ''}
            <p style="color: #374151; margin-top: 0.1rem;">${pr.description}</p>
          </div>
        `;
      });
    }

    if (Object.keys(data.skills).length) {
      html += `<h3 style="font-size: 0.95rem; font-weight: bold; color: #2563eb; margin-top: 0.8rem; margin-bottom: 0.3rem;">TECHNICAL SKILLS</h3>`;
      for (const [cat, items] of Object.entries(data.skills)) {
        if (items.length) {
          html += `<p style="font-size: 0.85rem; color: #374151;"><strong>${cat}:</strong> ${items.join(", ")}</p>`;
        }
      }
    }

    html += `</div>`;
    livePreview.innerHTML = html;
  }

  // --- PDF Download Action ---
  async function downloadPDF() {
    const data = getFormData();
    if (!data.personal.full_name) {
      alert("Please fill in your Full Name before generating PDF.");
      return;
    }

    try {
      const response = await fetch("/api/resumes/build?download=true", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const res = await response.json();
        alert(res.error || "Failed to generate PDF.");
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${data.personal.full_name.replace(/\s+/g, '_')}_Resume.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("An error occurred generating the PDF document.");
    }
  }
});
