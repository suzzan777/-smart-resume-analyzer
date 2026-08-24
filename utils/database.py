import sqlite3

DB_NAME = "resume_data.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            job_title TEXT,
            job_source TEXT,
            job_source_url TEXT,
            raw_text TEXT,
            job_description TEXT NOT NULL,
            similarity_score REAL NOT NULL,
            feature_score REAL NOT NULL,
            overall_score REAL NOT NULL,
            resume_skills TEXT,
            job_skills TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            resume_education TEXT,
            job_education TEXT,
            resume_experience TEXT,
            job_experience TEXT,
            resume_organisations TEXT,
            fit_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_analysis_result(result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analysis_results (
            filename, job_title, job_source, job_source_url, raw_text,
            job_description, similarity_score, feature_score, overall_score,
            resume_skills, job_skills, matched_skills, missing_skills,
            resume_education, job_education, resume_experience,
            job_experience, resume_organisations, fit_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result["filename"],
        result.get("job_title", ""),
        result.get("job_source", ""),
        result.get("job_source_url", ""),
        result.get("extracted_text", ""),
        result["job_description"],
        result["similarity_score"],
        result["feature_score"],
        result["overall_score"],
        ", ".join(result["resume_skills"]),
        ", ".join(result["job_skills"]),
        ", ".join(result["matched_skills"]),
        ", ".join(result["missing_skills"]),
        ", ".join(result["resume_education"]),
        ", ".join(result["job_education"]),
        ", ".join(result["resume_experience"]),
        ", ".join(result["job_experience"]),
        ", ".join(result["resume_organisations"]),
        result["employer_summary"]["fit_level"]
    ))

    conn.commit()
    conn.close()


def get_all_results():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM analysis_results
        ORDER BY created_at DESC, id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_result_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM analysis_results")
    total = cursor.fetchone()["total"]
    conn.close()
    return total


def delete_result(result_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_results WHERE id = ?", (result_id,))
    conn.commit()
    conn.close()