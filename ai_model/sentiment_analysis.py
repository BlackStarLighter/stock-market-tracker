import numpy as np
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
        # Fit tokenizer
        self.tokenizer.fit_on_texts(texts)

        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        labels = np.array(labels)

        self.model.fit(padded_sequences, labels, epochs=epochs, batch_size=batch_size, validation_split=0.2)

        # Save the trained model
        self.model.save("sentiment_model.h5")

    def predict(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=self.max_length, padding='post', truncating='post')
        prediction = self.model.predict(padded_sequence)[0][0]
        return "Positive" if prediction > 0.5 else "Negative"

if __name__ == "__main__":
    # Sample Dataset
    texts = [
        "Absolutely amazing product, exceeded my expectations!",  
        "I love how easy this is to use, highly recommend!",  
        "Fantastic quality, I will definitely buy again.",  
        "Best purchase I've made in a long time!",  
        "Very satisfied, everything works perfectly!",  
        "Super fast delivery and excellent packaging!",  
        "Incredible customer service, so helpful and kind.",  
        "Feels premium and well-made, worth every penny.",  
        "Exceeded all my expectations, five stars!",  
        "I’m extremely happy with this purchase!",  
        "Beautiful design and works flawlessly.",  
        "Surprisingly good for the price, highly recommended.",  
        "I love the attention to detail in this product!",  
        "Perfect fit and exactly what I was looking for!",  
        "Smooth performance, no issues at all.",  
        "User-friendly and very intuitive, even for beginners.",  
        "Great value for money, will purchase again.",  
        "The colors are vibrant and absolutely stunning!",  
        "Works better than I expected, super happy!",  
        "Looks and feels high-quality, no regrets!",  
        "Very comfortable and stylish, love it!",  
        "Received so many compliments on this product!",  
        "Definitely a must-have, I can’t recommend it enough!",  
        "Reliable and well-built, it’s going to last a long time.",  
        "Exceeded my expectations, truly a fantastic product.",  
        "Terrible quality, broke after just one use.",  
        "Worst purchase I’ve ever made, completely useless!",  
        "Very disappointing, nothing like the pictures.",  
        "Arrived damaged, what a waste of money!",  
        "Customer service was unhelpful and rude.",  
        "The product stopped working after a week.",  
        "Way too expensive for what it offers.",  
        "Does not work as advertised, very misleading.",  
        "Cheap material, feels flimsy and poorly made.",  
        "Horrible experience, will never buy again!",  
        "Shipping took forever, and it arrived broken.",  
        "Not worth the money at all, huge disappointment.",  
        "Completely useless, I want a refund!",  
        "False advertising, this is nothing like what I ordered!",  
        "It’s so frustrating to use, definitely not user-friendly.",  
        "Looks nice but doesn’t work properly.",  
        "Expected much better quality for the price.",  
        "I regret buying this, what a waste!",  
        "Stopped working within a few days, terrible quality.",  
        "The instructions were unclear and confusing.",  
        "Customer support ignored my emails, very frustrating.",  
        "It’s uncomfortable to use and feels awkward.",  
        "Completely unreliable, I wouldn’t trust it at all.",  
        "Misleading description, does not meet expectations.",  
        "Very cheap build quality, broke almost immediately."
    ]

    labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    sentiment_model = SentimentAnalysis()
    sentiment_model.train(texts, labels)

    # Test Prediction
    print(sentiment_model.predict("This is an awesome experience!"))  # Expected: Positive
    print(sentiment_model.predict("Terrible customer support, never buying again."))  # Expected: Negative
