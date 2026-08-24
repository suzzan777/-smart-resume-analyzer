def generate_job_seeker_feedback(overall_score, missing_skills, resume_education, resume_experience):
    feedback = []

    if overall_score < 30:
        feedback.append("The resume currently has a weak match with the target job. It should be improved with more role-specific content.")
    elif overall_score < 60:
        feedback.append("The resume has a moderate match with the job description, but there is room for improvement.")
    else:
        feedback.append("The resume shows a strong match with the target job description.")

    if missing_skills:
        feedback.append(
            "Add or highlight these missing skills more clearly: " + ", ".join(missing_skills)
        )

    if not resume_education:
        feedback.append(
            "Education or qualification details are not clearly visible. Add degree title, subject area, and institution more clearly."
        )

    if not resume_experience:
        feedback.append(
            "The resume does not strongly show experience indicators. Include project work, internships, or technical responsibilities."
        )

    feedback.append(
        "Use stronger action words and make sure important technical skills are visible in both the skills and experience sections."
    )

    return feedback


def generate_employer_summary(overall_score, matched_skills, missing_skills, resume_experience):
    if overall_score >= 70:
        fit_level = "Strong Fit"
    elif overall_score >= 40:
        fit_level = "Moderate Fit"
    else:
        fit_level = "Weak Fit"

    if len(resume_experience) >= 5:
        experience_strength = "Good evidence of experience indicators"
    elif len(resume_experience) >= 2:
        experience_strength = "Some evidence of experience indicators"
    else:
        experience_strength = "Limited evidence of experience indicators"

    return {
        "fit_level": fit_level,
        "matched_count": len(matched_skills),
        "missing_count": len(missing_skills),
        "experience_strength": experience_strength
    }