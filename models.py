from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

def load_model(model_path):
    # Load model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)
    # Return classifier
    return classifier

def load_emotion_distilroberta():
    model_path = "models/emotion-english-distilroberta-base"
    return load_model(model_path)

def load_suicidal_text_electra():
    model_path = "models/suicidal-text-electra-cj"
    return load_model(model_path)
