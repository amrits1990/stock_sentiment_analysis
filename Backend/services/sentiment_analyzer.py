# Sentiment analysis using DistilRoBERTa-financial
from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(texts):
    if not texts:
        return 0.5  # Neutral score if no text
    scores = []
    for text in texts:
        result = sentiment_model(text[:512])[0]  # Truncate long text
        label = result['label']
        score = result['score']
        if label == 'positive':
            scores.append(score)
        elif label == 'negative':
            scores.append(1 - score)
        else:
            scores.append(0.5)
    return sum(scores) / len(scores)

def aggregate_sentiment(list_of_text_lists):
    combined_texts = []
    for texts in list_of_text_lists:
        combined_texts.extend(texts)
    return round(analyze_sentiment(combined_texts) * 100, 2)  # Return percentage