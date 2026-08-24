import re


SECTION_PATTERNS = {
    "skills": [
        r"\bskills\b",
        r"\btechnical skills\b",
        r"\bcore competencies\b",
        r"\btechnologies\b"
    ],
    "education": [
        r"\beducation\b",
        r"\bacademic background\b",
        r"\bqualifications\b"
    ],
    "experience": [
        r"\bexperience\b",
        r"\bwork experience\b",
        r"\bemployment history\b",
        r"\bprofessional experience\b",
        r"\bprojects\b"
    ]
}


def split_into_sections(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = {"skills": [], "education": [], "experience": [], "other": []}

    current_section = "other"

    for line in lines:
        line_lower = line.lower()

        matched_section = None
        for section_name, patterns in SECTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line_lower):
                    matched_section = section_name
                    break
            if matched_section:
                break

        if matched_section:
            current_section = matched_section
        else:
            sections[current_section].append(line)

    return {key: "\n".join(value) for key, value in sections.items()}