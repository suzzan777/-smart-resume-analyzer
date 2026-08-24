import re
import spacy
from utils.section_parser import split_into_sections

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python", "java", "c", "c++", "sql", "html", "css", "javascript",
    "flask", "django", "react", "node.js", "machine learning",
    "data analysis", "tensorflow", "pandas", "numpy", "git",
    "bootstrap", "sqlite", "mysql", "postgresql", "mongodb", "api",
    "ui/ux", "figma", "photoshop", "illustrator", "web design",
    "frontend", "backend", "power bi", "tableau", "excel",
    "data visualization", "php", "laravel", "aws", "docker", "linux",
    "rest api", "spring boot", "kotlin", "swift", "firebase"
]


def skill_in_text(skill, text):
    """
    Safer matching:
    - single-letter skills like 'c' must match as a full token
    - c++ is handled separately
    - multi-word skills use word-boundary regex
    """
    escaped_skill = re.escape(skill.lower())

    if skill.lower() == "c":
        return re.search(r"\bc\b", text) is not None

    if skill.lower() == "c++":
        return re.search(r"(?<!\w)c\+\+(?!\w)", text) is not None

    if " " in skill or "+" in skill or "." in skill or "/" in skill:
        pattern = r"(?<!\w)" + escaped_skill + r"(?!\w)"
        return re.search(pattern, text) is not None

    pattern = r"\b" + escaped_skill + r"\b"
    return re.search(pattern, text) is not None


def extract_skills(text):
    sections = split_into_sections(text)
    combined_text = " ".join([
        sections.get("skills", ""),
        sections.get("experience", ""),
        text
    ]).lower()

    doc = nlp(combined_text)
    token_text = " ".join([token.text.lower() for token in doc])

    found_skills = set()

    for skill in SKILL_KEYWORDS:
        if skill_in_text(skill, combined_text) or skill_in_text(skill, token_text):
            found_skills.add(skill)

    return sorted(list(found_skills))


def compare_skills(resume_skills, job_skills):
    matched_skills = sorted(list(set(resume_skills) & set(job_skills)))
    missing_skills = sorted(list(set(job_skills) - set(resume_skills)))
    return matched_skills, missing_skills