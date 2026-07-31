"""
ResumeIQ AI Service

Dual-mode architecture:
1. AI Mode (OpenAI API key configured) - Uses GPT models for intelligent suggestions
2. Rule-based Fallback Mode (No API key) - Uses deterministic templates and heuristics

CRITICAL GUARDRAILS:
- NEVER invent companies, skills, experience, certifications, numbers, achievements, or metrics
- Only improve wording, grammar, structure, and presentation
- AI suggestions are prefixed with "[AI Suggestion]" in UI
"""

import os
import re
import json
from typing import Dict, List, Optional, Any

from config import Config


class AIService:
    """AI-powered resume enhancement service with deterministic fallback."""

    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.ai_available = bool(self.api_key)
        self._client = None

    def _get_client(self):
        """Lazy-load OpenAI client."""
        if self._client is None and self.ai_available:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def _call_openai(self, system_prompt: str, user_prompt: str, max_tokens: int = 300) -> str:
        """Call OpenAI API with given prompts."""
        client = self._get_client()
        if not client:
            return ""

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f""

    # ============================================================
    # PROFESSIONAL SUMMARY
    # ============================================================

    def generate_professional_summary(self, skills: List[str], experience_years: str = "",
                                       current_role: str = "", top_achievements: List[str] = None) -> str:
        """Generate a professional summary based on user's actual data."""
        if self.ai_available and self._get_client():
            sys_prompt = """You are a professional resume writer. Generate a 2-3 line professional summary.
CRITICAL RULES:
- Use ONLY the skills and experience provided. NEVER invent anything.
- Only rephrase, restructure, and improve wording.
- Do NOT add companies, metrics, certifications, or achievements not provided.
- Keep it concise and impactful."""
            
            user_prompt = f"""Generate a professional summary using:
Skills: {', '.join(skills) if skills else 'Not specified'}
Experience: {experience_years if experience_years else 'Not specified'}
Current Role: {current_role if current_role else 'Not specified'}
Key Achievements: {', '.join(top_achievements) if top_achievements else 'Not specified'}"""
            
            result = self._call_openai(sys_prompt, user_prompt)
            if result:
                return result

        # Rule-based fallback
        return self._rule_based_summary(skills, current_role, experience_years)

    def _rule_based_summary(self, skills: List[str], role: str = "", experience: str = "") -> str:
        """Generate a professional summary using template-based approach."""
        parts = []
        if role:
            parts.append(f"Experienced {role}")
        elif skills:
            parts.append(f"Skilled professional")

        if experience:
            parts.append(f"with {experience} of hands-on experience")
        elif skills:
            parts.append("with a strong technical background")

        if skills:
            skill_str = ", ".join(skills[:5])
            if len(skills) > 5:
                skill_str += f", and {len(skills) - 5} more"
            parts.append(f"Proficient in {skill_str}")

        parts.append("passionate about delivering high-quality solutions and driving continuous improvement.")

        return " ".join(parts)

    # ============================================================
    # IMPROVE BULLET POINTS
    # ============================================================

    def improve_bullet_points(self, text: str, context: str = "") -> str:
        """Improve wording of bullet points without inventing facts."""
        if not text or not text.strip():
            return text

        if self.ai_available and self._get_client():
            sys_prompt = """Improve the wording of these resume bullet points.
CRITICAL RULES:
- ONLY improve grammar, sentence structure, and action verbs.
- NEVER add numbers, metrics, companies, technologies, or achievements not in the original.
- Keep the same factual content. Make it more professional and impactful.
- Return improved bullet points, one per line."""
            
            user_prompt = f"Context: {context}\n\nBullet points to improve:\n{text}"
            result = self._call_openai(sys_prompt, user_prompt, max_tokens=500)
            if result:
                return result

        # Rule-based fallback
        return self._rule_based_improve_bullets(text)

    def _rule_based_improve_bullets(self, text: str) -> str:
        """Improve bullet points using predefined transformations."""
        lines = text.strip().split("\n")
        improved = []
        action_verbs = [
            "Engineered", "Developed", "Implemented", "Designed", "Architected",
            "Optimized", "Enhanced", "Built", "Created", "Delivered",
            "Led", "Managed", "Spearheaded", "Established", "Automated"
        ]

        for line in lines:
            line = line.strip().strip("-•").strip()
            if not line:
                continue

            # Check if starts with action verb
            starts_with_verb = any(line.lower().startswith(v.lower()) for v in action_verbs)
            
            if not starts_with_verb:
                # Pick an appropriate verb
                if "responsib" in line.lower():
                    improved.append(f"Oversaw {line}")
                elif "work" in line.lower() or "collaborat" in line.lower():
                    improved.append(f"Collaborated {line}")
                elif "help" in line.lower():
                    improved.append(f"Contributed {line}")
                elif "use" in line.lower() or "utiliz" in line.lower():
                    improved.append(f"Leveraged {line}")
                else:
                    improved.append(f"Executed {line}")
            else:
                improved.append(line)

        return "\n".join(improved)

    # ============================================================
    # REWRITE EXPERIENCE
    # ============================================================

    def rewrite_experience(self, description: str, role: str = "", company: str = "") -> str:
        """Rewrite work experience description improving wording only."""
        if not description or not description.strip():
            return description

        if self.ai_available and self._get_client():
            sys_prompt = """Rewrite this work experience description to be more professional.
CRITICAL RULES:
- ONLY improve language, grammar, and structure.
- NEVER add responsibilities, technologies, metrics, or achievements not in the original.
- Keep ALL factual content exactly as provided.
- Use strong action verbs."""
            
            user_prompt = f"Role: {role}\nCompany: {company}\n\nDescription:\n{description}"
            result = self._call_openai(sys_prompt, user_prompt, max_tokens=500)
            if result:
                return result

        return self._rule_based_improve_bullets(description)

    # ============================================================
    # IMPROVE PROJECT DESCRIPTION
    # ============================================================

    def improve_project_description(self, description: str, tech_stack: str = "") -> str:
        """Improve project description wording."""
        if not description or not description.strip():
            return description

        if self.ai_available and self._get_client():
            sys_prompt = """Improve this project description.
CRITICAL RULES:
- ONLY improve wording, clarity, and impact.
- NEVER add features, technologies, results, or metrics not in the original.
- Keep all technical details exactly as provided."""
            
            user_prompt = f"Tech Stack: {tech_stack}\n\nDescription:\n{description}"
            result = self._call_openai(sys_prompt, user_prompt, max_tokens=400)
            if result:
                return result

        return self._rule_based_improve_bullets(description)

    # ============================================================
    # GENERATE ACHIEVEMENT STATEMENT
    # ============================================================

    def generate_achievement_statement(self, role: str, context: str, action: str) -> str:
        """Generate an achievement statement using STAR method framing."""
        if self.ai_available and self._get_client():
            sys_prompt = """Generate an achievement statement using STAR (Situation, Task, Action, Result) format.
CRITICAL RULES:
- Use ONLY the information provided.
- NEVER add numerical results, percentages, or metrics not provided.
- Frame the statement professionally."""
            
            user_prompt = f"Role: {role}\nContext/Situation: {context}\nAction Taken: {action}"
            result = self._call_openai(sys_prompt, user_prompt, max_tokens=250)
            if result:
                return result

        # Rule-based fallback
        return f"Leveraged expertise as {role} to {action.lower()}, contributing to {context.lower()}."

    # ============================================================
    # IMPROVE SKILLS REPRESENTATION
    # ============================================================

    def improve_skills_representation(self, skills: List[str], categories: Dict[str, List[str]] = None) -> str:
        """Improve how skills are categorized and presented."""
        if not skills:
            return ""

        if categories:
            result_parts = []
            for cat, skill_list in categories.items():
                if skill_list:
                    result_parts.append(f"{cat}: {', '.join(skill_list)}")
            return "\n".join(result_parts)

        # Simple grouping if no categories
        return ", ".join(skills)

    # ============================================================
    # SUGGEST KEYWORDS
    # ============================================================

    def suggest_keywords(self, skills: List[str], job_title: str = "") -> List[str]:
        """Suggest additional keywords based on existing skills."""
        # Always rule-based for safety (no inventing)
        keyword_map = {
            "Python": ["Python3", "Scripting", "Automation", "Backend Development"],
            "JavaScript": ["ES6", "Async/Await", "DOM Manipulation", "Web Development"],
            "TypeScript": ["Static Typing", "Interfaces", "Generics"],
            "React": ["Hooks", "State Management", "Component Design", "JSX"],
            "Flask": ["RESTful APIs", "WSGI", "Route Design", "Middleware"],
            "Django": ["ORM", "MTV Pattern", "Admin Interface"],
            "AWS": ["Cloud Computing", "Infrastructure", "Scalability", "Serverless"],
            "Docker": ["Containerization", "Image Management", "Docker Compose"],
            "SQL": ["Query Optimization", "Database Design", "Data Modeling"],
            "Git": ["Version Control", "Branching Strategy", "Code Review"],
            "REST API": ["API Design", "HTTP Methods", "JSON", "Endpoints"],
            "OOP": ["Design Patterns", "SOLID Principles", "Inheritance", "Polymorphism"],
        }

        suggestions = []
        for skill in skills:
            if skill in keyword_map:
                for kw in keyword_map[skill]:
                    if kw.lower() not in [s.lower() for s in suggestions]:
                        suggestions.append(kw)

        if job_title and "engineer" in job_title.lower():
            suggestions.extend(["Agile", "Scrum", "CI/CD", "Code Quality"])

        return suggestions[:10]

    # ============================================================
    # GENERATE RESUME HEADLINE
    # ============================================================

    def generate_resume_headline(self, name: str = "", current_role: str = "",
                                  experience_years: str = "", top_skills: List[str] = None) -> str:
        """Generate a professional resume headline."""
        parts = []
        if current_role:
            parts.append(current_role)
        if experience_years:
            parts.append(experience_years)
        if top_skills:
            skill_str = " | ".join(top_skills[:4])
            parts.append(skill_str)
        if not parts:
            parts.append("Professional")

        return " | ".join(parts)

    # ============================================================
    # GENERATE COVER LETTER
    # ============================================================

    def generate_cover_letter(self, name: str, company: str, role: str,
                               skills: List[str], experience_summary: str = "") -> str:
        """Generate a cover letter based on actual user data."""
        if self.ai_available and self._get_client():
            sys_prompt = """Write a professional cover letter.
CRITICAL RULES:
- Use ONLY the information provided. NEVER invent anything.
- Do NOT add specific metrics, achievements, or experiences not provided.
- Keep it concise (3-4 paragraphs).
- Address it properly with date, salutation, and closing."""
            
            user_prompt = f"""Write a cover letter for:
Name: {name}
Company: {company}
Role: {role}
Skills: {', '.join(skills) if skills else 'Not specified'}
Experience: {experience_summary if experience_summary else 'Not specified'}"""
            
            result = self._call_openai(sys_prompt, user_prompt, max_tokens=600)
            if result:
                return result

        # Rule-based fallback
        skill_str = ", ".join(skills[:8]) if skills else "my technical skills"
        return f"""Dear Hiring Manager,

I am writing to express my interest in the {role} position at {company}. With my background and expertise in {skill_str}, I am confident in my ability to contribute effectively to your team.

{experience_summary if experience_summary else "My professional experience has equipped me with the skills necessary to excel in this role."}

I am eager to bring my technical expertise and problem-solving abilities to {company}. Thank you for considering my application.

Best regards,
{name if name else "Applicant"}"""

    # ============================================================
    # TAILOR RESUME FOR JOB DESCRIPTION
    # ============================================================

    def tailor_resume_for_jd(self, resume_data: Dict[str, Any], jd_text: str,
                              matched_skills: List[str], missing_skills: List[str]) -> Dict[str, Any]:
        """Generate tailored resume suggestions for a specific job description."""
        suggestions = {
            "summary_tailoring": "",
            "skills_emphasis": [],
            "experience_highlights": [],
            "keyword_additions": [],
            "sections_to_strengthen": []
        }

        if missing_skills:
            suggestions["sections_to_strengthen"].append(
                f"Consider highlighting any experience related to: {', '.join(missing_skills[:5])}"
            )

        if matched_skills:
            suggestions["skills_emphasis"] = matched_skills[:8]
            suggestions["summary_tailoring"] = (
                f"Emphasize your expertise in {', '.join(matched_skills[:4])} "
                f"which are key requirements for this position."
            )

        return suggestions


# Singleton instance
_ai_service_instance = None


def get_ai_service() -> AIService:
    """Get or create the singleton AI service instance."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance

