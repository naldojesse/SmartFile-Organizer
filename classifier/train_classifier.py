import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample data for training the classifier
training_data = [
    ("work project report", "documents.work"),
    ("family vacation photo", "images.photos"),
    ("finance statement 2023", "documents.finance"),
    ("movie night", "videos.movies"),
    ("screenshot of error", "images.screenshots")
]

# Train a simple classifier
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform([text for text, label in training_data])
y_train = [label for text, label in training_data]
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

# Save the model and vectorizer
joblib.dump(vectorizer, "classifier/vectorizer.pkl")
joblib.dump(classifier, "classifier/classifier.pkl")
