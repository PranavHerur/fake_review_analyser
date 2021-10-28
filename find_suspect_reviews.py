import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

df = pd.read_csv("data/reviews.csv")
print(df.describe().to_string())
df = df[["review_id", "review_text"]]
print(df.review_text.values)

review_sentiment_scores = []
for _, row in df.iterrows():
	review_score = {"review_id": row.review_id, "compound": 0, "neg": 0, "neu": 0, "pos": 0}

	for sentence in tokenize.sent_tokenize(row.review_text):
		ss = SentimentIntensityAnalyzer().polarity_scores(sentence)
		for k in sorted(ss):
			review_score[k] += ss[k]
	print(review_score)
	review_sentiment_scores.append(review_score)
sentiment_df = pd.DataFrame(review_sentiment_scores)
print(sentiment_df.describe().to_string())

too_postive_df = sentiment_df[(sentiment_df.pos > sentiment_df.pos.quantile(.75)) & (sentiment_df.neg < sentiment_df.neg.quantile(.75))]
too_postive_df["pos/neu"] = too_postive_df.apply(lambda r: r.pos/r.neu, axis=1)
print(too_postive_df.describe().to_string())
print(too_postive_df.sort_values("pos/neu", ascending=False).to_string())
