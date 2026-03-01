from core.matching_engine import ResumeMatcher
from core.skill_gap import skill_match_analysis
from core.scoring import calculate_final_score, generate_recommendation

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

# Final score
final_score = calculate_final_score(similarity_score, skill_percent)
recommendation = generate_recommendation(final_score)

print("Job Fit Score:", similarity_score)
print("Skill Match %:", skill_percent)
print("Matched Skills:", matched)
print("Missing Skills:", missing)
print("Final Score:", final_score)
print("Recommendation:", recommendation)