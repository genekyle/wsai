'''ORIGNAL CODE:
# Load the model and tokenizer
model_name = 'sentence-transformers/paraphrase-MiniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def encode(text):
    """Generate embeddings for input text."""
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Assuming we're using only the [CLS] token embedding which should be at position [0, 0, :]
    return model_output.last_hidden_state[:, 0, :].squeeze().numpy()  # Ensure it's 1-D


def match_answer_to_labels(answer, labels):
    """Find the best matching label for the given answer."""
    answer_embedding = encode(answer)
    label_embeddings = [(label.text, encode(label.text), label) for label in labels]

    best_label = None
    highest_similarity = -1
    for text, embedding, label_elem in label_embeddings:
        similarity = cosine_similarity([answer_embedding], [embedding])  # Ensuring both are 1-D
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_label = (text, label_elem)

    return best_label'''

from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

class ModelHandler:
    def __init__(self):
        self.model_name = 'sentence-transformers/paraphrase-MiniLM-L6-v2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def encode(self, text):
        """Generate embeddings for input text."""
        encoded_input = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        return model_output.last_hidden_state[:, 0, :].squeeze().numpy()  # Ensure it's 1-D

    def match_answer_to_labels(self, answer, labels):
        """Find the best matching label for the given answer."""
        answer_embedding = self.encode(answer)
        label_embeddings = [(label.text, self.encode(label.text), label) for label in labels]

        best_label = None
        highest_similarity = -1
        for text, embedding, label_elem in label_embeddings:
            similarity = cosine_similarity([answer_embedding], [embedding])[0][0]
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_label = (text, label_elem)

        return best_label
