# ResumeIQ AI — Complete Transformation Plan

## Executive Summary

After thorough analysis of the existing codebase, the project has a **solid foundation** with:
- Complete deterministic ATS engine (scoring, parsing, skill extraction, matching)
- Dual-mode architecture (local SQLite ↔ AWS DynamoDB/S3)
- Working Flask REST API with 4 blueprints
- 8 functional HTML templates with Jinja2 + dark theme CSS
- AWS SAM infrastructure templates
- Comprehensive test suite (8 test files)

The transformation requires **6 major modules** to be built on top of this foundation.

---

## PHASE 1: Fixes & Foundation Hardening

### Step 1.1 — Fix Builder JS Bug
**File**: `static/js/builder.js`
**Issue**: Uses Python's `.strip()` on JavaScript strings (lines ~169-170)
**Fix**: Change `.strip()` → `.trim()`

### Step 1.2 — Add Auth Service (Login/Register/JWT)
**New Files**:
- `services/auth/auth_service.py` — JWT token generation, password hashing (bcrypt/werkzeug), login/register logic
- `routes/auth_routes.py` — POST /api/auth/register, POST /api/auth/login, POST /api/auth/forgot-password, GET /api/auth/profile, DELETE /api/auth/account
- `services/database/user_repository.py` — SQLiteUserRepository + DynamoDBUserRepository
- `templates/login.html`, `templates/register.html`, `templates/forgot_password.html`
- `static/js/auth.js`

**Modified Files**:
- `app.py` — Register auth blueprint, add login_required decorator, protect existing routes
- `templates/base.html` — Add login/logout/profile nav items
- `config.py` — Add JWT_SECRET, JWT_EXPIRY config vars

### Step 1.3 — Add Requirements
**File**: `requirements.txt`
**Add**: `bcrypt>=4.1.0`, `pyjwt>=2.8.0`, `gunicorn>=22.0.0`

---

## PHASE 2: AI Architecture

### Step 2.1 — AI Service Core
**New File**: `core/ai_service.py`

**Design**:
```python
class AIService:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.ai_available = bool(self.api_key)
    
    def generate_summary(self, skills, experience):
        if self.ai_available:
            return self._call_openai(prompt)
        return self._rule_based_summary(skills, experience)
    
    def improve_bullet_points(self, text):
        if self.ai_available:
            return self._call_openai(prompt)
        return self._rule_based_improve(text)
    
    # ... similar pattern for all AI features
```

**Features**:
- `generate_professional_summary(skills, experience)` — AI or rule-based
- `improve_bullet_points(text)` — Rewrite weak bullets
- `rewrite_experience(description)` — Improve wording only (NEVER invent)
- `improve_project_description(description)` — Better phrasing
- `generate_achievement_statement(role, context)` — STAR method framing
- `improve_skills_representation(skills)` — Better formatting
- `suggest_keywords(skills, job_title)` — Keyword optimization
- `generate_resume_headline(name, role, years)` — Professional headline
- `generate_cover_letter(name, company, role, skills)` — Cover letter
- `tailor_resume_for_jd(resume_data, jd_text)` — JD tailoring

**AI Guardrails** (CRITICAL):
- NEVER invent companies, skills, experience, certifications, numbers, achievements, or metrics
- Only improve wording, grammar, structure, and presentation
- All AI suggestions are prefixed with "[AI Suggestion]" in UI

### Step 2.2 — AI Routes
**New File**: `routes/ai_routes.py`
- `POST /api/ai/summary` — Generate professional summary
- `POST /api/ai/improve-bullets` — Improve bullet points
- `POST /api/ai/rewrite-experience` — Rewrite experience
- `POST /api/ai/improve-project` — Improve project description
- `POST /api/ai/achievement` — Generate achievement statement
- `POST /api/ai/skills` — Improve skills representation
- `POST /api/ai/keywords` — Suggest better keywords
- `POST /api/ai/headline` — Generate resume headline
- `POST /api/ai/cover-letter` — Generate cover letter
- `POST /api/ai/tailor` — Tailor resume for JD

