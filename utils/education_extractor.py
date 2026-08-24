from utils.section_parser import split_into_sections

EDUCATION_KEYWORDS = [
    "bsc", "msc", "phd", "bachelor", "master", "degree",
    "computer science", "computing", "software engineering",
    "information technology", "data science", "artificial intelligence",
    "business information systems", "cyber security", "diploma",
    "certificate", "hnd", "higher national diploma"
]


def extract_education(text):
    sections = split_into_sections(text)
    education_text = sections.get("education", text).lower()

    found_education = []
    for item in EDUCATION_KEYWORDS:
        if item in education_text:
            found_education.append(item)

    return sorted(list(set(found_education)))