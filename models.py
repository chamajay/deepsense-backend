from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import os
import sys


def load_model(model_path):
    # Load model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)
    # Return classifier
    return classifier


def load_emotion_distilroberta():
    model_path = "models/emotion-english-distilroberta-base"
    if model_exists(model_path):
        return load_model(model_path)
    else:
        print("Error: Model file not found at", model_path)
        sys.exit()


def load_suicidal_text_electra():
    model_path = "models/suicidal-text-electra-cj"
    if model_exists(model_path):
        return load_model(model_path)
    else:
        print("Error: Model file not found at", model_path)
        sys.exit()


def model_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False
