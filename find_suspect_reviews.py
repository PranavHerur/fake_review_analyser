from nltk import pos_tag
import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def read_data():
	df = pd.read_csv("data/reviews.csv")
	return df


def clean_data(df):
	print("cleaning text data")
	stop = stopwords.words("english")
	review_sentiment_scores = []
	for _, row in df[["review_id", "review_text"]].iterrows():
		review_score = {"review_id": row.review_id, "compound": 0, "neg": 0, "neu": 0, "pos": 0, "count_verbs": 0, "count_nouns": 0}

		for sentence in tokenize.sent_tokenize(row.review_text):
			# remove stop words
			words = [word for word in tokenize.word_tokenize(sentence) if word not in stop]
			sentence = ' '.join(words)

			# get sentiment score
			ss = SentimentIntensityAnalyzer().polarity_scores(sentence)
			for k in sorted(ss):
				review_score[k] += ss[k]

			# pos tags
			for word, tag in pos_tag(words):
				if tag in ['VERB', 'VB', 'VBN', 'VBD', 'VBZ', 'VBG', 'VBP']:
					review_score["count_verbs"] += 1
				elif tag in ['NOUN', 'NNP', 'NN', 'NUM', 'NNS', 'NP', 'NNPS']:
					review_score["count_nouns"] += 1

		review_sentiment_scores.append(review_score)
	sentiment_df = pd.DataFrame(review_sentiment_scores)
	return sentiment_df


def post_process(sentiment_df):
	print("calculating ratios")
	# calculate ratios of positive:negative words
	sentiment_df["pos/neu"] = sentiment_df.apply(lambda r: r.pos / r.neu, axis=1)

	# calculate ratio of verbs:nouns
	sentiment_df["verb/noun"] = sentiment_df.apply(lambda r: r.count_verbs / r.count_nouns, axis=1)
	return sentiment_df


def get_top3_offenders(too_postive_df, search_var="pos/neu"):
	# find top3 offenders
	print("finding top 3 most suspicious reviews")
	too_postive_df = too_postive_df[(too_postive_df[search_var] > (too_postive_df[search_var].mean() + too_postive_df[search_var].std() * 1))]
	return too_postive_df.sort_values(search_var, ascending=False).head(3).review_id.values


def print_top3_offenders(df, top3_offender_ids):
	print(df[df["review_id"].isin(top3_offender_ids)].to_string())


def analyze_reviews(df):
	sentiment_df = clean_data(df)
	sentiment_df = post_process(sentiment_df)
	top3_offenders = get_top3_offenders(sentiment_df)
	print_top3_offenders(df, top3_offenders)


if __name__ == '__main__':
	analyze_reviews(read_data())