---

## PHASE 3: AI Resume Builder Enhancements

### Step 3.1 — AI Assistant Panel in Builder
**Modified File**: `templates/builder.html`
**Add**: AI Assistant sidebar panel with buttons for each AI feature

### Step 3.2 — Resume Versioning
**New File**: `services/database/resume_repository.py`
**Modified File**: `routes/builder_routes.py`
- Add save/resume version endpoints
- Add list versions, load version, delete version

### Step 3.3 — Resume Duplication & Import
**Modified File**: `routes/builder_routes.py`
- POST /api/resumes/duplicate — Duplicate existing resume
- POST /api/resumes/import — Import from uploaded PDF/DOCX into builder form
- GET /api/resumes/export — Export resume data as JSON

### Step 3.4 — Auto-Save
**Modified File**: `static/js/builder.js`
- Add debounced auto-save (localStorage + server backup)
- Add "Restore last session" prompt on load

### Step 3.5 — Enhanced Drag & Drop
**New File**: `static/js/builder-dnd.js`
- Sortable sections using SortableJS or native HTML5 drag & drop

---

## PHASE 4: AI Interview Platform (BIGGEST NEW FEATURE)

### Step 4.1 — Interview Engine Core
**New File**: `core/interview_engine.py`

**Question Generation**:
```python
class InterviewEngine:
    def __init__(self, ai_service):
        self.ai = ai_service
    
    def generate_questions(self, type, resume_data=None, jd_text=None):
        # Types: hr, technical, behavioral, coding, system_design, mcq, resume_based, jd_based
        # Uses AI if available, else rule-based templates
        pass
    
    def evaluate_answer(self, question, answer):
        # Evaluate: communication, completeness, technical accuracy, confidence, grammar, STAR
        pass
    
    def calculate_readiness(self, resume_analysis, interview_performance, job_match):
        # Overall readiness score
        pass
```

**Question Categories**:
- HR: "Tell me about yourself", "Strengths/Weaknesses", "Why this company?"
- Technical: OOP, SQL, Python, JavaScript, Cloud, Docker, AWS Lambda, REST API, Flask, DynamoDB
- Behavioral: STAR method questions
- Coding: Algorithm/pseudocode challenges
- System Design: Design a URL shortener, design a chat system
- MCQ: Multiple choice technical questions
- Resume-based: Questions generated from user's resume content
- JD-based: Questions generated from job description

### Step 4.2 — Interview Routes
**New File**: `routes/interview_routes.py`
- POST /api/interview/questions — Generate questions
- POST /api/interview/evaluate — Evaluate answer
- POST /api/interview/start — Start mock interview session
- POST /api/interview/answer — Submit answer and get next
- GET /api/interview/history — Get interview history
- GET /api/interview/readiness — Get readiness score
- POST /api/interview/voice — Process voice input (speech-to-text)

### Step 4.3 — Interview Templates
**New Files**:
- `templates/interview.html` — Main interview dashboard
- `templates/interview_mock.html` — Mock interview session
- `templates/interview_history.html` — Past interview results
- `templates/interview_results.html` — Detailed feedback

### Step 4.4 — Interview JS
**New Files**:
- `static/js/interview.js` — Main interview logic
- `static/js/interview_mock.js` — Mock interview flow
- `static/js/interview_voice.js` — Web Speech API integration

### Step 4.5 — Voice Support
**Modified File**: `static/js/interview_voice.js`
- Use browser `webkitSpeechRecognition` / `SpeechRecognition`
- Convert speech to text
- Submit for evaluation
- Show confidence level of transcription

### Step 4.6 — Interview Readiness Score
**Modified File**: `core/interview_engine.py`
- Combine resume quality, ATS score, interview performance, job match, skill coverage
- Generate dashboard with readiness meter

---

## PHASE 5: Enhanced Career Dashboard

### Step 5.1 — Dashboard Analytics
**Modified File**: `templates/dashboard.html` → Enhanced version
**New File**: `static/js/dashboard.js` — Charts using Chart.js

