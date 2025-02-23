# import tensorflow as tf
import numpy as np
# from tensorflow import keras
# from keras.models import Sequential
# from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import LSTM, Dense, Embedding, Bidirectional

# Define Sentiment Analysis Model
class SentimentAnalysis:
    def __init__(self, vocab_size=10000, max_length=100):
        self.vocab_size = vocab_size
        self.max_length = max_length
        self.tokenizer = Tokenizer(num_words=self.vocab_size, oov_token="<OOV>")
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            Embedding(self.vocab_size, 128, input_length=self.max_length),
            Bidirectional(LSTM(64, return_sequences=True)),
            Bidirectional(LSTM(32)),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def train(self, texts, labels, epochs=5, batch_size=32):
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        labels = np.array(labels)
        self.model.fit(padded_sequences, labels, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    def predict(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=self.max_length, padding='post', truncating='post')
        prediction = self.model.predict(padded_sequence)
        return "Positive" if prediction[0][0] > 0.5 else "Negative"
    
if __name__ == "__main__":

    # Sample Dataset
    texts = [
        "I love this product!", 
        "This is the worst thing I ever bought", 
        "Amazing experience, highly recommended!", 
        "Not worth the money",
        "Absolutely fantastic! Will buy again.",
        "Terrible service, I want a refund.",
        "Great quality and fast shipping!",
        "Horrible experience, never shopping here again.",
        "Best decision I made, I love it!",
        "The product arrived broken, very disappointing.",
        "Customer support was extremely helpful!",
        "I regret purchasing this, complete waste of money.",
        "The colors are vibrant and beautiful.",
        "I waited too long for delivery, not satisfied.",
        "Super easy to use, very intuitive!",
        "The material feels cheap and flimsy.",
        "Highly recommended, exceeded my expectations.",
        "I can't believe I wasted money on this.",
        "Fast delivery and excellent packaging.",
        "The item doesn’t match the description at all.",
        "Fantastic performance, smooth and efficient.",
        "Way too expensive for what it offers.",
        "I’m beyond happy with this purchase!",
        "It stopped working after just one week.",
        "Everything was perfect, no complaints!",
        "Poor build quality, expected better.",
        "Worth every penny, I would buy again.",
        "Customer service was rude and unhelpful.",
        "I was skeptical at first, but it's great!",
        "Product was defective upon arrival.",
        "Lightweight, stylish, and very comfortable.",
        "Not user-friendly, very frustrating to use.",
        "I am extremely satisfied with this purchase.",
        "Misleading advertising, very disappointed.",
        "Solid build and premium feel.",
        "Had high expectations but they weren't met.",
        "This product changed my life!",
        "Simply awful, I want my money back.",
        "Surprisingly good quality for the price.",
        "Arrived late, and packaging was damaged.",
        "Super fast performance, very impressed.",
        "Looks great but does not work well.",
        "Everything functions as described.",
        "I will never buy from this brand again.",
        "The design is sleek and modern.",
        "False advertising, very misleading.",
        "Perfect fit, just what I was looking for!",
        "Worst purchase I've made in a long time.",
        "Very reliable and easy to maintain.",
        "Big disappointment, nothing like the pictures."
    ]

    # Corresponding Sentiment Labels (1 = Positive, 0 = Negative)
    labels = [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0
    ]

    sentiment_model = SentimentAnalysis()
    sentiment_model.train(texts, labels)

    # Test Prediction
    print(sentiment_model.predict("This is an awesome experience!"))
    print(sentiment_model.predict("Terrible customer support, never buying again."))

