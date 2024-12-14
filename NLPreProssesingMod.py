import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
import joblib

nltk.download('stopwords')
nltk.download('punkt')

spell = SpellChecker()

# Text pre processing for misspelling, stopwords, and out of bound characters
def preprocess_text(text):
    text = ''.join([char for char in text if char.isalnum() or char.isspace()])
    
    text = text.lower()
    
    tokens = word_tokenize(text)
    
    corrected_tokens = [spell.correction(token) for token in tokens]
    
    filtered_tokens = [word for word in corrected_tokens if word not in stopwords.words('english')]
    
    return ' '.join(filtered_tokens)

# Data for training the model -> Update this every year for new data detection
data = [
    
]

# split of data into game names and topics
game_names, topics = zip(*data)

# Preprocess game names
preprocessed_game_names = [preprocess_text(name) for name in game_names]

# Encode topics
label_encoder = LabelEncoder()
encoded_topics = label_encoder.fit_transform(topics)

# Text data -> numerical features
vectorizer = TfidfVectorizer(stop_words=nltk.corpus.stopwords.words('english'))
X = vectorizer.fit_transform(preprocessed_game_names)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, encoded_topics, test_size=0.2, random_state=42)

# Pipeline
model = make_pipeline(vectorizer, LogisticRegression())

# Model training
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'game_topic_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model trained and saved!")