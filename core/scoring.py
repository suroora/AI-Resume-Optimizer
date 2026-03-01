def calculate_final_score(similarity_score: float, skill_match_percent: float):
    """
    Weighted scoring system.
    You can adjust weights later.
    """

    final_score = (0.6 * similarity_score) + (0.4 * skill_match_percent)

    return round(final_score, 2)


def generate_recommendation(score: float):
    """
    Convert score into recommendation.
    """

    if score >= 80:
        return "Ready to Apply"
    elif score >= 60:
        return "Moderate Fit – Improve Resume"
    else:
        return "Low Match – Significant Improvement Needed"
