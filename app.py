from flask import Flask, render_template, request, redirect, url_for, make_response
import os
import csv
import io

from utils.parser import extract_text_from_file
from utils.matcher import calculate_similarity, calculate_feature_score
from utils.extractor import extract_skills, compare_skills
from utils.education_extractor import extract_education
from utils.experience_extractor import extract_experience
from utils.organisation_extractor import extract_organisations
from utils.feedback import generate_job_seeker_feedback, generate_employer_summary
from utils.database import (
    init_db,
    save_analysis_result,
    get_all_results,
    get_result_count,
    delete_result
)
from utils.evaluator import load_evaluation_pairs, compute_classification_metrics, qualitative_summary

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


@app.route("/")
def index():
    total_analyses = get_result_count()
    return render_template("index.html", total_analyses=total_analyses)


@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("resume")
    job_title = request.form.get("job_title", "").strip()
    job_source = request.form.get("job_source", "").strip()
    job_source_url = request.form.get("job_source_url", "").strip()
    job_description = request.form.get("job_description", "").strip()
    view_mode = request.form.get("view_mode", "job_seeker")

    if not files or files[0].filename == "":
        return "No resume file uploaded."

    if not job_title:
        return "Job title is required."

    if not job_source:
        return "Job source is required."

    if not job_description:
        return "Job description is required."

    all_results = []

    for file in files:
        if not file.filename:
            continue

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        extracted_text = extract_text_from_file(file_path)
        if not extracted_text.strip():
            continue

        resume_skills = extract_skills(extracted_text)
        job_skills = extract_skills(job_description)
        matched_skills, missing_skills = compare_skills(resume_skills, job_skills)

        resume_education = extract_education(extracted_text)
        job_education = extract_education(job_description)

        resume_experience = extract_experience(extracted_text)
        job_experience = extract_experience(job_description)

        resume_organisations = extract_organisations(extracted_text)

        similarity_score = calculate_similarity(extracted_text, job_description)
        feature_score = calculate_feature_score(
            resume_skills=resume_skills,
            job_skills=job_skills,
            resume_education=resume_education,
            job_education=job_education,
            resume_experience=resume_experience,
            job_experience=job_experience
        )

        overall_score = round((similarity_score * 0.6) + (feature_score * 0.4), 2)

        job_seeker_feedback = generate_job_seeker_feedback(
            overall_score=overall_score,
            missing_skills=missing_skills,
            resume_education=resume_education,
            resume_experience=resume_experience
        )

        employer_summary = generate_employer_summary(
            overall_score=overall_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            resume_experience=resume_experience
        )

        result = {
            "filename": file.filename,
            "job_title": job_title,
            "job_source": job_source,
            "job_source_url": job_source_url,
            "extracted_text": extracted_text,
            "job_description": job_description,
            "similarity_score": similarity_score,
            "feature_score": feature_score,
            "overall_score": overall_score,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "resume_education": resume_education,
            "job_education": job_education,
            "resume_experience": resume_experience,
            "job_experience": job_experience,
            "resume_organisations": resume_organisations,
            "job_seeker_feedback": job_seeker_feedback,
            "employer_summary": employer_summary,
            "view_mode": view_mode
        }

        save_analysis_result(result)
        all_results.append(result)

    if not all_results:
        return "Could not process any uploaded resumes."

    if len(all_results) == 1:
        return render_template("results.html", result=all_results[0])

    all_results = sorted(all_results, key=lambda x: x["overall_score"], reverse=True)
    return render_template(
        "ranking.html",
        results=all_results,
        job_description=job_description,
        job_title=job_title,
        job_source=job_source,
        job_source_url=job_source_url
    )


@app.route("/history")
def history():
    results = get_all_results()

    score_labels = [row["filename"] for row in results[:10]]
    score_values = [row["overall_score"] for row in results[:10]]

    fit_counts = {"Strong Fit": 0, "Moderate Fit": 0, "Weak Fit": 0}
    for row in results:
        fit_level = row["fit_level"]
        if fit_level in fit_counts:
            fit_counts[fit_level] += 1

    return render_template(
        "history.html",
        results=results,
        score_labels=score_labels,
        score_values=score_values,
        fit_counts=fit_counts
    )


@app.route("/delete_result/<int:result_id>", methods=["POST"])
def delete_history_result(result_id):
    delete_result(result_id)
    return redirect(url_for("history"))


@app.route("/export_csv")
def export_csv():
    results = get_all_results()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID", "Filename", "Overall Score", "Similarity Score", "Feature Score",
        "Fit Level", "Matched Skills", "Missing Skills", "Education", "Experience", "Created At"
    ])

    for row in results:
        writer.writerow([
            row["id"],
            row["filename"],
            row["overall_score"],
            row["similarity_score"],
            row["feature_score"],
            row["fit_level"],
            row["matched_skills"],
            row["missing_skills"],
            row["resume_education"],
            row["resume_experience"],
            row["created_at"]
        ])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=analysis_history.csv"
    response.headers["Content-type"] = "text/csv"
    return response


@app.route("/evaluation")
def evaluation():
    pairs = load_evaluation_pairs()
    metrics = compute_classification_metrics(pairs)
    comments = qualitative_summary(metrics)

    metric_labels = ["Precision", "Recall", "F1 Score", "Accuracy"]
    metric_values = [
        metrics["precision"],
        metrics["recall"],
        metrics["f1_score"],
        metrics["accuracy"]
    ]

    confusion_labels = ["TP", "FP", "FN", "TN"]
    confusion_values = [
        metrics["true_positive"],
        metrics["false_positive"],
        metrics["false_negative"],
        metrics["true_negative"]
    ]

    return render_template(
        "evaluation.html",
        metrics=metrics,
        comments=comments,
        metric_labels=metric_labels,
        metric_values=metric_values,
        confusion_labels=confusion_labels,
        confusion_values=confusion_values
    )


if __name__ == "__main__":
    app.run(debug=True)