**Metrics to Add**:
- Average ATS Score over time (line chart)
- Average Interview Score trend
- Top Skills radar chart
- Weak Skills analysis
- Recommended Skills based on job market
- Improvement Trend (sparkline)
- Recent Resumes list with quick actions

### Step 5.2 — Dashboard Routes
**Modified File**: `routes/analysis_routes.py`
- GET /api/dashboard/stats — Aggregated stats
- GET /api/dashboard/trends — Score trends over time
- GET /api/dashboard/skills — Skill analysis

### Step 5.3 — Requirements
**Add to `requirements.txt`**: `chart.js` via CDN (no npm needed)

---

## PHASE 6: Security & User Management

### Step 6.1 — JWT Middleware
**New File**: `middleware/auth_middleware.py`
- `@jwt_required` decorator for protecting routes
- Token verification
- Role checking (user, admin)

### Step 6.2 — User Profile
**Modified File**: `routes/auth_routes.py`
- GET/PUT /api/auth/profile — View/update profile
- POST /api/auth/change-password — Change password
- POST /api/auth/delete-account — Delete account + all data

### Step 6.3 — Private Resume Storage
**Modified Files**:
- `services/storage/local_storage.py` — Use user_id in path
- `services/storage/s3_storage.py` — Use user_id prefix in S3 key
- All routes — Filter by authenticated user

---

## PHASE 7: Deployment & DevOps

### Step 7.1 — GitHub Actions CI/CD
**New File**: `.github/workflows/ci-cd.yml`
- Run tests on push/PR
- Build Docker image
- Deploy to AWS (optional)

### Step 7.2 — Enhanced Docker
**Modified File**: `Dockerfile` — Multi-stage build
**Modified File**: `docker-compose.yml` — Add nginx reverse proxy, health checks

### Step 7.3 — Terraform (Optional Alternative)
**New File**: `infrastructure/terraform/main.tf`
- VPC, Lambda, API Gateway, S3, DynamoDB, Cognito

---

## PHASE 8: Bonus Features

### Step 8.1 — Resume Version Comparison
**New File**: `templates/compare.html`
**New File**: `static/js/compare.js`
- Side-by-side diff view of two resume versions

### Step 8.2 — LinkedIn Import
**Modified File**: `routes/builder_routes.py`
- POST /api/resumes/import-linkedin — Parse LinkedIn profile URL

### Step 8.3 — QR Code Resume
**New File**: `core/qr_generator.py`
- Generate QR code linking to resume share page
- Add to PDF download

### Step 8.4 — Resume Share Link
**New File**: `routes/share_routes.py`
- Generate unique shareable link with optional password protection

### Step 8.5 — Dark Mode Toggle
**Modified File**: `static/css/style.css` — CSS variables for light/dark
**Modified File**: `static/js/main.js` — Toggle functionality

---

## PHASE 9: Testing & Quality Assurance

### Step 9.1 — New Tests
- `tests/test_interview_engine.py` — Interview question generation, answer evaluation
- `tests/test_ai_service.py` — AI service fallback behavior
- `tests/test_auth.py` — Registration, login, JWT verification
- `tests/test_dashboard.py` — Aggregated stats

### Step 9.2 — Bug Fixes
- Fix `.strip()` → `.trim()` in builder.js
- Fix any failed tests
- Test all API endpoints
- Verify all templates render correctly

### Step 9.3 — Performance Optimization
- Add caching headers
- Optimize PDF generation
- Minimize CSS/JS

---

## FILE MANIFEST (Complete)

### New Files to Create:
1. `services/auth/__init__.py`
2. `services/auth/auth_service.py`
3. `routes/auth_routes.py`
4. `routes/ai_routes.py`
5. `routes/interview_routes.py`
6. `routes/share_routes.py`
7. `core/ai_service.py`
8. `core/interview_engine.py`
9. `core/qr_generator.py`
10. `services/database/user_repository.py`
11. `services/database/resume_repository.py`
12. `middleware/auth_middleware.py`
13. `templates/login.html`
