"""
ResumeIQ AI Interview Engine

Comprehensive interview preparation platform supporting:
- Question generation (HR, Technical, Behavioral, Coding, System Design, MCQ, Resume-based, JD-based)
- Answer evaluation (Communication, Completeness, Technical Accuracy, Confidence, Grammar, STAR Method)
- Interview Readiness Score
- Voice support via Web Speech API (handled in frontend)

Architecture:
- AI Mode: Uses OpenAI for intelligent question generation and evaluation
- Rule-based Fallback: Deterministic question banks and evaluation criteria
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from config import Config


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class InterviewQuestion:
    """Represents a single interview question."""
    id: str
    type: str  # hr, technical, behavioral, coding, system_design, mcq, resume_based, jd_based
    category: str
    question: str
    difficulty: str  # easy, medium, hard
    expected_keywords: List[str] = field(default_factory=list)
    sample_answer: str = ""
    options: List[str] = field(default_factory=list)  # For MCQ
    correct_option: int = -1  # Index of correct answer for MCQ


@dataclass
class AnswerEvaluation:
    """Represents evaluation of a user's answer."""
    communication: int  # 0-100
    completeness: int  # 0-100
    technical_accuracy: int  # 0-100
    confidence: int  # 0-100
    grammar: int  # 0-100
    star_method: int  # 0-100 (for behavioral)
    overall_score: int  # 0-100
    good_points: List[str] = field(default_factory=list)
    weak_points: List[str] = field(default_factory=list)
    missing_concepts: List[str] = field(default_factory=list)
    better_answer: str = ""


# ============================================================
# QUESTION BANKS (Rule-based Fallback)
# ============================================================

HR_QUESTIONS = [
    InterviewQuestion("hr_1", "hr", "General", "Tell me about yourself.", "easy",
                      ["experience", "background", "skills", "passion"],
                      "Start with your current role, briefly mention previous experience, highlight key skills, and end with what you're looking for."),
    InterviewQuestion("hr_2", "hr", "General", "What are your greatest strengths?", "easy",
                      ["strength", "skill", "example"],
                      "Choose 2-3 strengths relevant to the role, provide brief examples."),
    InterviewQuestion("hr_3", "hr", "General", "What are your weaknesses?", "medium",
                      ["weakness", "improving", "learning", "action"],
                      "Be honest about a real weakness, but explain how you're actively working to improve it."),
    InterviewQuestion("hr_4", "hr", "Motivation", "Why do you want to work here?", "medium",
                      ["company", "values", "growth", "contribute"],
                      "Research the company, mention specific aspects you admire, and connect to your career goals."),
    InterviewQuestion("hr_5", "hr", "Experience", "Describe a challenging situation you faced at work and how you handled it.", "hard",
                      ["challenge", "solution", "outcome", "learned"],
                      "Use STAR method: Situation, Task, Action, Result."),
    InterviewQuestion("hr_6", "hr", "Career", "Where do you see yourself in 5 years?", "medium",
                      ["growth", "skills", "leadership", "goals"],
                      "Show ambition aligned with the company's trajectory."),
    InterviewQuestion("hr_7", "hr", "Teamwork", "Describe a time you worked successfully as part of a team.", "medium",
                      ["team", "collaboration", "role", "contribution"],
                      "Focus on your specific contribution and how the team benefited."),
    InterviewQuestion("hr_8", "hr", "Conflict", "How do you handle conflict with coworkers?", "hard",
                      ["conflict", "communication", "resolution", "professional"],
                      "Emphasize professional communication and finding common ground."),
]

