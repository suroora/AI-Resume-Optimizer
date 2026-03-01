from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeMatcher:
    def __init__(self):
        """
        Load lightweight SBERT model.
        Fast + deployment friendly.
        """
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Compute semantic similarity between resume and job description.
        Returns percentage score.
        """

        resume_embedding = self.model.encode([resume_text])
        jd_embedding = self.model.encode([job_description])

        similarity = cosine_similarity(
            resume_embedding,
            jd_embedding
        )[0][0]

        return round(float(similarity * 100), 2)