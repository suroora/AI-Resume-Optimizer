from core.matching_engine import ResumeMatcher
from core.skill_gap import skill_match_analysis

resume_text = """
Python developer with experience in SQL, machine learning,
data analysis and API development.
"""

job_description = """
Looking for Python developer skilled in SQL,
machine learning, deep learning and cloud deployment.
"""

skill_list = [
    "Python",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Cloud",
    "Data Analysis"
]

# Semantic similarity
matcher = ResumeMatcher()
similarity_score = matcher.compute_similarity(resume_text, job_description)

# Skill analysis
matched, missing, skill_percent = skill_match_analysis(
    resume_text,
    job_description,
    skill_list
)

print("Job Fit Score:", similarity_score)
print("Skill Match %:", skill_percent)
print("Matched Skills:", matched)
print("Missing Skills:", missing)