import spacy
from utils.section_parser import split_into_sections

nlp = spacy.load("en_core_web_sm")

EXPERIENCE_KEYWORDS = [
    "intern", "internship", "developer", "engineer", "analyst", "designer",
    "project", "experience", "worked", "developed", "designed",
    "implemented", "built", "managed", "tested", "maintained",
    "created", "responsible for", "software", "web application",
    "dashboard", "database", "api", "team", "deployment", "testing",
    "support", "research", "analysis", "programming", "coding"
]


def extract_experience(text):
    sections = split_into_sections(text)
    experience_text = sections.get("experience", text).lower()

    doc = nlp(experience_text)
    found_experience = set()

    for item in EXPERIENCE_KEYWORDS:
        if item in experience_text:
            found_experience.add(item)

    # verb-style indicators from spaCy tokens
    useful_verbs = {
        "develop", "design", "implement", "build", "manage",
        "test", "maintain", "create", "analyze", "support"
    }

    for token in doc:
        if token.pos_ == "VERB" and token.lemma_.lower() in useful_verbs:
            found_experience.add(token.lemma_.lower())

    return sorted(list(found_experience))