from nltk import pos_tag
import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def read_data():
	df = pd.read_csv("data/reviews.csv")
	print(df.describe().to_string())
	return df


def clean_data(df):
	stop = stopwords.words("english")
	review_sentiment_scores = []
	for _, row in df[["review_id", "review_text"]].iterrows():
		review_score = {"review_id": row.review_id, "compound": 0, "neg": 0, "neu": 0, "pos": 0, "count_verbs": 0, "count_nouns": 0}

		for sentence in tokenize.sent_tokenize(row.review_text):
			words = [word for word in tokenize.word_tokenize(sentence) if word not in stop]
			sentence = ' '.join(words)
			ss = SentimentIntensityAnalyzer().polarity_scores(sentence)
			for k in sorted(ss):
				review_score[k] += ss[k]

			for word, tag in pos_tag(words):
				if tag in ['VERB', 'VB', 'VBN', 'VBD', 'VBZ', 'VBG', 'VBP']:
					review_score["count_verbs"] += 1
				elif tag in ['NOUN', 'NNP', 'NN', 'NUM', 'NNS', 'NP', 'NNPS']:
					review_score["count_nouns"] += 1

		print(review_score)
		review_sentiment_scores.append(review_score)
	sentiment_df = pd.DataFrame(review_sentiment_scores)
	print(sentiment_df.describe().to_string())
	return sentiment_df


def print_top3_offenders(df, top3_offender_ids):
	print(df[df["review_id"].isin(top3_offender_ids)].to_string())


def post_process(sentiment_df):
	sentiment_df["pos/neu"] = sentiment_df.apply(lambda r: r.pos / r.neu, axis=1)
	sentiment_df["verb/noun"] = sentiment_df.apply(lambda r: r.count_verbs / r.count_nouns, axis=1)

	print(sentiment_df["pos/neu"].mean() + sentiment_df["pos/neu"].std()*3)
	too_postive_df = sentiment_df[(sentiment_df.pos > (sentiment_df["pos/neu"].mean() + sentiment_df["pos/neu"].std()*3))]
	return too_postive_df


def get_top3_offenders(too_postive_df):
	print(too_postive_df.describe().to_string())
	print(too_postive_df.sort_values("pos/neu", ascending=False).to_string())
	return too_postive_df.sort_values("pos/neu", ascending=False).head(3).review_id.values


def analyze_reviews():
	df = read_data()
	sentiment_df = clean_data(df)
	sentiment_df = post_process(sentiment_df)
	top3_offenders = get_top3_offenders(sentiment_df)
	print_top3_offenders(df, top3_offenders)


if __name__ == '__main__':
	analyze_reviews()

