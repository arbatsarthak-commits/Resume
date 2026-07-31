# ResumeIQ — Cloud-Based Resume Builder & ATS Analyzer

**ResumeIQ** is a full-stack, production-quality SaaS application for ATS-friendly resume creation, PDF/DOCX text parsing, technical skill extraction, deterministic ATS compatibility scoring, and job-description matching.

It features a **dual-mode architecture** that works **100% locally out-of-the-box** using SQLite and local storage (zero AWS account or paid AI API keys required) while supporting serverless cloud deployment on AWS (Lambda, API Gateway, S3, and DynamoDB).

---

## 🌟 Key Features

- **Interactive Resume Builder (`/builder`)**:
  - Dynamic form fields with add, edit, delete, and reorder controls for Education, Experience, Projects, Skills, and Certifications.
  - Real-time desktop split-screen preview and mobile responsive view.
  - Template switcher: *Minimal ATS*, *Software Engineer*, *Modern Professional*.
  - Real PDF generation using ReportLab with selectable text (never image/screenshot based).

- **ATS Resume Analyzer (`/analyzer`)**:
  - Drag-and-drop PDF and DOCX document parser with file type, MIME, and 5MB size validation.
  - Detects scanned/image-only PDFs without readable text and alerts the user.
  - Extracts 10+ standard resume sections and synonyms.
  - Extracts 100+ technical skills categorized into Programming Languages, Frameworks, Databases, Cloud, DevOps, Tools, and Software Engineering concepts.
  - Alias normalization (e.g., `ReactJS` / `React.js` → `React`, `AWS` / `Amazon Web Services` → `AWS`) and word boundary protection (`\bC\b`).

- **Job Description Matcher (`/matcher`)**:
  - Compares resume text against target job descriptions.
  - Generates an Estimated ATS Job Match Score.
  - Displays matched skills and missing/undetected skill gaps truthfully.

- **Analytics Dashboard & History (`/dashboard`)**:
  - Scorecard summaries for General Quality and Job Match.
  - Score breakdown across Structure, Contact, Skills, Experience, Projects, Formatting, and Certifications.
  - Section analysis checklist (green checkmarks & red missing indicators).
  - Prioritized optimization recommendations (HIGH, MEDIUM, LOW).
  - Historical analysis log with view and permanent deletion capabilities.

---

## 🏗️ Architecture

```
                         FRONTEND (HTML5 / CSS3 / JavaScript / Jinja2)
                                              |
                                              v
                                       Flask REST API
                                              |
                  +---------------------------+---------------------------+
                  |                                                       |
                  v                                                       v
             LOCAL MODE                                              AWS CLOUD MODE
        - Local Storage Service                                   - Amazon API Gateway
        - SQLite Database (`data/resumeiq.db`)                    - AWS Lambda
                                                                  - Amazon S3 Bucket
                                                                  - Amazon DynamoDB Table
                  |                                                       |
                  +---------------------------+---------------------------+
                                              |
                                              v
                                     SHARED ATS CORE ENGINE
             +--------------------------------+--------------------------------+
             |                                |                                |
             v                                v                                v
       Document Parsers                ATS Scoring Engine              JD Matcher & Recs
     (PyMuPDF & python-docx)           (Deterministic 100 pts)         (Skill Gap Analyzer)
```

---

## 📊 ATS Scoring Methodology

Scoring is 100% deterministic and transparent. No random numbers or opaque third-party AI APIs.

### 1. General Resume Quality Score (Max 100)
Used when evaluating a resume independently:
- **Structure & Sections (25 pts)**: Evaluates presence of standard section headers.
- **Contact Information (10 pts)**: Email, phone number, LinkedIn/GitHub/Portfolio URLs.
- **Technical Skills (20 pts)**: Skill catalog breadth & categorization density.
- **Work Experience (15 pts)**: Work history presence and action-oriented content.
- **Projects (15 pts)**: Applied technical project details.
- **Formatting Hygiene (10 pts)**: Readable text density and length.
- **Certifications & Honors (5 pts)**: Verified credentials and achievements.

### 2. Job-Specific Match Score (Max 100)
Used when a Job Description is provided:
- **Keyword Match (30 pts)**: Domain keyword density ratio.
- **Skills Match (25 pts)**: Required technical skills match ratio.
- **Experience Relevance (15 pts)**: Work history alignment.
- **Projects Relevance (10 pts)**: Applied skill demonstration.
- **Resume Structure (10 pts)**: Section hierarchy.
- **Contact Info (5 pts)**: Reachability.
- **Formatting Hygiene (5 pts)**: Readability.

---

## 🚀 Local Installation & Setup

### Prerequisites
- Python 3.9+ installed
- Git
- Web Browser

### Step-by-Step Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ResumeIQ.git
   cd ResumeIQ
   ```

2. **Create and Activate Virtual Environment**:
   - **Windows (Command Prompt / PowerShell)**:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - **Windows (Command Prompt)**:
     ```cmd
     copy .env.example .env
     ```
   - **Linux / macOS**:
     ```bash
     cp .env.example .env
     ```

   *(Default `.env` configuration comes pre-set for `STORAGE_MODE=local` and `DATABASE_MODE=sqlite`)*

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Open in Browser**:
   Navigate to [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧪 Automated Testing

Run the full pytest suite:

```bash
pytest -v
```

Tests cover PDF text parsing, scanned document detection, DOCX parsing, header detection, skill taxonomy extraction with word boundaries, score determinism, job matching, SQLite CRUD, and REST API endpoints.

---

## 🐳 Optional Docker Execution

Build and run using Docker Compose:

```bash
docker compose up --build
```

Access at `http://localhost:5000`.

---

## ☁️ AWS Cloud Deployment (Optional)

Deploy to AWS using AWS SAM:

```bash
cd infrastructure
sam build
sam deploy --guided
```

Update your `.env` for Cloud Mode:
```env
STORAGE_MODE=aws
DATABASE_MODE=dynamodb
AWS_REGION=us-east-1
AWS_S3_BUCKET=<your-s3-bucket-name>
AWS_DYNAMODB_TABLE=resumeiq-analyses
```

---

## 🔒 Privacy & Security

- **Local Privacy**: Local mode keeps all uploaded resumes and SQLite records strictly on your local machine.
- **Cloud Security**: Cloud mode uses private S3 buckets and IAM least-privilege policies.
- **Data Deletion**: Built-in deletion endpoint removes both database records and stored files permanently.

---

## 📄 License

Distributed under the MIT License.
