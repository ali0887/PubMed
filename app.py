from flask import Flask, render_template, request, jsonify
from transformers import T5ForConditionalGeneration, AutoTokenizer
import re
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)

# Load the fine-tuned model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('./fine_tuned_model_final')
tokenizer = AutoTokenizer.from_pretrained('./fine_tuned_model_final')

def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'\{.*?\}', '', text)  # Remove text in curly braces
    text = re.sub(r'\[.*?\]', '', text)  # Remove text in square brackets
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'\([^()]*\bfigure\b[^()]*\)', '', text)
    return text.strip()

# Initialize stopwords, lemmatizer, and counter
stop_words = set(stopwords.words('english'))
stop_words_dict = Counter(stop_words)
lemmatizer = WordNetLemmatizer()

# Function to remove stopwords and perform lemmatization
def remove_stopwords_and_lemmatize(text):
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words_dict]
    return ' '.join(lemmatized_words)

def postprocess_summary(summary, max_length):
    # Truncate to the nearest sentence end
    sentences = re.split(r'(?<=[.!?]) +', summary)
    result = ""
    for sentence in sentences:
        if len(result) + len(sentence) > max_length:
            break
        result += sentence + " "
    return result.strip()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.form['input_text']

    if len(data) < 100:
        return jsonify({'summary': ''})
    
    mode = int(request.form['mode'])

    data = clean_text(data)
    data = remove_stopwords_and_lemmatize(data)

    inputs = tokenizer.encode("summarize: " + data, return_tensors='pt', max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=mode, min_length=30, length_penalty=2.0, num_beams=2, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    postprocess_summary(summary, mode)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run() 
