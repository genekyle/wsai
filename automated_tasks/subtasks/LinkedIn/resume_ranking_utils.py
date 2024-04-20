# resume_ranking_utils.py
import torch
from transformers import BertModel, BertTokenizer
from scipy.spatial.distance import cosine

def rank_and_get_best_resume(job_title, resume_titles):
    print("Inside new resume ranking utils file")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    encoded_job_title = tokenizer.encode(job_title, add_special_tokens=True)
    encoded_resume_titles = [tokenizer.encode(title, add_special_tokens=True) for title in resume_titles]

    job_title_tensor = torch.tensor([encoded_job_title])
    resume_title_tensors = [torch.tensor([title]) for title in encoded_resume_titles]

    with torch.no_grad():
        job_title_embedding = model(job_title_tensor)[0][:,0,:].squeeze().numpy()
        resume_title_embeddings = [model(tensor)[0][:,0,:].squeeze().numpy() for tensor in resume_title_tensors]

    similarities = [1 - cosine(job_title_embedding, embedding) for embedding in resume_title_embeddings]
    ranked_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)

    best_match_index = ranked_indices[0]
    best_match_resume_title = resume_titles[best_match_index]
    best_match_score = similarities[best_match_index]

    return best_match_resume_title, best_match_score