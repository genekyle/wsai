import json
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import numpy as np
import torch

class HeaderClassifier:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-MiniLM-L6-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/paraphrase-MiniLM-L6-v2')
        self.classifier = SVC(kernel='linear')
        self.label_encoder = LabelEncoder()

    def encode(self, texts):
        """Encodes text inputs into embeddings using the model."""
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**encoded_input)
        # Squeeze the tensor to ensure 2D output for multiple texts
        embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
        return embeddings

    def train(self, data):
        """Trains the classifier using provided header data."""
        headers = [item['header'] for category in data.values() for item in category]
        categories = [item['category'] for category in data.values() for item in category]
        
        # Encode text data into embeddings
        embeddings = self.encode(headers)
        
        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(categories)
        
        # Train the classifier
        self.classifier.fit(embeddings, encoded_labels)

    def predict(self, header_text):
        """Predicts the category of a given header text."""
        header_embedding = self.encode([header_text])
        # Ensure input to predict is 2D
        prediction = self.classifier.predict(header_embedding)
        category = self.label_encoder.inverse_transform(prediction)
        return category[0]