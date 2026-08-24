import spacy
from utils.section_parser import split_into_sections

nlp = spacy.load("en_core_web_sm")


def extract_organisations(text):
    sections = split_into_sections(text)
    experience_text = sections.get("experience", text)

    doc = nlp(experience_text)
    organisations = set()

    for ent in doc.ents:
        if ent.label_ == "ORG":
            organisations.add(ent.text.strip())

    return sorted(list(organisations))