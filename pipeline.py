from preprocessing.resume_parser import parse_resume
from preprocessing.text_cleaning import clean_text

from core.matching_engine import ResumeMatcher
from core.skill_gap import skill_match_analysis
from core.scoring import calculate_final_score, generate_recommendation


# ===== INPUT =====
resume_file = "sample_resume.pdf"

job_description = """
Looking for a Data Analyst skilled in Python, SQL,
Machine Learning, Data Visualization, Power BI and Tableau.
"""


# Skill dictionary
skill_list = [
    "Python",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "Data Visualization",
    "Power BI",
    "Tableau",
    "Excel",
    "Pandas",
    "NumPy"
]


# ===== PIPELINE START =====

# 1. Parse resume
raw_text = parse_resume(resume_file)

# 2. Clean text
resume_text = clean_text(raw_text)
jd_text = clean_text(job_description)

# 3. Semantic similarity
matcher = ResumeMatcher()
similarity_score = matcher.compute_similarity(resume_text, jd_text)

# 4. Skill analysis
matched, missing, skill_percent = skill_match_analysis(
    resume_text,
    jd_text,
    skill_list
)

# 5. Final scoring
final_score = calculate_final_score(similarity_score, skill_percent)
recommendation = generate_recommendation(final_score)


# ===== OUTPUT =====
print("\n===== AI RESUME ANALYSIS =====")
print("Job Fit Score:", similarity_score)
print("Skill Match %:", skill_percent)
print("Matched Skills:", matched)
print("Missing Skills:", missing)
print("Final Score:", final_score)
print("Recommendation:", recommendation)