import json


def load_skill_dictionary(file_path="data/skill_dictionary.json"):
    """
    Load skills from JSON file.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    return data["skills"]


def extract_skills_from_text(text: str, skill_list: list):
    """
    Extract skills present in text.
    """
    text_lower = text.lower()

    found_skills = []

    for skill in skill_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))