TECHNICAL_QUESTIONS = [
    InterviewQuestion("tech_1", "technical", "OOP", "Explain the four pillars of Object-Oriented Programming.", "easy",
                      ["encapsulation", "inheritance", "polymorphism", "abstraction"],
                      "Encapsulation: bundling data and methods. Inheritance: deriving classes. Polymorphism: many forms. Abstraction: hiding complexity."),
    InterviewQuestion("tech_2", "technical", "OOP", "What is the difference between abstraction and encapsulation?", "medium",
                      ["abstraction", "encapsulation", "hiding", "implementation"],
                      "Abstraction hides complexity and shows only functionality. Encapsulation hides internal state and requires all interaction through methods."),
    InterviewQuestion("tech_3", "technical", "Python", "What is the difference between a list and a tuple in Python?", "easy",
                      ["mutable", "immutable", "list", "tuple"],
                      "Lists are mutable (can be changed), tuples are immutable (cannot be changed after creation). Lists use [], tuples use ()."),
    InterviewQuestion("tech_4", "technical", "Python", "Explain decorators in Python and provide a use case.", "medium",
                      ["decorator", "function", "wrapper", "@"],
                      "Decorators are functions that modify the behavior of other functions. Common uses: logging, authentication, timing."),
    InterviewQuestion("tech_5", "technical", "Python", "What is the Global Interpreter Lock (GIL) in Python?", "hard",
                      ["GIL", "thread", "mutex", "parallelism", "CPython"],
                      "GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously."),
    InterviewQuestion("tech_6", "technical", "SQL", "Write a SQL query to find the second highest salary from an employees table.", "medium",
                      ["SELECT", "ORDER BY", "LIMIT", "OFFSET", "subquery"],
                      "SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;"),
    InterviewQuestion("tech_7", "technical", "SQL", "Explain the difference between INNER JOIN and LEFT JOIN.", "easy",
                      ["INNER JOIN", "LEFT JOIN", "matching", "NULL"],
                      "INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table and matching rows from the right (NULL for non-matches)."),
    InterviewQuestion("tech_8", "technical", "REST API", "What are the key principles of RESTful API design?", "medium",
                      ["stateless", "resources", "HTTP methods", "URI", "CRUD"],
                      "Stateless communication, resource-based URLs, standard HTTP methods (GET, POST, PUT, DELETE), proper status codes."),
    InterviewQuestion("tech_9", "technical", "REST API", "Explain the difference between PUT and PATCH HTTP methods.", "medium",
                      ["PUT", "PATCH", "update", "partial", "idempotent"],
                      "PUT replaces the entire resource. PATCH applies partial modifications."),
    InterviewQuestion("tech_10", "technical", "Database", "What is a database index and when should you use one?", "medium",
                      ["index", "performance", "query", "B-tree"],
                      "An index is a data structure that improves query speed. Use on columns used in WHERE, JOIN, and ORDER BY clauses."),
    InterviewQuestion("tech_11", "technical", "Cloud", "What is AWS Lambda and what are its use cases?", "medium",
                      ["Lambda", "serverless", "function", "event-driven", "scaling"],
                      "AWS Lambda is a serverless compute service that runs code in response to events. Use cases: API backends, file processing, scheduled tasks."),
    InterviewQuestion("tech_12", "technical", "Cloud", "Explain the difference between vertical and horizontal scaling.", "easy",
                      ["vertical", "horizontal", "scale up", "scale out"],
                      "Vertical scaling adds more power to existing machine. Horizontal scaling adds more machines."),
    InterviewQuestion("tech_13", "technical", "Docker", "What is Docker and how does it differ from a virtual machine?", "easy",
                      ["Docker", "container", "VM", "hypervisor", "OS kernel"],
                      "Docker containers share the host OS kernel and are lightweight. VMs include a full guest OS and are heavier."),
    InterviewQuestion("tech_14", "technical", "System Design", "Explain how you would design a URL shortener like TinyURL.", "hard",
                      ["hash", "database", "redirect", "scaling", "caching"],
                      "Use a hash function (e.g., Base62) to generate short codes. Store mapping in database. Redirect using 301/302. Use caching for hot URLs."),
    InterviewQuestion("tech_15", "technical", "JavaScript", "Explain the event loop in JavaScript.", "medium",
                      ["event loop", "call stack", "callback queue", "microtask", "async"],
                      "JavaScript event loop continuously checks call stack and callback queue. Microtasks (Promises) execute before macrotasks (setTimeout)."),
    InterviewQuestion("tech_16", "technical", "Flask", "What is Flask and how does it handle routing?", "easy",
                      ["Flask", "route", "decorator", "WSGI"],
                      "Flask is a lightweight WSGI web framework. Routes are defined using the @app.route() decorator mapping URLs to functions."),
    InterviewQuestion("tech_17", "technical", "DynamoDB", "What is DynamoDB and what are its key features?", "medium",
                      ["DynamoDB", "NoSQL", "key-value", "scaling", "SSD"],
                      "DynamoDB is AWS's fully managed NoSQL database. Key features: auto-scaling, single-digit millisecond performance, DAX caching."),
    InterviewQuestion("tech_18", "technical", "API Gateway", "What is Amazon API Gateway and how does it integrate with Lambda?", "medium",
                      ["API Gateway", "Lambda", "REST", "proxy", "throttling"],
                      "API Gateway creates RESTful APIs that can proxy requests to Lambda functions. Features: throttling, caching, authentication."),
]

