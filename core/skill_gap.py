def extract_skills(text: str, skill_list: list):
    """
    Extract skills from text using keyword matching.
    """

    found_skills = []
    text_lower = text.lower()

    for skill in skill_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


def skill_match_analysis(resume_text: str, job_description: str, skill_list: list):
    """
    Compare resume skills with job description skills.
    Returns:
    - matched skills
    - missing skills
    - match percentage
    """

    resume_skills = extract_skills(resume_text, skill_list)
    jd_skills = extract_skills(job_description, skill_list)

    if not jd_skills:
        return [], [], 0.0

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    match_percent = (len(matched) / len(jd_skills)) * 100

    return matched, missing, round(match_percent, 2)
