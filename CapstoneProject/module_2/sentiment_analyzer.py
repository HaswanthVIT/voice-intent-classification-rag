# module2/sentiment_analyzer.py

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    VADER_ANALYZER = SentimentIntensityAnalyzer()

    def get_sentiment(text: str) -> str:
        """
        Returns: 'positive' | 'neutral' | 'negative'
        """
        scores = VADER_ANALYZER.polarity_scores(text)
        compound = scores["compound"]

        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"

except ImportError:
    from textblob import TextBlob

    def get_sentiment(text: str) -> str:
        """
        Returns: 'positive' | 'neutral' | 'negative'
        """
        polarity = TextBlob(text).sentiment.polarity

        if polarity > 0.05:
            return "positive"
        elif polarity < -0.05:
            return "negative"
        else:
            return "neutral"