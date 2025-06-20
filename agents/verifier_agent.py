from sentence_transformers import SentenceTransformer, util

class VerifierAgent:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def verify_summary(self, summary_data: dict, original_paper: dict) -> bool:
        original_text = original_paper["content"][:1000]
        summary_text = summary_data.get("summary", "")
        emb1 = self.model.encode(original_text, convert_to_tensor=True)
        emb2 = self.model.encode(summary_text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(emb1, emb2).item()
        return score > 0.6