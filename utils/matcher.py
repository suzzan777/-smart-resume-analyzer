from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity_score * 100, 2)


def calculate_feature_score(
    resume_skills,
    job_skills,
    resume_education,
    job_education,
    resume_experience,
    job_experience
):
    """
    Stricter scoring:
    - only score a category if the job description actually contains that category
    - do NOT give automatic 100 when the job has no extracted requirements
    - if nothing meaningful is extracted from the job description, feature score = 0
    """

    category_scores = []
    category_weights = []

    # Skills
    if job_skills:
        matched_skill_count = len(set(resume_skills) & set(job_skills))
        skill_score = (matched_skill_count / len(job_skills)) * 100
        category_scores.append(skill_score)
        category_weights.append(0.5)

    # Education
    if job_education:
        matched_education_count = len(set(resume_education) & set(job_education))
        education_score = (matched_education_count / len(job_education)) * 100
        category_scores.append(education_score)
        category_weights.append(0.2)

    # Experience
    if job_experience:
        matched_experience_count = len(set(resume_experience) & set(job_experience))
        experience_score = (matched_experience_count / len(job_experience)) * 100
        category_scores.append(experience_score)
        category_weights.append(0.3)

    # If the system cannot extract any meaningful requirement from the job description,
    # feature score should be 0 instead of giving free marks.
    if not category_scores:
        return 0.0

    weighted_total = sum(score * weight for score, weight in zip(category_scores, category_weights))
    total_weight = sum(category_weights)

    final_feature_score = weighted_total / total_weight
    return round(final_feature_score, 2)