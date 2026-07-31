import re
from typing import Dict, List, Set, Any

SKILL_TAXONOMY = {
    "PROGRAMMING LANGUAGES": {
        "Python": [r"\bpython\b", r"\bpython3\b"],
        "Java": [r"\bjava\b"],
        "C": [r"\bc\b"],
        "C++": [r"\bc\+\+", r"\bcpp\b"],
        "C#": [r"\bc\#", r"\bcsharp\b"],
        "JavaScript": [r"\bjavascript\b", r"\bjs\b", r"\bes6\b"],
        "TypeScript": [r"\btypescript\b", r"\bts\b"],
        "Go": [r"\bgo\b", r"\bgolang\b"],
        "Rust": [r"\brust\b"],
        "PHP": [r"\bphp\b"],
        "Kotlin": [r"\bkotlin\b"],
        "Swift": [r"\bswift\b"],
        "R": [r"\br\b"],
        "SQL": [r"\bsql\b"]
    },
    "FRAMEWORKS": {
        "React": [r"\breact\b", r"\breactjs\b", r"\breact\.js\b"],
        "Angular": [r"\bangular\b", r"\bangularjs\b", r"\bangular 2\+\b"],
        "Vue": [r"\bvue\b", r"\bvuejs\b", r"\bvue\.js\b"],
        "Flask": [r"\bflask\b"],
        "Django": [r"\bdjango\b"],
        "FastAPI": [r"\bfastapi\b"],
        "Spring": [r"\bspring\b", r"\bspring boot\b"],
        "Node.js": [r"\bnode\.js\b", r"\bnodejs\b", r"\bnode\b"],
        "Express": [r"\bexpress\b", r"\bexpressjs\b", r"\bexpress\.js\b"],
        "Next.js": [r"\bnext\.js\b", r"\bnextjs\b"],
        "Tailwind": [r"\btailwind\b", r"\btailwindcss\b"],
        "Bootstrap": [r"\bbootstrap\b"]
    },
    "DATABASES": {
        "MySQL": [r"\bmysql\b"],
        "PostgreSQL": [r"\bpostgresql\b", r"\bpostgres\b"],
        "MongoDB": [r"\bmongodb\b", r"\bmongo\b"],
        "SQLite": [r"\bsqlite\b", r"\bsqlite3\b"],
        "DynamoDB": [r"\bdynamodb\b", r"\baws dynamodb\b"],
        "Redis": [r"\bredis\b"],
        "Oracle": [r"\boracle db\b", r"\boracle database\b"],
        "Elasticsearch": [r"\belasticsearch\b"]
    },
    "CLOUD": {
        "AWS": [r"\baws\b", r"\bamazon web services\b"],
        "Azure": [r"\bazure\b", r"\bmicrosoft azure\b"],
        "GCP": [r"\bgcp\b", r"\bgoogle cloud\b", r"\bgoogle cloud platform\b"],
        "EC2": [r"\bec2\b", r"\bamazon ec2\b"],
        "Lambda": [r"\blambda\b", r"\baws lambda\b"],
        "S3": [r"\bs3\b", r"\bamazon s3\b"],
        "API Gateway": [r"\bapi gateway\b", r"\baws api gateway\b"],
        "CloudFront": [r"\bcloudfront\b"]
    },
    "DEVOPS": {
        "Docker": [r"\bdocker\b"],
        "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
        "Jenkins": [r"\bjenkins\b"],
        "GitHub Actions": [r"\bgithub actions\b"],
        "Terraform": [r"\bterraform\b"],
        "CI/CD": [r"\bci/cd\b", r"\bci\s*/\s*cd\b", r"\bcontinuous integration\b"]
    },
    "TOOLS": {
        "Git": [r"\bgit\b"],
        "GitHub": [r"\bgithub\b"],
        "Postman": [r"\bpostman\b"],
        "Linux": [r"\blinux\b", r"\bubuntu\b"],
        "VS Code": [r"\bvs code\b", r"\bvscode\b", r"\bvisual studio code\b"],
        "Jira": [r"\bjira\b"]
    },
    "SOFTWARE ENGINEERING": {
        "REST API": [r"\brest api\b", r"\brestful api\b", r"\brest apis\b", r"\brest\b"],
        "OOP": [r"\boop\b", r"\bobject oriented programming\b"],
        "SDLC": [r"\bsdlc\b", r"\bsoftware development life cycle\b"],
        "Agile": [r"\bagile\b", r"\bscrum\b"],
        "Software Testing": [r"\bsoftware testing\b", r"\bunit testing\b", r"\bpytest\b"],
        "Data Structures": [r"\bdata structures\b", r"\bdsa\b"],
        "Algorithms": [r"\balgorithms\b"],
        "Microservices": [r"\bmicroservices\b", r"\bmicroservice architecture\b"]
    }
}

def extract_skills(text: str) -> Dict[str, Any]:
    """
    Extracts technical skills from normalized text using strict pattern boundaries and aliases.
    Returns dict containing flat list of detected skills and categorized breakdown.
    """
    if not text:
        return {"detected_skills": [], "categorized_skills": {}}

    detected_skills_set: Set[str] = set()
    categorized: Dict[str, List[str]] = {}

    lower_text = text.lower()

    for category, skills_dict in SKILL_TAXONOMY.items():
        cat_skills = []
        for canonical_name, patterns in skills_dict.items():
            matched = False
            for pat in patterns:
                # Use regex search with word boundaries
                if re.search(pat, lower_text, re.IGNORECASE):
                    matched = True
                    break
            if matched:
                detected_skills_set.add(canonical_name)
                cat_skills.append(canonical_name)
        if cat_skills:
            categorized[category] = cat_skills

    return {
        "detected_skills": sorted(list(detected_skills_set)),
        "categorized_skills": categorized
    }
