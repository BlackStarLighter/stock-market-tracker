import unittest
from ai_model.sentiment_analysis import SentimentAnalysis

class TestSentimentAnalysis(unittest.TestCase):
    def setUp(self):
        self.model = SentimentAnalysis()
        self.texts = [
            "I love this product!", "This is the worst thing I ever bought.",
            "Amazing experience, highly recommended!", "Not worth the money.",
            "This is fantastic!", "I hate it.", "Such a great buy!", "Absolutely terrible.",
            "Super happy with this purchase!", "I regret buying this.",
            "Incredible quality, very satisfied.", "Disappointed beyond words.",
            "A wonderful experience!", "I will never buy this again.",
            "Highly recommend to everyone!", "Complete waste of money.",
            "This exceeded my expectations!", "Not what I expected, very bad.",
            "Perfect! Couldn’t be happier.", "Horrible service, never again.",
            "Truly outstanding product.", "One of the worst things I’ve used.",
            "It works like a charm!", "Totally useless.",
            "This changed my life!", "I wish I could return this.",
            "Best investment I’ve made.", "It broke after a day.",
            "Flawless experience!", "So disappointed, don’t waste your money.",
            "An absolute joy to use.", "This was a nightmare.",
            "Everything I wanted and more.", "It stopped working immediately.",
            "Such a pleasant surprise!", "Never buying from this brand again.",
            "Worth every penny.", "Feels like a scam.",
            "A must-have item!", "This was a disaster.",
            "Top-notch quality.", "Not as advertised.",
            "Five stars all the way!", "Gave me a headache.",
            "Superb design and performance!", "I want a refund.",
            "Love it so much!", "Awful experience, wouldn’t recommend.",
            "I would buy this again in a heartbeat.", "Terrible, stay away!"
        ]
        self.labels = [
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0
        ]  # 1 = Positive, 0 = Negative

    def test_train_model(self):
        """Test training the sentiment analysis model."""
        self.model.train(self.texts, self.labels)
        self.assertTrue(hasattr(self.model, "vectorizer"))

    def test_predict_sentiment(self):
        """Test predicting sentiment from a new sentence."""
        self.model.train(self.texts, self.labels)
        prediction = self.model.predict("This is an awesome experience!")
        self.assertIn(prediction, [0, 1])  # Should return either 0 (negative) or 1 (positive)

if __name__ == '__main__':
    unittest.main()