BEHAVIORAL_QUESTIONS = [
    InterviewQuestion("beh_1", "behavioral", "Leadership", "Tell me about a time you led a team or project.", "medium",
                      ["lead", "team", "direction", "result", "STAR"],
                      "Use STAR: Describe the situation, your task as leader, actions you took, and the outcome."),
    InterviewQuestion("beh_2", "behavioral", "Problem Solving", "Describe a complex problem you solved.", "hard",
                      ["problem", "analyze", "solution", "implement", "result"],
                      "Walk through your problem-solving process: identify, analyze, develop solutions, implement, evaluate."),
    InterviewQuestion("beh_3", "behavioral", "Failure", "Tell me about a time you failed and what you learned.", "hard",
                      ["failure", "mistake", "learned", "improved"],
                      "Be honest about a real failure, but focus on lessons learned and how you improved."),
    InterviewQuestion("beh_4", "behavioral", "Initiative", "Describe a time you went above and beyond your job description.", "medium",
                      ["initiative", "extra", "impact", "proactive"],
                      "Describe a situation where you identified an opportunity and took proactive action."),
    InterviewQuestion("beh_5", "behavioral", "Adaptability", "Tell me about a time you had to adapt to a significant change at work.", "medium",
                      ["change", "adapt", "flexible", "learning"],
                      "Show your flexibility and positive attitude toward change."),
]

CODING_QUESTIONS = [
    InterviewQuestion("code_1", "coding", "Algorithms", "Write a function to check if a string is a palindrome.", "easy",
                      ["palindrome", "reverse", "two pointers", "O(n)"],
                      "Compare characters from both ends moving inward. O(n) time, O(1) space."),
    InterviewQuestion("code_2", "coding", "Algorithms", "Write a function to find the factorial of a number recursively.", "easy",
                      ["factorial", "recursion", "base case"],
                      "Base case: n <= 1 return 1. Recursive: n * factorial(n-1)."),
    InterviewQuestion("code_3", "coding", "Data Structures", "Implement a binary search algorithm.", "medium",
                      ["binary search", "sorted", "O(log n)", "divide"],
                      "Find middle, compare, narrow search space. O(log n) time complexity."),
    InterviewQuestion("code_4", "coding", "Data Structures", "Explain how you would reverse a linked list.", "medium",
                      ["linked list", "reverse", "pointers", "iteration"],
                      "Use three pointers: prev, current, next. Iterate through reversing links."),
]

SYSTEM_DESIGN_QUESTIONS = [
    InterviewQuestion("sd_1", "system_design", "Architecture", "Design a real-time chat application like WhatsApp.", "hard",
                      ["WebSocket", "message queue", "database", "scaling", "presence"],
                      "Use WebSockets for real-time, message queues for delivery, NoSQL for messages, sharding for scaling."),
    InterviewQuestion("sd_2", "system_design", "Architecture", "Design a scalable video streaming platform like YouTube.", "hard",
                      ["CDN", "transcoding", "storage", "caching", "microservices"],
                      "Use CDN for delivery, transcoding pipeline for formats, distributed storage, caching layer."),
    InterviewQuestion("sd_3", "system_design", "Architecture", "Design an e-commerce system like Amazon.", "hard",
                      ["microservices", "database", "caching", "search", "recommendation"],
                      "Microservices for catalog, cart, orders, payments. Use Elasticsearch for search, Redis for caching."),
]

