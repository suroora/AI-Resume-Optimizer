from core.matching_engine import ResumeMatcher

resume_text = """
Python developer with experience in SQL, machine learning,
data analysis and API development.
"""

job_description = """
Looking for Python developer skilled in SQL,
machine learning and backend development.
"""

matcher = ResumeMatcher()

score = matcher.compute_similarity(resume_text, job_description)

print("Job Fit Score:", score)