MCQ_QUESTIONS = [
    InterviewQuestion("mcq_1", "mcq", "Python", "What will be the output of print(type([]))?", "easy",
                      ["list", "type"],
                      "",
                      ["<class 'tuple'>", "<class 'list'>", "<class 'dict'>", "<class 'array'>"],
                      1),
    InterviewQuestion("mcq_2", "mcq", "Python", "Which of the following is NOT a Python data type?", "easy",
                      ["data type"],
                      "",
                      ["List", "Dictionary", "Tuple", "Array (built-in)"],
                      3),
    InterviewQuestion("mcq_3", "mcq", "SQL", "Which SQL clause is used to filter records?", "easy",
                      ["SQL", "WHERE"],
                      "",
                      ["HAVING", "WHERE", "FILTER", "MATCH"],
                      1),
    InterviewQuestion("mcq_4", "mcq", "Cloud", "Which AWS service is used for serverless computing?", "easy",
                      ["Lambda", "serverless"],
                      "",
                      ["EC2", "Lambda", "S3", "RDS"],
                      1),
    InterviewQuestion("mcq_5", "mcq", "Docker", "What does 'docker-compose up' do?", "medium",
                      ["docker-compose", "container"],
                      "",
                      ["Stops all containers", "Builds and starts containers", "Deletes containers", "Pulls images only"],
                      1),
    InterviewQuestion("mcq_6", "mcq", "Git", "What command is used to create a new branch in Git?", "easy",
                      ["Git", "branch"],
                      "",
                      ["git branch new-branch", "git checkout new-branch", "git create new-branch", "git new new-branch"],
                      0),
    InterviewQuestion("mcq_7", "mcq", "REST", "Which HTTP method is used to update a resource completely?", "medium",
                      ["PUT", "HTTP"],
                      "",
                      ["POST", "PUT", "PATCH", "DELETE"],
                      1),
    InterviewQuestion("mcq_8", "mcq", "OOP", "Which principle means a class should have only one reason to change?", "medium",
                      ["SOLID", "single responsibility"],
                      "",
                      ["Single Responsibility", "Open-Closed", "Liskov Substitution", "Dependency Inversion"],
                      0),
]


# ============================================================
# INTERVIEW ENGINE
# ============================================================

class InterviewEngine:
    """Core interview engine for question generation and answer evaluation."""

    def __init__(self):
        self.ai_available = bool(Config.OPENAI_API_KEY)
        self._client = None
        self._question_banks = {
            "hr": HR_QUESTIONS,
            "technical": TECHNICAL_QUESTIONS,
            "behavioral": BEHAVIORAL_QUESTIONS,
            "coding": CODING_QUESTIONS,
            "system_design": SYSTEM_DESIGN_QUESTIONS,
            "mcq": MCQ_QUESTIONS,
        }

    def _get_client(self):
        if self._client is None and self.ai_available:
            from openai import OpenAI
            self._client = OpenAI(api_key=Config.OPENAI_API_KEY)
        return self._client

    # ============================================================
    # QUESTION GENERATION
    # ============================================================

    def generate_questions(
        self,
        interview_type: str = "mixed",
        resume_data: Optional[Dict[str, Any]] = None,
        jd_text: Optional[str] = None,
        count: int = 5,
        difficulty: str = "medium"
    ) -> List[InterviewQuestion]:
        """Generate interview questions based on type and context."""
        questions = []

        if interview_type == "resume_based" and resume_data:
            questions = self._generate_resume_based_questions(resume_data, count)
        elif interview_type == "jd_based" and jd_text:
            questions = self._generate_jd_based_questions(jd_text, count)
        elif interview_type == "mixed":
            questions = self._generate_mixed_questions(count, difficulty)
        elif interview_type in self._question_banks:
            questions = self._sample_questions(self._question_banks[interview_type], count)
        else:
            questions = self._generate_mixed_questions(count, difficulty)

        # If AI available, enhance questions with AI
        if self.ai_available and self._get_client() and interview_type in ("resume_based", "jd_based"):
            ai_questions = self._generate_ai_questions(interview_type, resume_data, jd_text, count)
            if ai_questions:
                questions = ai_questions

        return questions[:count]

    def _sample_questions(self, bank: List[InterviewQuestion], count: int) -> List[InterviewQuestion]:
        """Sample questions from a bank, ensuring variety."""
        import random
        if len(bank) <= count:
            return bank.copy()
        return random.sample(bank, count)

    def _generate_mixed_questions(self, count: int, difficulty: str) -> List[InterviewQuestion]:
        """Generate a mix of question types."""
        all_questions = []
        for bank in self._question_banks.values():
            all_questions.extend(bank)

        # Filter by difficulty if specified
        if difficulty != "mixed":
            filtered = [q for q in all_questions if q.difficulty == difficulty]
            if filtered:
                all_questions = filtered

        import random
        random.shuffle(all_questions)
        return all_questions[:count]

    def _generate_resume_based_questions(self, resume_data: Dict[str, Any], count: int) -> List[InterviewQuestion]:
        """Generate questions based on resume content."""
        questions = []
        skills = resume_data.get("skills", {})
        all_skills = []
        if isinstance(skills, dict):
            for cat_skills in skills.values():
                if isinstance(cat_skills, list):
                    all_skills.extend(cat_skills)
        elif isinstance(skills, list):
            all_skills = skills

        projects = resume_data.get("projects", [])
        experience = resume_data.get("experience", [])

        # Skills-based questions
        skill_questions_map = {
            "Python": "You have Python listed. Can you explain the difference between a list comprehension and a generator expression?",
            "Flask": "You have Flask experience. How does Flask handle routing and what is the request context?",
            "AWS": "You have AWS experience. Can you explain the shared responsibility model?",
            "Lambda": "You've worked with AWS Lambda. How do you handle cold starts and what are best practices?",
            "Docker": "You have Docker experience. Can you explain multi-stage builds?",
            "REST API": "You list REST API experience. What are the constraints of REST architecture?",
            "DynamoDB": "You have DynamoDB experience. How do you choose between a GSI and LSI?",
            "React": "You have React experience. Explain the virtual DOM and reconciliation.",
            "SQL": "You list SQL. Can you explain query execution order?",
            "JavaScript": "You have JavaScript experience. Explain closures and hoisting.",
        }

        for skill in all_skills:
            if skill in skill_questions_map and len(questions) < count:
                questions.append(InterviewQuestion(
                    f"res_{len(questions)+1}", "resume_based", skill,
                    skill_questions_map[skill], "medium",
                    [skill.lower(), "experience"]
                ))

        # Project-based questions
        for proj in projects:
            if len(questions) >= count:
                break
            proj_name = proj.get("name", "")
            if proj_name:
                questions.append(InterviewQuestion(
                    f"res_proj_{len(questions)+1}", "resume_based", "Project",
                    f"Can you explain the architecture of your project '{proj_name}' and your specific role?",
                    "medium", [proj_name.lower(), "architecture", "role"]
                ))

        # Experience-based questions
        for exp in experience:
            if len(questions) >= count:
                break
            company = exp.get("company", "")
            role = exp.get("role", "")
            if company and role:
                questions.append(InterviewQuestion(
                    f"res_exp_{len(questions)+1}", "resume_based", "Experience",
                    f"At {company}, you worked as {role}. What was your biggest achievement there?",
                    "medium", [company.lower(), role.lower(), "achievement"]
                ))

        # Fallback if no resume-specific questions
        if not questions:
            questions = self._sample_questions(HR_QUESTIONS + TECHNICAL_QUESTIONS, count)

        return questions[:count]

    def _generate_jd_based_questions(self, jd_text: str, count: int) -> List[InterviewQuestion]:
        """Generate questions based on job description."""
        from core.jd_parser import parse_job_description
        parsed = parse_job_description(jd_text)
        required_skills = parsed.get("required_skills", [])

        questions = []

        # Skills-based questions from JD
        skill_questions = {
            "Python": "The job requires Python. Can you describe your most complex Python project?",
            "AWS": "AWS skills are required. How would you design a cost-effective AWS architecture?",
            "Docker": "Docker is in the requirements. Explain how you containerize applications.",
            "Kubernetes": "Kubernetes is needed. Explain how you manage pod scaling.",
            "React": "React is required. How do you manage state in large React applications?",
            "SQL": "SQL is required. How do you optimize slow queries?",
            "REST API": "REST API experience is needed. How do you version APIs?",
            "Java": "Java is required. Explain the Spring Boot autoconfiguration.",
            "Node.js": "Node.js is listed. How does the event loop work?",
            "TypeScript": "TypeScript is needed. Explain advanced types like mapped types.",
        }

        for skill in required_skills:
            if skill in skill_questions and len(questions) < count:
                questions.append(InterviewQuestion(
                    f"jd_{len(questions)+1}", "jd_based", "JD Match",
                    skill_questions[skill], "medium",
                    [skill.lower()]
                ))

        if not questions:
            questions.append(InterviewQuestion(
                "jd_fallback_1", "jd_based", "JD Match",
                f"The job description mentions {', '.join(required_skills[:5])}. How does your experience align with these requirements?",
                "medium", [s.lower() for s in required_skills[:3]]
            ))

        return questions[:count]

    def _generate_ai_questions(self, interview_type: str, resume_data, jd_text, count: int) -> List[InterviewQuestion]:
        """Use AI to generate context-specific questions."""
        client = self._get_client()
        if not client:
            return []

        try:
            if interview_type == "resume_based" and resume_data:
                prompt = f"Generate {count} interview questions based on this resume: {json.dumps(resume_data)}"
            elif interview_type == "jd_based" and jd_text:
                prompt = f"Generate {count} interview questions based on this job description: {jd_text[:1000]}"
            else:
                return []

            sys_prompt = """Generate interview questions. Return as JSON array with fields: question, type, category, difficulty.
CRITICAL: Use ONLY the information provided. Do NOT invent skills or experience not present."""

            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            text = response.choices[0].message.content.strip()
            
            # Try to parse JSON from response
            import json as json_lib
            # Find JSON array in response
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                questions_data = json_lib.loads(json_match.group())
                return [
                    InterviewQuestion(
                        f"ai_{i}", q.get("type", "technical"),
                        q.get("category", "General"),
                        q["question"], q.get("difficulty", "medium")
                    )
                    for i, q in enumerate(questions_data)
                ]
        except Exception:
            pass

        return []

    # ============================================================
    # ANSWER EVALUATION
    # ============================================================

    def evaluate_answer(self, question: InterviewQuestion, answer: str) -> AnswerEvaluation:
        """Evaluate a user's answer to an interview question."""
        if not answer or not answer.strip():
            return AnswerEvaluation(
                communication=0, completeness=0, technical_accuracy=0,
                confidence=0, grammar=0, star_method=0, overall_score=0,
                good_points=[], weak_points=["No answer provided."],
                missing_concepts=question.expected_keywords,
                better_answer=question.sample_answer
            )

        # Use AI evaluation if available
        if self.ai_available and self._get_client():
            ai_eval = self._evaluate_with_ai(question, answer)
            if ai_eval:
                return ai_eval

        # Rule-based evaluation
        return self._rule_based_evaluation(question, answer)

    def _evaluate_with_ai(self, question: InterviewQuestion, answer: str) -> Optional[AnswerEvaluation]:
        """Use AI to evaluate an answer."""
        client = self._get_client()
        if not client:
            return None

        try:
            sys_prompt = """Evaluate this interview answer. Return ONLY valid JSON:
{
    "communication": 0-100,
    "completeness": 0-100,
    "technical_accuracy": 0-100,
    "confidence": 0-100,
    "grammar": 0-100,
    "star_method": 0-100 (for behavioral),
    "overall_score": 0-100,
    "good_points": ["point1", "point2"],
    "weak_points": ["point1"],
    "missing_concepts": ["concept1"],
    "better_answer": "improved answer"
}

IMPORTANT: 
- Evaluate based on the actual content. Do NOT invent criteria.
- Be fair and specific in feedback."""

            user_prompt = f"Question: {question.question}\n\nAnswer: {answer}\n\nExpected keywords: {', '.join(question.expected_keywords)}"

            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )

            text = response.choices[0].message.content.strip()
            # Extract JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                eval_data = json.loads(json_match.group())
                return AnswerEvaluation(
                    communication=eval_data.get("communication", 50),
                    completeness=eval_data.get("completeness", 50),
                    technical_accuracy=eval_data.get("technical_accuracy", 50),
                    confidence=eval_data.get("confidence", 50),
                    grammar=eval_data.get("grammar", 50),
                    star_method=eval_data.get("star_method", 0),
                    overall_score=eval_data.get("overall_score", 50),
                    good_points=eval_data.get("good_points", []),
                    weak_points=eval_data.get("weak_points", []),
                    missing_concepts=eval_data.get("missing_concepts", []),
                    better_answer=eval_data.get("better_answer", "")
                )
        except Exception:
            pass

        return None

    def _rule_based_evaluation(self, question: InterviewQuestion, answer: str) -> AnswerEvaluation:
        """Evaluate answer using deterministic rules."""
        answer_lower = answer.lower()
        words = answer.split()
        word_count = len(words)

        # === Communication Score ===
        # Based on answer length, structure, clarity
        comm_score = min(100, max(20, word_count * 3))
        if word_count < 10:
            comm_score = 20
        elif word_count < 30:
            comm_score = 40
        elif word_count < 60:
            comm_score = 60
        elif word_count < 100:
            comm_score = 80
        else:
            comm_score = 90

        # === Completeness Score ===
        # Based on keyword coverage
        expected_keywords = question.expected_keywords
        if expected_keywords:
            matched = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
            completeness = int((matched / len(expected_keywords)) * 100)
        else:
            completeness = min(100, word_count * 5)

        # === Technical Accuracy ===
        # Check for correct technical terms
        tech_accuracy = max(30, completeness - 10)
        if question.type == "technical" and completeness < 30:
            tech_accuracy = 20

        # === Confidence Score ===
        # Based on hedging words vs definitive statements
        hedging_words = ["maybe", "perhaps", "i think", "not sure", "might", "possibly", "kind of"]
        confidence_boosters = ["definitely", "certainly", "absolutely", "i know", "confident", "sure"]
        
        hedging_count = sum(1 for hw in hedging_words if hw in answer_lower)
        booster_count = sum(1 for cb in confidence_boosters if cb in answer_lower)
        confidence = max(20, 70 - (hedging_count * 15) + (booster_count * 10))
        confidence = min(100, confidence)

        # === Grammar Score ===
        # Simple heuristic based on sentence structure
        sentences = [s.strip() for s in answer.split(".") if s.strip()]
        if sentences:
            avg_words_per_sentence = word_count / len(sentences)
            if avg_words_per_sentence < 3:
                grammar = 40  # Too short sentences
            elif avg_words_per_sentence > 50:
                grammar = 50  # Run-on
            else:
                grammar = 75
        else:
            grammar = 30

        # === STAR Method (for behavioral) ===
        star_score = 0
        if question.type == "behavioral":
            star_elements = {
                "situation": ["situation", "context", "background", "when"],
                "task": ["task", "goal", "objective", "needed to"],
                "action": ["action", "did", "implemented", "created", "developed", "led"],
                "result": ["result", "outcome", "achieved", "improved", "delivered"]
            }
            found_elements = 0
            for element, keywords in star_elements.items():
                if any(kw in answer_lower for kw in keywords):
                    found_elements += 1
            star_score = (found_elements / 4) * 100

        # === Overall Score ===
        overall = int((comm_score + completeness + tech_accuracy + confidence + grammar + star_score) / 6)

        # === Generate Feedback ===
        good_points = []
        weak_points = []
        missing_concepts = []

        if completeness >= 60:
            good_points.append("Good coverage of key concepts")
        else:
            weak_points.append("Could cover more key concepts related to the question")
            for kw in expected_keywords:
                if kw.lower() not in answer_lower:
                    missing_concepts.append(kw)

        if confidence >= 60:
            good_points.append("Shows confidence in the response")
        else:
            weak_points.append("Consider using more definitive language")

        if grammar >= 60:
            good_points.append("Good grammar and sentence structure")
        else:
            weak_points.append("Work on sentence structure and clarity")

        if question.type == "behavioral" and star_score >= 60:
            good_points.append("Good use of STAR method structure")
        elif question.type == "behavioral":
            weak_points.append("Structure your answer using the STAR method (Situation, Task, Action, Result)")

        if word_count >= 50:
            good_points.append("Comprehensive answer length")
        else:
            weak_points.append("Consider providing more detail in your answer")

        return AnswerEvaluation(
            communication=comm_score,
            completeness=completeness,
            technical_accuracy=tech_accuracy,
            confidence=confidence,
            grammar=grammar,
            star_method=star_score,
            overall_score=overall,
            good_points=good_points,
            weak_points=weak_points,
            missing_concepts=missing_concepts,
            better_answer=question.sample_answer
        )

    # ============================================================
    # INTERVIEW READINESS SCORE
    # ============================================================

    def calculate_readiness_score(
        self,
        resume_score: Optional[int] = None,
        ats_score: Optional[int] = None,
        interview_performance: Optional[List[AnswerEvaluation]] = None,
        job_match_score: Optional[int] = None,
        skill_coverage: Optional[float] = None
    ) -> Dict[str, Any]:
        """Calculate overall interview readiness score."""
        components = []

        # Resume quality (25% weight)
        if resume_score is not None:
            components.append(("Resume Quality", resume_score, 25))

        # ATS compatibility (20% weight)
        if ats_score is not None:
            components.append(("ATS Compatibility", ats_score, 20))

        # Interview performance (30% weight)
        if interview_performance and len(interview_performance) > 0:
            avg_interview = int(sum(e.overall_score for e in interview_performance) / len(interview_performance))
            components.append(("Interview Performance", avg_interview, 30))

        # Job match (15% weight)
        if job_match_score is not None:
            components.append(("Job Match", job_match_score, 15))

        # Skill coverage (10% weight)
        if skill_coverage is not None:
            skill_score = int(skill_coverage * 100)
            components.append(("Skill Coverage", skill_score, 10))

        if not components:
            return {
                "readiness_score": 0,
                "level": "Not Assessed",
                "components": [],
                "message": "No data available for readiness calculation."
            }

        total_weight = sum(w for _, _, w in components)
        weighted_sum = sum(score * weight for _, score, weight in components)
        readiness_score = int(weighted_sum / total_weight) if total_weight > 0 else 0

        # Determine level
        if readiness_score >= 85:
            level = "Excellent"
            message = "You are well-prepared for interviews. Continue practicing to maintain your edge."
        elif readiness_score >= 70:
            level = "Good"
            message = "You have solid preparation. Focus on weaker areas to improve further."
        elif readiness_score >= 50:
            level = "Moderate"
            message = "You have a foundation but need more practice in key areas."
        elif readiness_score >= 30:
            level = "Needs Work"
            message = "Significant preparation needed. Focus on resume optimization and interview practice."
        else:
            level = "Beginner"
            message = "Start by building a strong resume and practicing common interview questions."

        return {
            "readiness_score": readiness_score,
            "level": level,
            "message": message,
            "components": [
                {"name": name, "score": score, "weight": weight}
                for name, score, weight in components
            ]
        }


# Singleton instance
_interview_engine_instance = None


def get_interview_engine() -> InterviewEngine:
    """Get or create the singleton interview engine instance."""
    global _interview_engine_instance
    if _interview_engine_instance is None:
        _interview_engine_instance = InterviewEngine()
    return _interview_engine_instance

